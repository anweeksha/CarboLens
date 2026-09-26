"""Personal carbon footprint, category breakdown, monthly trend, and campus benchmark API endpoints."""

from __future__ import annotations

from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.activity import Activity
from app.models.user import User
from app.schemas.campus import UserBenchmarkResponse
from app.schemas.footprint import (
    CategoryBreakdownResponse,
    FootprintResponse,
    MonthlyTrendItem,
    MonthlyTrendResponse,
)
from app.services.campus_engine import get_user_benchmark
from app.services.exceptions import UserNotFoundError

router = APIRouter(prefix="/users", tags=["footprint"])


@router.get("/{user_id}/footprint", response_model=FootprintResponse, summary="Get personal monthly carbon footprint")
def get_user_footprint(
    user_id: int,
    month: int | None = Query(default=None, ge=1, le=12, description="Month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Year (YYYY)"),
    db: Session = Depends(get_db),
) -> FootprintResponse:
    """Retrieve a user's total carbon emissions (kgCO2e) for a specified month and year."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    now = datetime.now()
    req_month = month if month is not None else now.month
    req_year = year if year is not None else now.year

    stmt = select(func.coalesce(func.sum(Activity.emission), 0.0)).where(
        Activity.user_id == user_id,
        extract("year", Activity.activity_date) == req_year,
        extract("month", Activity.activity_date) == req_month,
    )
    total_emission = float(db.scalar(stmt) or 0.0)

    return FootprintResponse(
        user_id=user_id,
        month=req_month,
        year=req_year,
        total_emission=round(total_emission, 4),
        unit="kgCO2e",
    )


@router.get("/{user_id}/breakdown", response_model=CategoryBreakdownResponse, summary="Get footprint category breakdown")
def get_user_breakdown(
    user_id: int,
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> CategoryBreakdownResponse:
    """Retrieve category-wise emissions breakdown (travel, electricity, food, waste) for a user."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    stmt = select(Activity.category, func.coalesce(func.sum(Activity.emission), 0.0)).where(
        Activity.user_id == user_id
    )

    if year is not None:
        stmt = stmt.where(extract("year", Activity.activity_date) == year)
    if month is not None:
        stmt = stmt.where(extract("month", Activity.activity_date) == month)

    stmt = stmt.group_by(Activity.category)

    rows = db.execute(stmt).all()
    breakdown_dict = {cat.lower(): float(val) for cat, val in rows}

    return CategoryBreakdownResponse(
        travel=round(breakdown_dict.get("travel", 0.0), 4),
        electricity=round(breakdown_dict.get("electricity", 0.0), 4),
        food=round(breakdown_dict.get("food", 0.0), 4),
        waste=round(breakdown_dict.get("waste", 0.0), 4),
    )


@router.get("/{user_id}/trend", response_model=MonthlyTrendResponse, summary="Get monthly footprint trend")
def get_user_trend(
    user_id: int,
    start_date: date | None = Query(default=None, description="Start date filter"),
    end_date: date | None = Query(default=None, description="End date filter"),
    db: Session = Depends(get_db),
) -> MonthlyTrendResponse:
    """Retrieve monthly emission totals in chronological order for trend analysis."""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with ID {user_id} not found.",
        )

    stmt = select(
        extract("year", Activity.activity_date).label("yr"),
        extract("month", Activity.activity_date).label("mo"),
        func.coalesce(func.sum(Activity.emission), 0.0).label("tot"),
    ).where(Activity.user_id == user_id)

    if start_date:
        stmt = stmt.where(Activity.activity_date >= start_date)
    if end_date:
        stmt = stmt.where(Activity.activity_date <= end_date)

    stmt = stmt.group_by("yr", "mo").order_by("yr", "mo")

    results = db.execute(stmt).all()
    trend_items = []
    for yr, mo, tot in results:
        month_str = f"{int(yr):04d}-{int(mo):02d}"
        trend_items.append(MonthlyTrendItem(month=month_str, emission=round(float(tot), 4)))

    return MonthlyTrendResponse(user_id=user_id, trend=trend_items)


@router.get("/{user_id}/benchmark", response_model=UserBenchmarkResponse, summary="Get user benchmark against campus average")
def get_user_benchmark_endpoint(
    user_id: int,
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> dict:
    """Compare a user's carbon footprint against the database-derived campus average per active user."""
    try:
        return get_user_benchmark(user_id=user_id, month=month, year=year, db=db)
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
