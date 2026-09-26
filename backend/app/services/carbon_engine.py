"""Carbon calculation engine service.

Core calculation: CO2e = quantity * emission_factor
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.services.emission_factor_service import get_emission_factor
from app.services.exceptions import InvalidQuantityError

ALLOWED_CATEGORIES = {"travel", "electricity", "food", "waste"}


@dataclass
class CarbonCalculationResult:
    category: str
    activity_type: str
    quantity: float
    unit: str
    emission_factor: float
    emission: float
    factor_source: str
    factor_source_year: int
    region: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "activity_type": self.activity_type,
            "quantity": self.quantity,
            "unit": self.unit,
            "emission_factor": round(self.emission_factor, 8),
            "emission": round(self.emission, 4),
            "factor_source": self.factor_source,
            "factor_source_year": self.factor_source_year,
            "region": self.region,
        }


def calculate_emission(
    category: str,
    activity_type: str,
    quantity: float,
    unit: str,
    db: Session,
    region: str = "global",
) -> CarbonCalculationResult:
    """Calculate carbon emissions (kg CO2e) for a given activity.

    1. Validates quantity (> 0).
    2. Finds the matching emission factor.
    3. Validates unit compatibility.
    4. Calculates CO2e = quantity * emission_factor.
    5. Returns result containing emission value, factor, and source reference.
    """
    clean_category = category.strip().lower()
    clean_type = activity_type.strip().lower()

    if clean_category not in ALLOWED_CATEGORIES:
        # We allow custom category lookup in factor DB if available, but log/validate standard
        pass

    if quantity <= 0:
        raise InvalidQuantityError(
            f"Quantity must be greater than 0. Received: {quantity}"
        )

    # Lookup emission factor from database
    factor_record = get_emission_factor(
        db=db,
        category=clean_category,
        activity_type=clean_type,
        unit=unit,
        region=region,
    )

    factor_value = float(factor_record.factor)

    # Calculate CO2e without excessive intermediate rounding
    co2e_emission = quantity * factor_value

    return CarbonCalculationResult(
        category=clean_category,
        activity_type=clean_type,
        quantity=float(quantity),
        unit=unit.strip(),
        emission_factor=factor_value,
        emission=co2e_emission,
        factor_source=factor_record.source,
        factor_source_year=factor_record.source_year,
        region=factor_record.region,
    )
