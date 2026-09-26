"""Challenge Engine — baseline, current emission, savings, and completion calculations.

All challenge business logic lives here.  Route handlers delegate to these functions.
"""

from __future__ import annotations

from datetime import date, timedelta
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.challenge import Challenge
from app.models.challenge_progress import ChallengeProgress
from app.models.user import User


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _challenge_status(challenge: Challenge, today: date | None = None) -> str:
    """Derive challenge status from its date range."""
    today = today or date.today()
    if today < challenge.start_date:
        return "upcoming"
    if today > challenge.end_date:
        return "completed"
    return "active"


def _challenge_duration_days(challenge: Challenge) -> int:
    """Number of days in the challenge (inclusive)."""
    return (challenge.end_date - challenge.start_date).days + 1


def _baseline_period(challenge: Challenge) -> tuple[date, date]:
    """Return (start, end) for the baseline period immediately preceding the challenge."""
    duration = _challenge_duration_days(challenge)
    baseline_end = challenge.start_date - timedelta(days=1)
    baseline_start = baseline_end - timedelta(days=duration - 1)
    return baseline_start, baseline_end


def _query_period_emission_and_quantity(
    db: Session,
    user_id: int,
    category: str,
    activity_type: str | None,
    period_start: date,
    period_end: date,
) -> tuple[float, float]:
    """Sum emission and quantity for a user's activities matching challenge category/type within a date range."""
    stmt = select(
        func.coalesce(func.sum(Activity.emission), 0.0),
        func.coalesce(func.sum(Activity.quantity), 0.0),
    ).where(
        Activity.user_id == user_id,
        Activity.category == category,
        Activity.activity_date >= period_start,
        Activity.activity_date <= period_end,
    )
    if activity_type:
        stmt = stmt.where(Activity.activity_type == activity_type)

    row = db.execute(stmt).one()
    return float(row[0]), float(row[1])


def _compute_completion_percentage(
    baseline_quantity: float,
    current_quantity: float,
    target: float,
) -> float:
    """Compute completion % based on quantity reduction relative to challenge target.

    completion = clamp(0, (baseline_quantity - current_quantity) / target * 100, 100)
    """
    if target <= 0:
        return 0.0
    reduction = baseline_quantity - current_quantity
    pct = (reduction / target) * 100.0
    return max(0.0, min(100.0, pct))


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def list_challenges(
    db: Session,
    status: str | None = None,
) -> dict[str, Any]:
    """Return challenges, optionally filtered by status (active/upcoming/completed)."""
    today = date.today()
    stmt = select(Challenge)

    if status == "active":
        stmt = stmt.where(Challenge.start_date <= today, Challenge.end_date >= today)
    elif status == "upcoming":
        stmt = stmt.where(Challenge.start_date > today)
    elif status == "completed":
        stmt = stmt.where(Challenge.end_date < today)

    challenges = db.scalars(stmt.order_by(Challenge.start_date)).all()
    items = []
    for c in challenges:
        items.append({
            "id": c.id,
            "name": c.name,
            "description": c.description,
            "category": c.category,
            "activity_type": c.activity_type,
            "start_date": c.start_date,
            "end_date": c.end_date,
            "target": float(c.target),
            "target_unit": c.target_unit,
            "status": _challenge_status(c, today),
        })
    return {"challenges": items, "count": len(items)}


