"""Challenge API router.

Endpoints:
- GET  /challenges                            — List challenges (filter by status)
- POST /challenges/{challenge_id}/join        — Join a challenge
- GET  /challenges/{challenge_id}/progress    — Get user progress
- GET  /challenges/{challenge_id}/summary     — Aggregated challenge summary
- GET  /challenges/{challenge_id}/leaderboard — Challenge-specific leaderboard
"""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.challenge import (
    ChallengeJoinRequest,
    ChallengeJoinResponse,
    ChallengeLeaderboardResponse,
    ChallengeListResponse,
    ChallengeProgressResponse,
    ChallengeSummaryResponse,
)
from app.services.challenge_engine import (
    ChallengeDuplicateJoinError,
    ChallengeNotFoundError,
    ChallengeNotJoinableError,
    ChallengeNotJoinedError,
    ChallengeUserNotFoundError,
    get_challenge_leaderboard,
    get_challenge_progress,
    get_challenge_summary,
    join_challenge,
    list_challenges,
)

router = APIRouter(tags=["challenges"])


# ---------------------------------------------------------------------------
# GET /challenges
# ---------------------------------------------------------------------------

@router.get(
    "/challenges",
    response_model=ChallengeListResponse,
    summary="List challenges with optional status filter",
)
def list_challenges_endpoint(
    status_filter: str | None = Query(
        default=None,
        alias="status",
        description="Filter: 'active', 'upcoming', or 'completed'",
    ),
    db: Session = Depends(get_db),
) -> dict:
    """Return challenges, optionally filtered by status."""
    if status_filter and status_filter not in ("active", "upcoming", "completed"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid status filter '{status_filter}'. Must be 'active', 'upcoming', or 'completed'.",
        )
    return list_challenges(db=db, status=status_filter)


# ---------------------------------------------------------------------------
# POST /challenges/{challenge_id}/join
# ---------------------------------------------------------------------------

@router.post(
    "/challenges/{challenge_id}/join",
    response_model=ChallengeJoinResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Join a challenge",
)
def join_challenge_endpoint(
    challenge_id: int,
    body: ChallengeJoinRequest,
    db: Session = Depends(get_db),
) -> dict:
    """Join a user to a challenge and compute baseline emissions."""
    try:
        return join_challenge(challenge_id=challenge_id, user_id=body.user_id, db=db)
    except ChallengeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Challenge {challenge_id} not found")
    except ChallengeUserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {body.user_id} not found")
    except ChallengeNotJoinableError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except ChallengeDuplicateJoinError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))


# ---------------------------------------------------------------------------
# GET /challenges/{challenge_id}/progress
# ---------------------------------------------------------------------------

@router.get(
    "/challenges/{challenge_id}/progress",
    response_model=ChallengeProgressResponse,
    summary="Get user progress in a challenge",
)
def get_progress_endpoint(
    challenge_id: int,
    user_id: int = Query(..., description="User ID"),
    db: Session = Depends(get_db),
) -> dict:
    """Return real-time challenge progress calculated from actual activity data."""
    try:
        return get_challenge_progress(challenge_id=challenge_id, user_id=user_id, db=db)
    except ChallengeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Challenge {challenge_id} not found")
    except ChallengeUserNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} not found")
    except ChallengeNotJoinedError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {user_id} has not joined challenge {challenge_id}")


# ---------------------------------------------------------------------------
# GET /challenges/{challenge_id}/summary
# ---------------------------------------------------------------------------

@router.get(
    "/challenges/{challenge_id}/summary",
    response_model=ChallengeSummaryResponse,
    summary="Aggregated challenge summary",
)
def get_summary_endpoint(
    challenge_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Return aggregated metrics across all challenge participants."""
    try:
        return get_challenge_summary(challenge_id=challenge_id, db=db)
    except ChallengeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Challenge {challenge_id} not found")


# ---------------------------------------------------------------------------
# GET /challenges/{challenge_id}/leaderboard
# ---------------------------------------------------------------------------

@router.get(
    "/challenges/{challenge_id}/leaderboard",
    response_model=ChallengeLeaderboardResponse,
    summary="Challenge participant leaderboard",
)
def get_leaderboard_endpoint(
    challenge_id: int,
    db: Session = Depends(get_db),
) -> dict:
    """Return participants ranked by CO2e saved (descending)."""
    try:
        return get_challenge_leaderboard(challenge_id=challenge_id, db=db)
    except ChallengeNotFoundError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Challenge {challenge_id} not found")
