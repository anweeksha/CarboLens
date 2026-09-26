"""Unit & API tests for personalized recommendations and top carbon drivers."""

from datetime import date

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.deps import get_db
from app.database.base import Base
from app.database.seed import seed_database
from app.main import app
from app.models import load_models
from app.models.activity import Activity
from app.services.recommendation_engine import generate_recommendations, get_top_carbon_drivers


@pytest.fixture
def client_and_session():
    """Create a clean isolated SQLite in-memory database fixture for recommendation tests."""
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


def test_top_carbon_drivers(client_and_session):
    """Test 5: Top carbon drivers selection based on actual stored activity emissions."""
    client, session = client_and_session

    # Log activities for user 1
    session.add_all([
        Activity(user_id=1, category="travel", activity_type="car", quantity=100, unit="km", activity_date=date(2026, 9, 10), emission=17.09),
        Activity(user_id=1, category="electricity", activity_type="grid_electricity", quantity=500, unit="kWh", activity_date=date(2026, 9, 12), emission=358.0),
        Activity(user_id=1, category="food", activity_type="vegetarian_meal", quantity=5, unit="meal", activity_date=date(2026, 9, 14), emission=6.0),
    ])
    session.commit()

    drivers = get_top_carbon_drivers(user_id=1, month=9, year=2026, db=session, limit=3)
    assert len(drivers) == 3
    # First top driver should be electricity (358.0 kgCO2e)
    assert drivers[0].category == "electricity"
    assert drivers[0].activity_type == "grid_electricity"
    assert abs(drivers[0].emission - 358.0) < 1e-2

    # Second top driver should be travel (17.09 kgCO2e)
    assert drivers[1].category == "travel"
    assert drivers[1].activity_type == "car"


def test_recommendation_generation_and_ranking(client_and_session):
    """Tests 1, 2, 3: Recommendation generation, ranking by potential saving, and potential saving calculation."""
    client, session = client_and_session

    # Add duplicate activities: 100 km car + 140 km car = 240 km car total
    session.add_all([
        Activity(user_id=1, category="travel", activity_type="car", quantity=100, unit="km", activity_date=date(2026, 9, 10), emission=17.09),
        Activity(user_id=1, category="travel", activity_type="car", quantity=140, unit="km", activity_date=date(2026, 9, 12), emission=23.926),
        # Food activity: 10 non-veg meals
        Activity(user_id=1, category="food", activity_type="non_vegetarian_meal", quantity=10, unit="meal", activity_date=date(2026, 9, 15), emission=35.0),
    ])
    session.commit()

    res = generate_recommendations(user_id=1, month=9, year=2026, db=session)
    recs = res["recommendations"]

    assert len(recs) >= 2
    # Verify aggregation: quantity for car travel recommendation should be 240 km
    car_rec = next(r for r in recs if r["current_activity"] == "car")
    assert car_rec["quantity"] == 240.0
    # Car (0.1709) vs Bus (0.0965): 240 * 0.1709 = 41.016, 240 * 0.0965 = 23.16 -> saving = 17.856
    assert abs(car_rec["potential_saving"] - 17.856) < 1e-2

    # Verify ranking: recommendations must be sorted by potential_saving DESC
    savings = [r["potential_saving"] for r in recs]
    assert savings == sorted(savings, reverse=True)


def test_missing_alternative_factor(client_and_session):
    """Test 4: Missing alternative factor does not generate invalid recommendation."""
    client, session = client_and_session

    # Add activity with no valid alternative factor in DB
    session.add(Activity(user_id=1, category="waste", activity_type="organic_waste", quantity=10, unit="kg", activity_date=date(2026, 9, 10), emission=5.84))
    session.commit()

    res = generate_recommendations(user_id=1, month=9, year=2026, db=session)
    recs = res["recommendations"]
    # Should not contain an alternative for organic_waste because no lower-emission alternative factor exists for organic waste in DB
    assert not any(r["current_activity"] == "organic_waste" for r in recs)


def test_recommendations_api_endpoint(client_and_session):
    """Test GET /api/users/{user_id}/recommendations HTTP endpoint."""
    client, session = client_and_session

    session.add(Activity(user_id=1, category="travel", activity_type="car", quantity=200, unit="km", activity_date=date(2026, 9, 10), emission=34.18))
    session.commit()

    response = client.get("/api/users/1/recommendations?month=9&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert "top_drivers" in data
    assert len(data["recommendations"]) > 0
    assert data["recommendations"][0]["category"] == "travel"
