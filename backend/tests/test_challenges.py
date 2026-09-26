"""Comprehensive tests for Challenge Engine — Step 6.

Covers 14 test cases:
 1. Challenge model creation/validation
 2. Listing challenges
 3. Joining a challenge
 4. Duplicate challenge join (409)
 5. Baseline calculation from preceding period
 6. Insufficient baseline data
 7. Current emission calculation during challenge period
 8. CO2e savings (baseline − current, clamped ≥ 0)
 9. Negative savings handling (user increased emissions)
10. Completion percentage calculation
11. Challenge summary aggregation
12. Challenge leaderboard ordering
13. Invalid challenge ID (404)
14. Invalid user ID (404)
"""

from datetime import date, timedelta

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
from app.models.challenge import Challenge
from app.models.challenge_progress import ChallengeProgress
from app.models.department import Department
from app.models.hostel import Hostel
from app.models.user import User
from app.services.challenge_engine import (
    ChallengeDuplicateJoinError,
    ChallengeNotFoundError,
    ChallengeUserNotFoundError,
    get_challenge_leaderboard,
    get_challenge_progress,
    get_challenge_summary,
    join_challenge,
    list_challenges,
)


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def client_and_session():
    """Create isolated in-memory SQLite environment with seed data and sample challenges."""
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

    # Create a second user for multi-participant tests
    dept = session.query(Department).filter_by(name="Computer Science & Engineering").first()
    hostel = session.query(Hostel).filter_by(name="Hostel Alpha").first()
    u2 = User(id=2, name="User Two", email="u2@test.org", department_id=dept.id, hostel_id=hostel.id, user_type="student")
    session.add(u2)
    session.commit()

    # Challenge dates: active challenge running this week (Sep 20–26), baseline = Sep 13–19
    active_challenge = Challenge(
        id=1,
        name="No-Car Week",
        description="Avoid car travel for one week",
        category="travel",
        activity_type="car",
        start_date=date(2026, 9, 20),
        end_date=date(2026, 9, 26),
        target=50.0,
        target_unit="km",
    )

    # Upcoming challenge (starts Oct 1)
    upcoming_challenge = Challenge(
        id=2,
        name="Reduce Electricity",
        description="Reduce electricity consumption",
        category="electricity",
        activity_type="grid_electricity",
        start_date=date(2026, 10, 1),
        end_date=date(2026, 10, 7),
        target=100.0,
        target_unit="kWh",
    )

    # Completed challenge (ended Sep 12)
    completed_challenge = Challenge(
        id=3,
        name="Lower-Carbon Food",
        description="Switch to vegetarian meals",
        category="food",
        activity_type="non_vegetarian_meal",
        start_date=date(2026, 9, 6),
        end_date=date(2026, 9, 12),
        target=10.0,
        target_unit="meal",
    )

    session.add_all([active_challenge, upcoming_challenge, completed_challenge])
    session.commit()

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


def _add_car_activities(session: Session, user_id: int, period_start: date, period_end: date, km_per_day: float):
    """Helper: add car activities for each day in a period."""
    emission_per_km = 0.1709  # from seed data
    current = period_start
    while current <= period_end:
        session.add(Activity(
            user_id=user_id,
            category="travel",
            activity_type="car",
            quantity=km_per_day,
            unit="km",
            activity_date=current,
            emission=km_per_day * emission_per_km,
            emission_factor_used=emission_per_km,
            emission_factor_source="UK DEFRA 2024",
        ))
        current += timedelta(days=1)
    session.commit()


# ---------------------------------------------------------------------------
# Test 1: Challenge model creation/validation
# ---------------------------------------------------------------------------

def test_challenge_model_creation(client_and_session):
    """Test 1: Challenge model stores all required fields correctly."""
    _, session = client_and_session
    challenge = session.get(Challenge, 1)
    assert challenge is not None
    assert challenge.name == "No-Car Week"
    assert challenge.category == "travel"
    assert challenge.activity_type == "car"
    assert challenge.start_date == date(2026, 9, 20)
    assert challenge.end_date == date(2026, 9, 26)
    assert float(challenge.target) == 50.0
    assert challenge.target_unit == "km"


# ---------------------------------------------------------------------------
# Test 2: Listing challenges
# ---------------------------------------------------------------------------

