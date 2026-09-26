from __future__ import annotations

from datetime import date

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


def test_campus_report_pdf_success(client_with_db: TestClient):
    client_with_db.post(
        "/api/activities",
        json={
            "user_id": 1,
            "category": "travel",
            "activity_type": "car",
            "quantity": 100.0,
            "unit": "km",
            "activity_date": "2026-09-15",
        },
    )
    client_with_db.post(
        "/api/activities",
        json={
            "user_id": 1,
            "category": "electricity",
            "activity_type": "grid_electricity",
            "quantity": 200.0,
            "unit": "kWh",
            "activity_date": "2026-09-20",
        },
    )

    response = client_with_db.get(
        "/api/campus/report/pdf",
        params={"start_date": "2026-09-01", "end_date": "2026-09-30"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert "attachment; filename=\"carbonlens-campus-sustainability-report-2026-09-01-to-2026-09-30.pdf\"" in response.headers["content-disposition"]
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 100


def test_campus_report_pdf_period_validation(client_with_db: TestClient):
    response = client_with_db.get(
        "/api/campus/report/pdf",
        params={"start_date": "2026-10-01", "end_date": "2026-09-30"},
    )
    assert response.status_code == 400
    assert "end_date" in response.json()["detail"].lower()


def test_campus_report_pdf_no_data_period(client_with_db: TestClient):
    response = client_with_db.get(
        "/api/campus/report/pdf",
        params={"start_date": "2025-01-01", "end_date": "2025-01-31"},
    )
    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert response.content.startswith(b"%PDF")


def test_campus_report_pdf_analytics_failure_handling(client_with_db: TestClient, monkeypatch):
    from app.api import campus as campus_api

    def boom(*args, **kwargs):
        raise RuntimeError("analytics unavailable")

    monkeypatch.setattr(campus_api, "generate_campus_sustainability_report_pdf", boom)

    response = client_with_db.get(
        "/api/campus/report/pdf",
        params={"start_date": "2026-09-01", "end_date": "2026-09-30"},
    )

    assert response.status_code == 500
    assert "report" in response.json()["detail"].lower()


def test_campus_report_pdf_service_stays_database_backed(client_with_db: TestClient):
    client_with_db.post(
        "/api/activities",
        json={
            "user_id": 1,
            "category": "travel",
            "activity_type": "car",
            "quantity": 200.0,
            "unit": "km",
            "activity_date": "2026-09-10",
        },
    )

    response = client_with_db.get(
        "/api/campus/report/pdf",
        params={"start_date": "2026-09-01", "end_date": "2026-09-30"},
    )

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("application/pdf")
    assert len(response.content) > 100