def join_challenge(
    challenge_id: int,
    user_id: int,
    db: Session,
) -> dict[str, Any]:
    """Join a user to a challenge, computing baseline where possible."""
    # 1. Verify challenge exists
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise ChallengeNotFoundError(f"Challenge {challenge_id} not found")

    # 2. Verify user exists
    user = db.get(User, user_id)
    if not user:
        raise ChallengeUserNotFoundError(f"User {user_id} not found")

    # 3. Verify challenge is joinable (active or upcoming)
    status = _challenge_status(challenge)
    if status == "completed":
        raise ChallengeNotJoinableError(f"Challenge {challenge_id} has already ended")

    # 4. Check duplicate join
    existing = db.scalar(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge_id,
            ChallengeProgress.user_id == user_id,
        )
    )
    if existing:
        raise ChallengeDuplicateJoinError(
            f"User {user_id} has already joined challenge {challenge_id}"
        )

    # 5. Calculate baseline
    baseline_start, baseline_end = _baseline_period(challenge)
    baseline_emission, baseline_quantity = _query_period_emission_and_quantity(
        db=db,
        user_id=user_id,
        category=challenge.category,
        activity_type=challenge.activity_type,
        period_start=baseline_start,
        period_end=baseline_end,
    )

    # Determine baseline status
    if baseline_emission == 0.0 and baseline_quantity == 0.0:
        baseline_status = "insufficient_baseline_data"
    else:
        baseline_status = "calculated"

    # 6. Create ChallengeProgress
    progress = ChallengeProgress(
        challenge_id=challenge_id,
        user_id=user_id,
        baseline_emission=baseline_emission,
        baseline_quantity=baseline_quantity,
        baseline_status=baseline_status,
        current_emission=0.0,
        current_quantity=0.0,
        saved_emission=0.0,
        completion_percentage=0.0,
        status="joined",
    )
    db.add(progress)
    db.commit()
    db.refresh(progress)

    return {
        "challenge_id": challenge_id,
        "user_id": user_id,
        "status": "joined",
        "baseline_emission": float(progress.baseline_emission),
        "baseline_status": baseline_status,
    }


def get_challenge_progress(
    challenge_id: int,
    user_id: int,
    db: Session,
) -> dict[str, Any]:
    """Compute real-time progress for a user in a challenge."""
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise ChallengeNotFoundError(f"Challenge {challenge_id} not found")

    user = db.get(User, user_id)
    if not user:
        raise ChallengeUserNotFoundError(f"User {user_id} not found")

    progress = db.scalar(
        select(ChallengeProgress).where(
            ChallengeProgress.challenge_id == challenge_id,
            ChallengeProgress.user_id == user_id,
        )
    )
    if not progress:
        raise ChallengeNotJoinedError(
            f"User {user_id} has not joined challenge {challenge_id}"
        )

    # Re-compute current emissions from actual activity data during challenge period
    current_emission, current_quantity = _query_period_emission_and_quantity(
        db=db,
        user_id=user_id,
        category=challenge.category,
        activity_type=challenge.activity_type,
        period_start=challenge.start_date,
        period_end=challenge.end_date,
    )

    baseline_emission = float(progress.baseline_emission)
    baseline_quantity = float(progress.baseline_quantity)

    # saved = max(0, baseline - current) for display
    raw_saved = baseline_emission - current_emission
    saved_emission = max(0.0, raw_saved)

    # Completion percentage based on quantity reduction vs target
    completion_pct = _compute_completion_percentage(
        baseline_quantity=baseline_quantity,
        current_quantity=current_quantity,
        target=float(challenge.target),
    )

    # Determine status
    challenge_status = _challenge_status(challenge)
    if completion_pct >= 100.0:
        progress_status = "completed"
    elif challenge_status == "completed":
        progress_status = "challenge_ended"
    else:
        progress_status = "in_progress"

    # Persist updated values
    progress.current_emission = current_emission
    progress.current_quantity = current_quantity
    progress.saved_emission = saved_emission
    progress.completion_percentage = completion_pct
    progress.status = progress_status
    if progress_status == "completed" and progress.completed_at is None:
        from datetime import datetime, timezone
        progress.completed_at = datetime.now(timezone.utc)
    db.commit()

    return {
        "challenge_id": challenge_id,
        "user_id": user_id,
        "baseline_emission": round(baseline_emission, 4),
        "baseline_status": progress.baseline_status,
        "current_emission": round(current_emission, 4),
        "saved_emission": round(saved_emission, 4),
        "completion_percentage": round(completion_pct, 2),
        "status": progress_status,
    }


