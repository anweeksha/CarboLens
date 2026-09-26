"""Emission factor management endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.emission_factor import EmissionFactor
from app.schemas.emission_factor import EmissionFactorCreate, EmissionFactorResponse

router = APIRouter(prefix="/emission-factors", tags=["emission-factors"])


@router.get("", response_model=list[EmissionFactorResponse], summary="List emission factors")
def list_emission_factors(
    category: str | None = Query(default=None, description="Filter by category"),
    activity_type: str | None = Query(default=None, description="Filter by activity type"),
    region: str | None = Query(default=None, description="Filter by region"),
    db: Session = Depends(get_db),
) -> list[EmissionFactor]:
    """Retrieve stored emission factors with optional category, activity_type, and region filtering."""
    stmt = select(EmissionFactor)
    if category:
        stmt = stmt.where(EmissionFactor.category.ilike(f"%{category.strip()}%"))
    if activity_type:
        stmt = stmt.where(EmissionFactor.activity_type.ilike(f"%{activity_type.strip()}%"))
    if region:
        stmt = stmt.where(EmissionFactor.region.ilike(f"%{region.strip()}%"))

    stmt = stmt.order_by(EmissionFactor.category, EmissionFactor.activity_type)
    return list(db.scalars(stmt).all())


@router.post("", response_model=EmissionFactorResponse, status_code=status.HTTP_201_CREATED, summary="Add emission factor")
def create_emission_factor(
    payload: EmissionFactorCreate,
    db: Session = Depends(get_db),
) -> EmissionFactor:
    """Add a new published emission factor record into the database."""
    factor = EmissionFactor(
        category=payload.category.strip().lower(),
        activity_type=payload.activity_type.strip().lower(),
        unit=payload.unit.strip(),
        factor=payload.factor,
        source=payload.source.strip(),
        source_year=payload.source_year,
        region=payload.region.strip().lower(),
    )
    db.add(factor)
    db.commit()
    db.refresh(factor)
    return factor


@router.get("/{factor_id}", response_model=EmissionFactorResponse, summary="Get emission factor by ID")
def get_emission_factor_by_id(
    factor_id: int,
    db: Session = Depends(get_db),
) -> EmissionFactor:
    """Retrieve details of a single emission factor by its ID."""
    factor = db.get(EmissionFactor, factor_id)
    if not factor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Emission factor with ID {factor_id} not found.",
        )
    return factor