def test_list_all_challenges(client_and_session):
    """Test 2a: GET /api/challenges returns all challenges."""
    client, _ = client_and_session
    resp = client.get("/api/challenges")
    assert resp.status_code == 200
    data = resp.json()
    assert data["count"] == 3


def test_list_challenges_by_status(client_and_session):
    """Test 2b: GET /api/challenges?status=active filters correctly."""
    client, _ = client_and_session

    # Active
    resp = client.get("/api/challenges?status=active")
    assert resp.status_code == 200
    data = resp.json()
    assert all(c["status"] == "active" for c in data["challenges"])
    assert any(c["name"] == "No-Car Week" for c in data["challenges"])

    # Upcoming
    resp = client.get("/api/challenges?status=upcoming")
    data = resp.json()
    assert all(c["status"] == "upcoming" for c in data["challenges"])

    # Completed
    resp = client.get("/api/challenges?status=completed")
    data = resp.json()
    assert all(c["status"] == "completed" for c in data["challenges"])


def test_list_challenges_invalid_status(client_and_session):
    """Test 2c: Invalid status filter returns 400."""
    client, _ = client_and_session
    resp = client.get("/api/challenges?status=invalid")
    assert resp.status_code == 400


# ---------------------------------------------------------------------------
# Test 3: Joining a challenge
# ---------------------------------------------------------------------------

def test_join_challenge_api(client_and_session):
    """Test 3: POST /api/challenges/{id}/join creates progress record."""
    client, session = client_and_session

    # Add baseline period car activities for user 1 (Sep 13–19)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)

    resp = client.post("/api/challenges/1/join", json={"user_id": 1})
    assert resp.status_code == 201
    data = resp.json()
    assert data["challenge_id"] == 1
    assert data["user_id"] == 1
    assert data["status"] == "joined"
    assert data["baseline_status"] == "calculated"
    # baseline = 7 days × 20 km/day × 0.1709 = 23.926
    assert data["baseline_emission"] > 0


# ---------------------------------------------------------------------------
# Test 4: Duplicate challenge join
# ---------------------------------------------------------------------------

def test_duplicate_join_rejected(client_and_session):
    """Test 4: Joining the same challenge twice returns 409."""
    client, session = client_and_session

    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=10.0)

    resp1 = client.post("/api/challenges/1/join", json={"user_id": 1})
    assert resp1.status_code == 201

    resp2 = client.post("/api/challenges/1/join", json={"user_id": 1})
    assert resp2.status_code == 409


# ---------------------------------------------------------------------------
# Test 5: Baseline calculation
# ---------------------------------------------------------------------------

def test_baseline_calculation_from_preceding_period(client_and_session):
    """Test 5: Baseline uses activities from the period immediately preceding the challenge."""
    _, session = client_and_session

    # Baseline period for Challenge 1 (Sep 20-26) is Sep 13-19
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=30.0)

    result = join_challenge(challenge_id=1, user_id=1, db=session)
    # 7 days × 30 km × 0.1709 = 35.889
    expected_baseline = 7 * 30.0 * 0.1709
    assert abs(result["baseline_emission"] - expected_baseline) < 0.01
    assert result["baseline_status"] == "calculated"


# ---------------------------------------------------------------------------
# Test 6: Insufficient baseline data
# ---------------------------------------------------------------------------

def test_insufficient_baseline_data(client_and_session):
    """Test 6: No historical data results in 'insufficient_baseline_data' status."""
    _, session = client_and_session

    # No activities in baseline period
    result = join_challenge(challenge_id=1, user_id=1, db=session)
    assert result["baseline_emission"] == 0.0
    assert result["baseline_status"] == "insufficient_baseline_data"


# ---------------------------------------------------------------------------
# Test 7: Current emission calculation
# ---------------------------------------------------------------------------

def test_current_emission_from_challenge_period(client_and_session):
    """Test 7: Current emission is calculated from activities during the challenge period."""
    _, session = client_and_session

    # Add baseline activities
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    join_challenge(challenge_id=1, user_id=1, db=session)

    # Add challenge-period activities (reduced driving)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=5.0)

    progress = get_challenge_progress(challenge_id=1, user_id=1, db=session)
    expected_current = 7 * 5.0 * 0.1709
    assert abs(progress["current_emission"] - expected_current) < 0.01


