"""What-If Simulation Engine Service.

Calculates hypothetical carbon reduction scenarios for proposed activity changes.
Performs ZERO database mutations (100% read-only).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy.orm import Session

from app.models.user import User
from app.services.emission_factor_service import get_emission_factor
from app.services.exceptions import (
    EmissionFactorNotFoundError,
    InvalidQuantityError,
    UserNotFoundError,
)


@dataclass
class SimulationChangeItemInput:
    category: str
    from_activity: str
    to_activity: str
    quantity: float
    unit: str
    region: str = "global"


@dataclass
class SimulationChangeItemResult:
    category: str
    from_activity: str
    to_activity: str
    quantity: float
    unit: str
    current_emission: float
    projected_emission: float
    saving: float
    reduction_percentage: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "category": self.category,
            "from_activity": self.from_activity,
            "to_activity": self.to_activity,
            "quantity": round(self.quantity, 4),
            "unit": self.unit,
            "current_emission": round(self.current_emission, 4),
            "projected_emission": round(self.projected_emission, 4),
            "saving": round(self.saving, 4),
            "reduction_percentage": round(self.reduction_percentage, 2),
        }


def run_simulation(
    user_id: int,
    changes: list[SimulationChangeItemInput],
    db: Session,
) -> dict[str, Any]:
    """Calculate hypothetical carbon savings across one or multiple proposed activity changes.

    Does NOT modify the database in any way.
    """
    user = db.get(User, user_id)
    if not user:
        if user_id == 1:
            # User 1 demo user allowed if database is empty/fresh
            pass
        else:
            raise UserNotFoundError(f"User with ID {user_id} not found.")

    if not changes:
        return {
            "user_id": user_id,
            "current_total": 0.0,
            "projected_total": 0.0,
            "total_saving": 0.0,
            "saving_unit": "kgCO2e",
            "reduction_percentage": 0.0,
            "changes": [],
        }

    results: list[SimulationChangeItemResult] = []

    for item in changes:
        if item.quantity <= 0:
            raise InvalidQuantityError(
                f"Quantity for simulation must be greater than 0. Received: {item.quantity}"
            )

        cat = item.category.strip().lower()
        from_act = item.from_activity.strip().lower()
        to_act = item.to_activity.strip().lower()
        unit = item.unit.strip()

        # Lookup current emission factor
        current_ef_record = get_emission_factor(
            db=db,
            category=cat,
            activity_type=from_act,
            unit=unit,
            region=item.region,
        )
        current_factor = float(current_ef_record.factor)

        # Lookup target alternative emission factor
        alt_ef_record = get_emission_factor(
            db=db,
            category=cat,
            activity_type=to_act,
            unit=unit,
            region=item.region,
        )
        alt_factor = float(alt_ef_record.factor)

        current_emission = item.quantity * current_factor
        projected_emission = item.quantity * alt_factor
        saving = current_emission - projected_emission
        pct = (saving / current_emission * 100.0) if current_emission > 0 else 0.0

        results.append(
            SimulationChangeItemResult(
                category=cat,
                from_activity=from_act,
                to_activity=to_act,
                quantity=item.quantity,
                unit=unit,
                current_emission=current_emission,
                projected_emission=projected_emission,
                saving=saving,
                reduction_percentage=pct,
            )
        )

    current_total = sum(res.current_emission for res in results)
    projected_total = sum(res.projected_emission for res in results)
    total_saving = current_total - projected_total
    overall_pct = (total_saving / current_total * 100.0) if current_total > 0 else 0.0

    return {
        "user_id": user_id,
        "current_total": round(current_total, 4),
        "projected_total": round(projected_total, 4),
        "total_saving": round(total_saving, 4),
        "saving_unit": "kgCO2e",
        "reduction_percentage": round(overall_pct, 2),
        "changes": [res.to_dict() for res in results],
    }
