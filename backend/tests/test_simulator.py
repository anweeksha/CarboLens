"""Unit & API tests for What-If Simulator."""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.database.base import Base
from app.database.seed import seed_database
from app.main import app
from app.models import load_models
from app.models.activity import Activity
from app.models.emission_factor import EmissionFactor
from app.services.simulator import SimulationChangeItemInput, run_simulation


@pytest.fixture
def client_and_session():
    """Create isolated SQLite in-memory fixture for simulator tests."""
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

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    try:
        yield client, session
    finally:
        session.close()
        app.dependency_overrides.clear()


def test_single_what_if_change(client_and_session):
    """Test 6: Single what-if change simulation (car 240 km -> bus 240 km)."""
    client, session = client_and_session

    changes = [
        SimulationChangeItemInput(
            category="travel",
            from_activity="car",
            to_activity="bus",
            quantity=240.0,
            unit="km",
        )
    ]
    res = run_simulation(user_id=1, changes=changes, db=session)

    # Car: 240 * 0.1709 = 41.016, Bus: 240 * 0.0965 = 23.16 -> Saving = 17.856 (43.53% reduction)
    assert res["user_id"] == 1
    assert abs(res["current_total"] - 41.016) < 1e-2
    assert abs(res["projected_total"] - 23.16) < 1e-2
    assert abs(res["total_saving"] - 17.856) < 1e-2
    assert abs(res["reduction_percentage"] - 43.53) < 1e-1
    assert len(res["changes"]) == 1


def test_multiple_what_if_changes(client_and_session):
    """Test 7: Multiple simultaneous what-if changes in one simulation request."""
    client, session = client_and_session

    payload = {
        "user_id": 1,
        "changes": [
            {
                "category": "travel",
                "from_activity": "car",
                "to_activity": "bus",
                "quantity": 240.0,
                "unit": "km",
            },
            {
                "category": "food",
                "from_activity": "non_vegetarian_meal",
                "to_activity": "vegetarian_meal",
                "quantity": 20.0,
                "unit": "meal",
            },
        ],
    }

    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert len(data["changes"]) == 2

    # Travel saving: 17.856, Food saving: 20 * (3.5 - 1.2) = 46.0 -> Total saving = 63.856
    assert abs(data["total_saving"] - 63.856) < 1e-2
    assert data["total_saving"] > 0


def test_simulator_does_not_modify_database(client_and_session):
    """Test 9: Verify POST /api/simulate is strictly read-only and alters 0 database records."""
    client, session = client_and_session

    initial_activities_count = len(session.scalars(select(Activity)).all())
    initial_factors_count = len(session.scalars(select(EmissionFactor)).all())

    payload = {
        "user_id": 1,
        "changes": [
            {
                "category": "travel",
                "from_activity": "car",
                "to_activity": "bus",
                "quantity": 500.0,
                "unit": "km",
            }
        ],
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 200

    final_activities_count = len(session.scalars(select(Activity)).all())
    final_factors_count = len(session.scalars(select(EmissionFactor)).all())

    assert final_activities_count == initial_activities_count
    assert final_factors_count == initial_factors_count


def test_zero_emission_edge_case(client_and_session):
    """Test 8: Simulation edge case handling empty change list or zero saving."""
    client, session = client_and_session

    res = run_simulation(user_id=1, changes=[], db=session)
    assert res["current_total"] == 0.0
    assert res["projected_total"] == 0.0
    assert res["total_saving"] == 0.0
    assert res["reduction_percentage"] == 0.0


def test_invalid_quantity_rejection_in_simulation(client_and_session):
    """Test 10: Rejection of negative or zero quantities in simulation requests."""
    client, session = client_and_session

    payload = {
        "user_id": 1,
        "changes": [
            {
                "category": "travel",
                "from_activity": "car",
                "to_activity": "bus",
                "quantity": -50.0,
                "unit": "km",
            }
        ],
    }
    response = client.post("/api/simulate", json=payload)
    assert response.status_code == 422  # Pydantic schema validation rejects <= 0 quantity
