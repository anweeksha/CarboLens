"""Leaderboard aggregation API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.campus import LeaderboardResponse
from app.services.campus_engine import get_leaderboard

router = APIRouter(tags=["leaderboard"])


@router.get(
    "/leaderboard",
    response_model=LeaderboardResponse,
    summary="Get department or hostel carbon leaderboard",
)
def get_leaderboard_endpoint(
    type: str = Query(default="department", description="Leaderboard entity type: 'department' or 'hostel'"),
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve department or hostel leaderboard entries distinguishing total emissions, per-active-user emissions, population, and period change."""
    try:
        return get_leaderboard(entity_type=type, month=month, year=year, db=db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
