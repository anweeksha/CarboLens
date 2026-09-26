"""Campus analytics HTTP router."""

from __future__ import annotations

from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.campus import (
    CampusOverviewResponse,
    CampusTrendResponse,
    DepartmentAnalyticsResponse,
    HostelAnalyticsResponse,
)
from app.services.campus_engine import (
    get_campus_overview,
    get_campus_trend,
    get_department_analytics,
    get_hostel_analytics,
)
from app.services.sustainability_report_service import (
    generate_campus_sustainability_report_pdf as generate_report_bytes,
)

router = APIRouter(prefix="/campus", tags=["campus"])


def generate_campus_sustainability_report_pdf(start_date: date, end_date: date, db: Session) -> bytes:
    """Generate a campus sustainability report PDF using the project's real analytics data."""
    return generate_report_bytes(start_date=start_date, end_date=end_date, db=db)


@router.get("/overview", response_model=CampusOverviewResponse, summary="Get campus-wide carbon overview")
def get_overview_endpoint(
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve campus-wide total emissions, active user count, average per active user, and category breakdown."""
    return get_campus_overview(month=month, year=year, db=db)


@router.get("/trend", response_model=CampusTrendResponse, summary="Get campus-wide monthly trend")
def get_trend_endpoint(
    start_date: date | None = Query(default=None, description="Start date filter (inclusive)"),
    end_date: date | None = Query(default=None, description="End date filter (inclusive)"),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve chronological campus-wide monthly emission totals."""
    return get_campus_trend(start_date=start_date, end_date=end_date, db=db)


@router.get("/departments", response_model=DepartmentAnalyticsResponse, summary="Get department analytics")
def get_departments_endpoint(
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve department population, active users, total emissions, per-active-user average, and category breakdown."""
    return get_department_analytics(month=month, year=year, db=db)


@router.get("/hostels", response_model=HostelAnalyticsResponse, summary="Get hostel analytics")
def get_hostels_endpoint(
    month: int | None = Query(default=None, ge=1, le=12, description="Filter by month (1-12)"),
    year: int | None = Query(default=None, ge=2000, le=2100, description="Filter by year (YYYY)"),
    db: Session = Depends(get_db),
) -> dict:
    """Retrieve hostel population, active users, total emissions, per-active-user average, and category breakdown."""
    return get_hostel_analytics(month=month, year=year, db=db)


@router.get(
    "/report/pdf",
    summary="Generate a campus sustainability PDF report for a date range",
    response_class=Response,
)
def get_campus_report_pdf(
    start_date: date = Query(..., description="Start date for the reporting period"),
    end_date: date = Query(..., description="End date for the reporting period"),
    db: Session = Depends(get_db),
) -> Response:
    """Generate a downloadable PDF report using real campus analytics and activity data."""
    if start_date > end_date:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="end_date must be on or after start_date.",
        )

    try:
        pdf_bytes = generate_campus_sustainability_report_pdf(start_date=start_date, end_date=end_date, db=db)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc
    except Exception as exc:  # pragma: no cover - defensive guard for runtime failures
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Report generation failed: {exc}",
        ) from exc

    filename = (
        f"carbonlens-campus-sustainability-report-{start_date.isoformat()}-to-{end_date.isoformat()}.pdf"
    )
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
