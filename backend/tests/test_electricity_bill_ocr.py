from __future__ import annotations

import io

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.database.base import Base
from app.database.seed import seed_database
from app.main import app
from app.models import load_models


@pytest.fixture
def client_with_db():
    load_models()
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(bind=engine)

    session = TestingSessionLocal()
    seed_database(session)
    session.close()

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.clear()


def test_valid_structured_ocr_response_parsing(client_with_db: TestClient, monkeypatch):
    from app.services import electricity_ocr_service

    class FakeExtractor:
        def extract_bill(self, *, file_bytes, file_name, mime_type):
            return {
                "status": "success",
                "extracted_consumption": 220.5,
                "unit": "kWh",
                "billing_start_date": "2026-09-01",
                "billing_end_date": "2026-09-30",
                "provider": "BSES Rajdhani",
                "bill_amount": 1234.56,
                "confidence": 0.87,
                "needs_confirmation": ["consumption"],
                "source": "gemini",
            }

    monkeypatch.setattr(electricity_ocr_service, "GeminiBillExtractor", FakeExtractor)

    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("bill.pdf", b"%PDF-1.4 fake pdf", "application/pdf")},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["consumption"] == 220.5
    assert data["unit"] == "kWh"
    assert data["provider"] == "BSES Rajdhani"
    assert data["needs_confirmation"] == ["consumption"]


def test_missing_consumption_rejected(client_with_db: TestClient, monkeypatch):
    from app.services import electricity_ocr_service

    class FakeExtractor:
        def extract_bill(self, *, file_bytes, file_name, mime_type):
            return {
                "status": "success",
                "extracted_consumption": None,
                "unit": "kWh",
                "provider": "MGVCL",
            }

    monkeypatch.setattr(electricity_ocr_service, "GeminiBillExtractor", FakeExtractor)

    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("bill.png", b"fake-image-png", "image/png")},
    )
    assert response.status_code == 400
    assert "consumption" in response.json()["detail"].lower()


def test_invalid_consumption_rejected(client_with_db: TestClient, monkeypatch):
    from app.services import electricity_ocr_service

    class FakeExtractor:
        def extract_bill(self, *, file_bytes, file_name, mime_type):
            return {
                "status": "success",
                "extracted_consumption": -12,
                "unit": "kWh",
                "provider": "BSES",
            }

    monkeypatch.setattr(electricity_ocr_service, "GeminiBillExtractor", FakeExtractor)

    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("bill.jpg", b"fake-image-jpg", "image/jpeg")},
    )
    assert response.status_code == 400
    assert "greater than 0" in response.json()["detail"].lower()


def test_invalid_file_type_rejected(client_with_db: TestClient):
    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("notes.txt", b"not an image or pdf", "text/plain")},
    )
    assert response.status_code == 400
    assert "unsupported file type" in response.json()["detail"].lower()


def test_oversized_upload_rejected(client_with_db: TestClient):
    large_bytes = b"a" * (11 * 1024 * 1024)
    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("large.pdf", large_bytes, "application/pdf")},
    )
    assert response.status_code == 413


def test_confirmation_validation(client_with_db: TestClient):
    payload = {
        "user_id": 1,
        "consumption": 0,
        "unit": "kWh",
        "billing_start_date": "2026-09-01",
        "billing_end_date": "2026-09-30",
    }
    response = client_with_db.post("/api/electricity-bills/confirm", json=payload)
    assert response.status_code == 400
    assert "greater than 0" in response.json()["detail"].lower()


def test_confirmed_bill_creates_activity_and_uses_existing_carbon_engine(client_with_db: TestClient, monkeypatch):
    from app.api import electricity_bills as bills_api

    captured = {}

    def fake_calculate_emission(*, category, activity_type, quantity, unit, db, region="global"):
        captured["category"] = category
        captured["activity_type"] = activity_type
        captured["quantity"] = quantity
        captured["unit"] = unit
        Result = type(
            "Result",
            (),
            {
                "category": category,
                "activity_type": activity_type,
                "quantity": quantity,
                "unit": unit,
                "emission": 71.6,
                "emission_factor": 0.716,
                "factor_source": "Test source",
                "factor_source_year": 2024,
                "region": region,
            },
        )
        return Result()

    monkeypatch.setattr(bills_api, "calculate_emission", fake_calculate_emission)

    payload = {
        "user_id": 1,
        "consumption": 100,
        "unit": "kWh",
        "billing_start_date": "2026-09-01",
        "billing_end_date": "2026-09-30",
        "provider": "BSES",
        "bill_amount": 1200,
    }
    response = client_with_db.post("/api/electricity-bills/confirm", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "electricity"
    assert data["activity_type"] == "grid_electricity"
    assert data["quantity"] == 100.0
    assert data["unit"] == "kWh"
    assert abs(data["emission"] - 71.6) < 1e-6
    assert captured["category"] == "electricity"
    assert captured["activity_type"] == "grid_electricity"


def test_gemini_api_failure_handled_cleanly(client_with_db: TestClient, monkeypatch):
    from app.services import electricity_ocr_service

    class BrokenExtractor:
        def extract_bill(self, *, file_bytes, file_name, mime_type):
            raise RuntimeError("Gemini API key is invalid or missing: GEMINI_API_KEY=secret-value")

    monkeypatch.setattr(electricity_ocr_service, "GeminiBillExtractor", BrokenExtractor)

    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("bill.pdf", b"%PDF-1.4 fake pdf", "application/pdf")},
    )
    assert response.status_code == 502
    body = response.json()
    assert "gemini" in body["detail"].lower()
    assert "secret-value" not in body["detail"].lower()
    assert "gemini_api_key" not in body["detail"].lower()


def test_api_key_not_exposed_in_responses_or_logs(client_with_db: TestClient, monkeypatch, caplog):
    from app.services import electricity_ocr_service

    class BrokenExtractor:
        def extract_bill(self, *, file_bytes, file_name, mime_type):
            raise RuntimeError("GEMINI_API_KEY=super-secret-key")

    monkeypatch.setattr(electricity_ocr_service, "GeminiBillExtractor", BrokenExtractor)

    response = client_with_db.post(
        "/api/electricity-bills/extract",
        files={"file": ("bill.jpg", b"fake-jpg", "image/jpeg")},
    )

    assert response.status_code == 502
    response_text = str(response.json())
    assert "super-secret-key" not in response_text
    assert "GEMINI_API_KEY" not in response_text
    assert "super-secret-key" not in caplog.text
