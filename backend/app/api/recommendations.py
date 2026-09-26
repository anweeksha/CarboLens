"""Personalized recommendations API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.recommendation import RecommendationResponse
from app.services.exceptions import UserNotFoundError
from app.services.recommendation_engine import generate_recommendations

router = APIRouter(prefix="/users", tags=["recommendations"])


@router.get(
    "/{user_id}/recommendations",
    response_model=RecommendationResponse,
    summary="Get personalized carbon reduction recommendations",
)
def get_recommendations(
    user_id: int,
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    limit: int = Query(default=10, ge=1, le=50, description="Max number of recommendations to return"),
    db: Session = Depends(get_db),
) -> dict:
    """Generate personalized, quantity-driven carbon reduction recommendations for a user sorted by potential CO2e savings."""
    try:
        return generate_recommendations(
            user_id=user_id,
            month=month,
            year=year,
            db=db,
            limit=limit,
        )
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
