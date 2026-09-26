"""Integration API tests for activity logging, footprint, category breakdown, and monthly trend."""

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
    """Create FastAPI test client with an isolated in-memory SQLite database."""
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


def test_activity_creation_api(client_with_db: TestClient):
    """Test 5: POST /api/activities creates an activity and calculates emission."""
    payload = {
        "user_id": 1,
        "category": "travel",
        "activity_type": "car",
        "quantity": 100.0,
        "unit": "km",
        "activity_date": "2026-09-15",
        "metadata": {"note": "Test trip"},
    }
    response = client_with_db.post("/api/activities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["user_id"] == 1
    assert data["category"] == "travel"
    assert data["activity_type"] == "car"
    assert data["quantity"] == 100.0
    assert data["unit"] == "km"
    assert abs(data["emission"] - 17.09) < 1e-3
    assert data["emission_factor_used"] == 0.1709
    assert "UK DEFRA" in data["emission_factor_source"]


def test_footprint_calculation_api(client_with_db: TestClient):
    """Test 6: GET /api/users/{user_id}/footprint calculates total monthly CO2e."""
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "travel",
        "activity_type": "car",
        "quantity": 100.0,
        "unit": "km",
        "activity_date": "2026-09-10",
    })
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "electricity",
        "activity_type": "grid_electricity",
        "quantity": 200.0,
        "unit": "kWh",
        "activity_date": "2026-09-15",
    })

    response = client_with_db.get("/api/users/1/footprint?month=9&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["month"] == 9
    assert data["year"] == 2026
    # 100*0.1709 = 17.09, 200*0.7160 = 143.2 -> Total = 160.29
    assert abs(data["total_emission"] - 160.29) < 1e-2


def test_category_breakdown_api(client_with_db: TestClient):
    """Test 7: GET /api/users/{user_id}/breakdown returns emissions grouped by category."""
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "travel",
        "activity_type": "car",
        "quantity": 100.0,
        "unit": "km",
        "activity_date": "2026-09-10",
    })
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "food",
        "activity_type": "vegetarian_meal",
        "quantity": 10.0,
        "unit": "meal",
        "activity_date": "2026-09-12",
    })

    response = client_with_db.get("/api/users/1/breakdown?month=9&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert abs(data["travel"] - 17.09) < 1e-2
    assert abs(data["food"] - 12.0) < 1e-2
    assert data["electricity"] == 0.0
    assert data["waste"] == 0.0


def test_monthly_trend_api(client_with_db: TestClient):
    """Test 8: GET /api/users/{user_id}/trend returns chronological monthly totals."""
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "travel",
        "activity_type": "car",
        "quantity": 100.0,
        "unit": "km",
        "activity_date": "2026-06-15",
    })
    client_with_db.post("/api/activities", json={
        "user_id": 1,
        "category": "electricity",
        "activity_type": "grid_electricity",
        "quantity": 100.0,
        "unit": "kWh",
        "activity_date": "2026-07-20",
    })

    response = client_with_db.get("/api/users/1/trend")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    trend = data["trend"]
    assert len(trend) == 2
    assert trend[0]["month"] == "2026-06"
    assert abs(trend[0]["emission"] - 17.09) < 1e-2
    assert trend[1]["month"] == "2026-07"
    assert abs(trend[1]["emission"] - 71.60) < 1e-2
