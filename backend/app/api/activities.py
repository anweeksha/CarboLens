"""Activity logging and retrieval API endpoints."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityCreate, ActivityResponse
from app.services.carbon_engine import calculate_emission
from app.services.exceptions import (
    EmissionFactorNotFoundError,
    InvalidQuantityError,
    UnitMismatchError,
    UserNotFoundError,
)

router = APIRouter(prefix="/activities", tags=["activities"])


@router.post("", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED, summary="Log a carbon activity")
def create_activity(
    payload: ActivityCreate,
    db: Session = Depends(get_db),
) -> Activity:
    """Log an individual carbon activity, calculate emissions, and preserve historical factor metadata."""
    # Verify user exists (if user doesn't exist, create demo user for user_id=1 if initial run, else raise 404)
    user = db.get(User, payload.user_id)
    if not user:
        if payload.user_id == 1:
            user = User(
                id=1,
                name="Demo CarbonLens User",
                email="demo@carbonlens.org",
                user_type="student",
            )
            db.add(user)
            db.commit()
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"User with ID {payload.user_id} not found.",
            )

    try:
        calc_result = calculate_emission(
            category=payload.category,
            activity_type=payload.activity_type,
            quantity=payload.quantity,
            unit=payload.unit,
            db=db,
            region=payload.region,
        )
    except InvalidQuantityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except UnitMismatchError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except EmissionFactorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )

    # Persist activity with calculated emission and immutable historical factor references
    activity = Activity(
        user_id=payload.user_id,
        category=calc_result.category,
        activity_type=calc_result.activity_type,
        quantity=payload.quantity,
        unit=payload.unit,
        activity_date=payload.activity_date,
        emission=calc_result.emission,
        emission_factor_used=calc_result.emission_factor,
        emission_factor_source=f"{calc_result.factor_source} ({calc_result.factor_source_year})",
        activity_metadata=payload.activity_metadata,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


@router.get("", response_model=list[ActivityResponse], summary="List logged activities")
def list_activities(
    user_id: int | None = Query(default=None, description="Filter activities by user ID"),
    category: str | None = Query(default=None, description="Filter activities by category"),
    activity_type: str | None = Query(default=None, description="Filter activities by activity type"),
    start_date: date | None = Query(default=None, description="Start date filter (inclusive)"),
    end_date: date | None = Query(default=None, description="End date filter (inclusive)"),
    db: Session = Depends(get_db),
) -> list[Activity]:
    """Retrieve logged activities with optional filtering by user, category, type, and date range."""
    stmt = select(Activity)

    if user_id is not None:
        stmt = stmt.where(Activity.user_id == user_id)
    if category:
        stmt = stmt.where(Activity.category.ilike(f"%{category.strip()}%"))
    if activity_type:
        stmt = stmt.where(Activity.activity_type.ilike(f"%{activity_type.strip()}%"))
    if start_date:
        stmt = stmt.where(Activity.activity_date >= start_date)
    if end_date:
        stmt = stmt.where(Activity.activity_date <= end_date)

    stmt = stmt.order_by(Activity.activity_date.desc(), Activity.created_at.desc())
    return list(db.scalars(stmt).all())


@router.get("/{activity_id}", response_model=ActivityResponse, summary="Get activity by ID")
def get_activity_by_id(
    activity_id: int,
    db: Session = Depends(get_db),
) -> Activity:
    """Retrieve details of a logged activity by its ID."""
    activity = db.get(Activity, activity_id)
    if not activity:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Activity with ID {activity_id} not found.",
        )
    return activity