# ---------------------------------------------------------------------------
# Test 8: CO2e savings
# ---------------------------------------------------------------------------

def test_co2e_savings_calculation(client_and_session):
    """Test 8: saved_emission = baseline_emission - current_emission (clamped ≥ 0)."""
    _, session = client_and_session

    # Baseline: 20 km/day
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    join_challenge(challenge_id=1, user_id=1, db=session)

    # Challenge period: 5 km/day (reduced)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=5.0)

    progress = get_challenge_progress(challenge_id=1, user_id=1, db=session)
    expected_saved = 7 * (20.0 - 5.0) * 0.1709
    assert abs(progress["saved_emission"] - expected_saved) < 0.01
    assert progress["saved_emission"] > 0


# ---------------------------------------------------------------------------
# Test 9: Negative savings handling
# ---------------------------------------------------------------------------

def test_negative_savings_clamped_to_zero(client_and_session):
    """Test 9: If user increased emissions, saved_emission = 0 (not negative)."""
    _, session = client_and_session

    # Baseline: 5 km/day
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=5.0)
    join_challenge(challenge_id=1, user_id=1, db=session)

    # Challenge period: 30 km/day (INCREASED)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=30.0)

    progress = get_challenge_progress(challenge_id=1, user_id=1, db=session)
    assert progress["saved_emission"] == 0.0
    # Completion should be 0% since user went wrong direction
    assert progress["completion_percentage"] == 0.0


# ---------------------------------------------------------------------------
# Test 10: Completion percentage
# ---------------------------------------------------------------------------

def test_completion_percentage(client_and_session):
    """Test 10: Completion % = (baseline_qty - current_qty) / target * 100, clamped 0–100."""
    _, session = client_and_session

    # Baseline: 20 km/day × 7 days = 140 km total
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    join_challenge(challenge_id=1, user_id=1, db=session)

    # Challenge: 10 km/day × 7 days = 70 km total
    # Reduction = 140 - 70 = 70 km
    # target = 50 km → completion = 70/50 * 100 = 140% → clamped to 100%
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=10.0)

    progress = get_challenge_progress(challenge_id=1, user_id=1, db=session)
    assert progress["completion_percentage"] == 100.0
    assert progress["status"] == "completed"


def test_partial_completion_percentage(client_and_session):
    """Test 10b: Partial completion reflects proportional progress."""
    _, session = client_and_session

    # Baseline: 20 km/day × 7 = 140 km
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    join_challenge(challenge_id=1, user_id=1, db=session)

    # Challenge: 15 km/day × 7 = 105 km
    # Reduction = 140 - 105 = 35 km, target = 50
    # completion = 35/50 * 100 = 70%
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=15.0)

    progress = get_challenge_progress(challenge_id=1, user_id=1, db=session)
    assert abs(progress["completion_percentage"] - 70.0) < 0.1


# ---------------------------------------------------------------------------
# Test 11: Challenge summary
# ---------------------------------------------------------------------------

def test_challenge_summary(client_and_session):
    """Test 11: Summary aggregates across all participants."""
    _, session = client_and_session

    # User 1: baseline 20 km/day, challenge 5 km/day
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    join_challenge(challenge_id=1, user_id=1, db=session)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=5.0)

    # User 2: baseline 10 km/day, challenge 3 km/day
    _add_car_activities(session, user_id=2, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=10.0)
    join_challenge(challenge_id=1, user_id=2, db=session)
    _add_car_activities(session, user_id=2, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=3.0)

    summary = get_challenge_summary(challenge_id=1, db=session)
    assert summary["participants"] == 2
    assert summary["total_baseline_emission"] > 0
    assert summary["total_current_emission"] > 0
    assert summary["total_saved_emission"] > 0
    assert summary["average_saved_per_participant"] > 0


def test_challenge_summary_api(client_and_session):
    """Test 11b: GET /api/challenges/{id}/summary returns correct response."""
    client, session = client_and_session

    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    client.post("/api/challenges/1/join", json={"user_id": 1})

    resp = client.get("/api/challenges/1/summary")
    assert resp.status_code == 200
    data = resp.json()
    assert data["challenge_id"] == 1
    assert data["participants"] == 1
    assert "total_saved_emission" in data


