"""Emission factor lookup service."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.emission_factor import EmissionFactor
from app.services.exceptions import (
    AmbiguousEmissionFactorError,
    EmissionFactorNotFoundError,
    UnitMismatchError,
)

# Unit category grouping for unit compatibility
UNIT_GROUPS: dict[str, str] = {
    "km": "distance",
    "kilometer": "distance",
    "kilometers": "distance",
    "kms": "distance",
    "passenger_km": "distance",
    "passenger_kilometer": "distance",
    "passenger_kilometers": "distance",
    "pkm": "distance",
    "kwh": "energy",
    "kilowatt_hour": "energy",
    "kilowatt_hours": "energy",
    "kg": "mass",
    "kilogram": "mass",
    "kilograms": "mass",
    "kgs": "mass",
    "meal": "count",
    "meals": "count",
}


def normalize_unit(unit: str) -> str:
    cleaned = unit.strip().lower()
    return UNIT_GROUPS.get(cleaned, cleaned)


def are_units_compatible(unit1: str, unit2: str) -> bool:
    u1 = normalize_unit(unit1)
    u2 = normalize_unit(unit2)
    return u1 == u2


def get_emission_factor(
    db: Session,
    category: str,
    activity_type: str,
    unit: str,
    region: str = "global",
) -> EmissionFactor:
    """Lookup an emission factor by category, activity_type, unit, and region.

    Raises EmissionFactorNotFoundError if no factor exists for the category and type.
    Raises UnitMismatchError if a factor exists but for an incompatible unit group.
    Raises AmbiguousEmissionFactorError if conflicting factors exist for the same year.
    """
    clean_category = category.strip().lower()
    clean_type = activity_type.strip().lower()
    clean_region = region.strip().lower()

    # Step 1: Check if any emission factor exists for category + activity_type
    stmt_any = select(EmissionFactor).where(
        EmissionFactor.category.ilike(clean_category),
        EmissionFactor.activity_type.ilike(clean_type),
    )
    existing_factors = list(db.scalars(stmt_any).all())

    if not existing_factors:
        raise EmissionFactorNotFoundError(
            f"No emission factor found for category '{category}' and activity_type '{activity_type}'."
        )

    # Step 2: Filter by unit compatibility
    unit_matched_factors = [
        f for f in existing_factors if are_units_compatible(f.unit, unit)
    ]

    if not unit_matched_factors:
        supported_units = sorted(list({f.unit for f in existing_factors}))
        raise UnitMismatchError(
            f"Unit '{unit}' is incompatible with emission factor for '{category}/{activity_type}'. "
            f"Supported unit(s): {', '.join(supported_units)}."
        )

    # Step 3: Filter by region (exact match first, then fallback to 'global' / available)
    region_matched = [
        f for f in unit_matched_factors if f.region.strip().lower() == clean_region
    ]

    if not region_matched:
        # Fallback to 'global' region if region-specific factor is not found
        region_matched = [
            f for f in unit_matched_factors if f.region.strip().lower() == "global"
        ]

    if not region_matched:
        # If still not found, take whatever region factor is available
        region_matched = unit_matched_factors

    # Step 4: Sort by source_year descending to pick the most recent published factor
    region_matched.sort(key=lambda x: x.source_year, reverse=True)

    # Check for ambiguity if multiple factors exist for the latest source_year with different values
    latest_year = region_matched[0].source_year
    latest_year_factors = [f for f in region_matched if f.source_year == latest_year]

    distinct_values = {float(f.factor) for f in latest_year_factors}
    if len(distinct_values) > 1:
        raise AmbiguousEmissionFactorError(
            f"Multiple conflicting emission factors found for '{category}/{activity_type}' in year {latest_year}."
        )

    return region_matched[0]