def get_challenge_summary(
    challenge_id: int,
    db: Session,
) -> dict[str, Any]:
    """Aggregate summary across all participants of a challenge."""
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise ChallengeNotFoundError(f"Challenge {challenge_id} not found")

    # Get all progress records, refreshing current emissions for each participant
    progress_records = db.scalars(
        select(ChallengeProgress).where(ChallengeProgress.challenge_id == challenge_id)
    ).all()

    # Refresh each participant's current emissions from activity data
    for p in progress_records:
        current_emission, current_quantity = _query_period_emission_and_quantity(
            db=db,
            user_id=p.user_id,
            category=challenge.category,
            activity_type=challenge.activity_type,
            period_start=challenge.start_date,
            period_end=challenge.end_date,
        )
        p.current_emission = current_emission
        p.current_quantity = current_quantity
        raw_saved = float(p.baseline_emission) - current_emission
        p.saved_emission = max(0.0, raw_saved)
        p.completion_percentage = _compute_completion_percentage(
            baseline_quantity=float(p.baseline_quantity),
            current_quantity=current_quantity,
            target=float(challenge.target),
        )
        if p.completion_percentage >= 100.0:
            p.status = "completed"
    db.commit()

    participants = len(progress_records)
    completed = sum(1 for p in progress_records if p.status == "completed")
    total_baseline = sum(float(p.baseline_emission) for p in progress_records)
    total_current = sum(float(p.current_emission) for p in progress_records)
    total_saved = sum(float(p.saved_emission) for p in progress_records)
    avg_saved = total_saved / participants if participants > 0 else 0.0

    return {
        "challenge_id": challenge_id,
        "name": challenge.name,
        "participants": participants,
        "completed": completed,
        "total_baseline_emission": round(total_baseline, 4),
        "total_current_emission": round(total_current, 4),
        "total_saved_emission": round(total_saved, 4),
        "average_saved_per_participant": round(avg_saved, 4),
    }


def get_challenge_leaderboard(
    challenge_id: int,
    db: Session,
) -> dict[str, Any]:
    """Return participants ranked by saved_emission DESC."""
    challenge = db.get(Challenge, challenge_id)
    if not challenge:
        raise ChallengeNotFoundError(f"Challenge {challenge_id} not found")

    # Re-compute for all participants
    progress_records = db.scalars(
        select(ChallengeProgress).where(ChallengeProgress.challenge_id == challenge_id)
    ).all()

    for p in progress_records:
        current_emission, current_quantity = _query_period_emission_and_quantity(
            db=db,
            user_id=p.user_id,
            category=challenge.category,
            activity_type=challenge.activity_type,
            period_start=challenge.start_date,
            period_end=challenge.end_date,
        )
        p.current_emission = current_emission
        p.current_quantity = current_quantity
        raw_saved = float(p.baseline_emission) - current_emission
        p.saved_emission = max(0.0, raw_saved)
        p.completion_percentage = _compute_completion_percentage(
            baseline_quantity=float(p.baseline_quantity),
            current_quantity=current_quantity,
            target=float(challenge.target),
        )
    db.commit()

    # Sort by saved_emission DESC
    sorted_records = sorted(progress_records, key=lambda p: float(p.saved_emission), reverse=True)

    leaderboard = []
    for rank, p in enumerate(sorted_records, start=1):
        user = db.get(User, p.user_id)
        leaderboard.append({
            "rank": rank,
            "user_id": p.user_id,
            "user_name": user.name if user else "Unknown",
            "saved_emission": round(float(p.saved_emission), 4),
            "completion_percentage": round(float(p.completion_percentage), 2),
        })

    return {
        "challenge_id": challenge_id,
        "leaderboard": leaderboard,
    }


# ---------------------------------------------------------------------------
# Domain Exceptions
# ---------------------------------------------------------------------------

class ChallengeEngineError(Exception):
    """Base exception for challenge engine."""


class ChallengeNotFoundError(ChallengeEngineError):
    """Raised when the requested challenge does not exist."""


class ChallengeUserNotFoundError(ChallengeEngineError):
    """Raised when the requested user does not exist."""


class ChallengeNotJoinableError(ChallengeEngineError):
    """Raised when a challenge cannot be joined (e.g. already completed)."""


class ChallengeDuplicateJoinError(ChallengeEngineError):
    """Raised when a user tries to join a challenge they already joined."""


class ChallengeNotJoinedError(ChallengeEngineError):
    """Raised when querying progress for a user who hasn't joined the challenge."""