# ---------------------------------------------------------------------------
# Test 12: Challenge leaderboard
# ---------------------------------------------------------------------------

def test_challenge_leaderboard(client_and_session):
    """Test 12: Leaderboard orders participants by saved_emission DESC."""
    _, session = client_and_session

    # User 1 saves more (big baseline, low challenge)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=30.0)
    join_challenge(challenge_id=1, user_id=1, db=session)
    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=5.0)

    # User 2 saves less
    _add_car_activities(session, user_id=2, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=10.0)
    join_challenge(challenge_id=1, user_id=2, db=session)
    _add_car_activities(session, user_id=2, period_start=date(2026, 9, 20), period_end=date(2026, 9, 26), km_per_day=8.0)

    lb = get_challenge_leaderboard(challenge_id=1, db=session)
    items = lb["leaderboard"]
    assert len(items) == 2
    # User 1 should be rank 1 (higher savings)
    assert items[0]["user_id"] == 1
    assert items[0]["rank"] == 1
    assert items[1]["user_id"] == 2
    assert items[1]["rank"] == 2
    assert items[0]["saved_emission"] > items[1]["saved_emission"]


def test_challenge_leaderboard_api(client_and_session):
    """Test 12b: GET /api/challenges/{id}/leaderboard returns correct response."""
    client, session = client_and_session

    _add_car_activities(session, user_id=1, period_start=date(2026, 9, 13), period_end=date(2026, 9, 19), km_per_day=20.0)
    client.post("/api/challenges/1/join", json={"user_id": 1})

    resp = client.get("/api/challenges/1/leaderboard")
    assert resp.status_code == 200
    data = resp.json()
    assert data["challenge_id"] == 1
    assert "leaderboard" in data


# ---------------------------------------------------------------------------
# Test 13: Invalid challenge ID
# ---------------------------------------------------------------------------

def test_invalid_challenge_id_join(client_and_session):
    """Test 13a: Joining non-existent challenge returns 404."""
    client, _ = client_and_session
    resp = client.post("/api/challenges/999/join", json={"user_id": 1})
    assert resp.status_code == 404


def test_invalid_challenge_id_progress(client_and_session):
    """Test 13b: Progress for non-existent challenge returns 404."""
    client, _ = client_and_session
    resp = client.get("/api/challenges/999/progress?user_id=1")
    assert resp.status_code == 404


def test_invalid_challenge_id_summary(client_and_session):
    """Test 13c: Summary for non-existent challenge returns 404."""
    client, _ = client_and_session
    resp = client.get("/api/challenges/999/summary")
    assert resp.status_code == 404


def test_invalid_challenge_id_leaderboard(client_and_session):
    """Test 13d: Leaderboard for non-existent challenge returns 404."""
    client, _ = client_and_session
    resp = client.get("/api/challenges/999/leaderboard")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Test 14: Invalid user ID
# ---------------------------------------------------------------------------

def test_invalid_user_id_join(client_and_session):
    """Test 14a: Joining with non-existent user returns 404."""
    client, _ = client_and_session
    resp = client.post("/api/challenges/1/join", json={"user_id": 999})
    assert resp.status_code == 404


def test_invalid_user_id_progress(client_and_session):
    """Test 14b: Progress for non-existent user returns 404."""
    client, _ = client_and_session
    resp = client.get("/api/challenges/1/progress?user_id=999")
    assert resp.status_code == 404


# ---------------------------------------------------------------------------
# Additional edge-case tests
# ---------------------------------------------------------------------------

def test_join_completed_challenge_rejected(client_and_session):
    """Joining a completed challenge returns 400."""
    client, _ = client_and_session
    resp = client.post("/api/challenges/3/join", json={"user_id": 1})
    assert resp.status_code == 400


def test_progress_not_joined(client_and_session):
    """Querying progress without joining returns 404."""
    client, _ = client_and_session
    resp = client.get("/api/challenges/1/progress?user_id=1")
    assert resp.status_code == 404


def test_join_upcoming_challenge_allowed(client_and_session):
    """Joining an upcoming challenge is allowed."""
    client, _ = client_and_session
    resp = client.post("/api/challenges/2/join", json={"user_id": 1})
    assert resp.status_code == 201
    data = resp.json()
    assert data["status"] == "joined"
