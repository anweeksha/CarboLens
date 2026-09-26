"""Unit & API integration tests for Campus Analytics, Department/Hostel Aggregation, Benchmarks, and Leaderboards."""

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
from app.models.department import Department
from app.models.hostel import Hostel
from app.models.user import User
from app.services.campus_engine import (
    get_campus_overview,
    get_campus_trend,
    get_department_analytics,
    get_hostel_analytics,
    get_leaderboard,
    get_user_benchmark,
)


@pytest.fixture
def client_and_session():
    """Create isolated in-memory SQLite fixture for campus analytics tests."""
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


def test_zero_activity_and_zero_active_users_campus(client_and_session):
    """Tests 9, 10: Campus overview with 0 activities & 0 active users returns safe zero averages."""
    client, session = client_and_session

    overview = get_campus_overview(month=9, year=2026, db=session)
    assert overview["total_emission"] == 0.0
    assert overview["active_users"] == 0
    assert overview["average_per_active_user"] == 0.0
    assert overview["categories"]["travel"] == 0.0
    assert overview["category_percentages"]["travel"] == 0.0


def test_campus_total_category_breakdown_and_active_users(client_and_session):
    """Tests 1, 2, 4, 5: Campus total calculation, category breakdown, active users, and average per active user."""
    client, session = client_and_session

    dept_cst = session.query(Department).filter_by(name="Computer Science & Engineering").first()
    hostel_a = session.query(Hostel).filter_by(name="Hostel Alpha").first()

    # Create User 2
    u2 = User(id=2, name="User Two", email="u2@test.org", department_id=dept_cst.id, hostel_id=hostel_a.id, user_type="student")
    session.add(u2)
    session.commit()

    # Add activities for User 1 & User 2 in Sept 2026
    session.add_all([
        Activity(user_id=1, category="travel", activity_type="car", quantity=100, unit="km", activity_date=date(2026, 9, 10), emission=17.09),
        Activity(user_id=2, category="electricity", activity_type="grid_electricity", quantity=200, unit="kWh", activity_date=date(2026, 9, 15), emission=143.2),
    ])
    session.commit()

    overview = get_campus_overview(month=9, year=2026, db=session)
    # Total = 17.09 + 143.2 = 160.29
    assert abs(overview["total_emission"] - 160.29) < 1e-2
    assert overview["active_users"] == 2
    # Avg = 160.29 / 2 = 80.145
    assert abs(overview["average_per_active_user"] - 80.145) < 1e-2
    assert abs(overview["categories"]["travel"] - 17.09) < 1e-2
    assert abs(overview["categories"]["electricity"] - 143.2) < 1e-2
    assert overview["categories"]["food"] == 0.0


def test_campus_monthly_trend(client_and_session):
    """Test 3: Campus monthly trend returns chronological monthly emission totals."""
    client, session = client_and_session

    session.add_all([
        Activity(user_id=1, category="travel", activity_type="car", quantity=100, unit="km", activity_date=date(2026, 6, 10), emission=17.09),
        Activity(user_id=1, category="electricity", activity_type="grid_electricity", quantity=100, unit="kWh", activity_date=date(2026, 7, 15), emission=71.60),
    ])
    session.commit()

    res = get_campus_trend(start_date=None, end_date=None, db=session)
    trend = res["trend"]
    assert len(trend) == 2
    assert trend[0]["month"] == "2026-06"
    assert abs(trend[0]["emission"] - 17.09) < 1e-2
    assert trend[1]["month"] == "2026-07"
    assert abs(trend[1]["emission"] - 71.60) < 1e-2


def test_department_and_hostel_aggregation(client_and_session):
    """Tests 6, 7, 12: Department & hostel aggregation with population, active users, and missing dept/hostel handling."""
    client, session = client_and_session

    dept_cst = session.query(Department).filter_by(name="Computer Science & Engineering").first()
    hostel_a = session.query(Hostel).filter_by(name="Hostel Alpha").first()

    # User 3 without department or hostel
    u3 = User(id=3, name="User Three No Dept", email="u3@test.org", department_id=None, hostel_id=None, user_type="staff")
    session.add(u3)

    # Activity for User 1 (belonging to CST & Hostel Alpha)
    session.add(Activity(user_id=1, category="travel", activity_type="car", quantity=100, unit="km", activity_date=date(2026, 9, 10), emission=17.09))
    # Activity for User 3 (no department/hostel)
    session.add(Activity(user_id=3, category="food", activity_type="vegetarian_meal", quantity=10, unit="meal", activity_date=date(2026, 9, 11), emission=12.0))
    session.commit()

    dept_res = get_department_analytics(month=9, year=2026, db=session)["departments"]
    cst_dept = next(d for d in dept_res if d["department"] == "Computer Science & Engineering")
    assert cst_dept["active_users"] == 1
    assert abs(cst_dept["total_emission"] - 17.09) < 1e-2

    hostel_res = get_hostel_analytics(month=9, year=2026, db=session)["hostels"]
    alpha_hostel = next(h for h in hostel_res if h["hostel"] == "Hostel Alpha")
    assert alpha_hostel["active_users"] == 1
    assert abs(alpha_hostel["total_emission"] - 17.09) < 1e-2


def test_user_benchmark(client_and_session):
    """Test 8: User benchmark comparison against campus average per active user."""
    client, session = client_and_session

    dept_cst = session.query(Department).filter_by(name="Computer Science & Engineering").first()
    hostel_a = session.query(Hostel).filter_by(name="Hostel Alpha").first()

    u2 = User(id=2, name="User Two", email="u2@test.org", department_id=dept_cst.id, hostel_id=hostel_a.id, user_type="student")
    session.add(u2)
    session.commit()

    # User 1 emission = 100.0, User 2 emission = 50.0. Campus avg per active user = 75.0
    session.add_all([
        Activity(user_id=1, category="electricity", activity_type="grid_electricity", quantity=100, unit="kWh", activity_date=date(2026, 9, 10), emission=100.0),
        Activity(user_id=2, category="electricity", activity_type="grid_electricity", quantity=50, unit="kWh", activity_date=date(2026, 9, 12), emission=50.0),
    ])
    session.commit()

    bm = get_user_benchmark(user_id=1, month=9, year=2026, db=session)
    assert bm["user_id"] == 1
    assert bm["user_emission"] == 100.0
    assert bm["campus_average"] == 75.0
    assert bm["difference"] == 25.0
    assert abs(bm["difference_percentage"] - 33.33) < 1e-1
    assert bm["benchmark_type"] == "Campus average per active user"


def test_leaderboard_endpoint(client_and_session):
    """Test 11: GET /api/leaderboard for department and hostel entities."""
    client, session = client_and_session

    response = client.get("/api/leaderboard?type=department&month=9&year=2026")
    assert response.status_code == 200
    data = response.json()
    assert data["entity_type"] == "department"
    assert "leaderboard" in data
    assert len(data["leaderboard"]) > 0

    # Test invalid type returns HTTP 400
    bad_resp = client.get("/api/leaderboard?type=invalid_type")
    assert bad_resp.status_code == 400
