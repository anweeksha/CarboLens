"""Personalized Recommendation Engine & Top Carbon Drivers Service."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from sqlalchemy import extract, func, select
from sqlalchemy.orm import Session

from app.models.activity import Activity
from app.models.user import User
from app.services.emission_factor_service import get_emission_factor
from app.services.exceptions import EmissionFactorNotFoundError, UserNotFoundError

# Reasonable alternative activity mappings per category & activity type
ALTERNATIVE_MAPPINGS: dict[str, dict[str, list[str]]] = {
    "travel": {
        "car": ["bus", "train", "cycling", "walking"],
        "motorcycle": ["bus", "cycling", "walking"],
        "flight_domestic": ["train", "bus"],
    },
    "food": {
        "non_vegetarian_meal": ["vegetarian_meal"],
    },
    "electricity": {
        "grid_electricity": ["solar_electricity", "renewable_electricity"],
    },
    "waste": {
        "plastic": ["recycled_plastic", "organic_waste"],
    },
}


@dataclass
class CarbonDriverItem:
    category: str
    activity_type: str
    emission: float


@dataclass
class RecommendationItemResult:
    title: str
    category: str
    current_activity: str
    alternative_activity: str
    quantity: float
    unit: str
    current_emission: float
    alternative_emission: float
    potential_saving: float
    saving_unit: str
    reduction_percentage: float

    def to_dict(self) -> dict[str, Any]:
        return {
            "title": self.title,
            "category": self.category,
            "current_activity": self.current_activity,
            "alternative_activity": self.alternative_activity,
            "quantity": round(self.quantity, 4),
            "unit": self.unit,
            "current_emission": round(self.current_emission, 4),
            "alternative_emission": round(self.alternative_emission, 4),
            "potential_saving": round(self.potential_saving, 4),
            "saving_unit": self.saving_unit,
            "reduction_percentage": round(self.reduction_percentage, 2),
        }


def get_top_carbon_drivers(
    user_id: int,
    month: int | None,
    year: int | None,
    db: Session,
    limit: int = 3,
) -> list[CarbonDriverItem]:
    """Retrieve top N activity types contributing most to a user's stored carbon footprint."""
    stmt = (
        select(
            Activity.category,
            Activity.activity_type,
            func.coalesce(func.sum(Activity.emission), 0.0).label("total_emission"),
        )
        .where(Activity.user_id == user_id)
        .group_by(Activity.category, Activity.activity_type)
        .order_by(func.sum(Activity.emission).desc())
    )

    if year is not None:
        stmt = stmt.where(extract("year", Activity.activity_date) == year)
    if month is not None:
        stmt = stmt.where(extract("month", Activity.activity_date) == month)

    rows = db.execute(stmt.limit(limit)).all()
    return [
        CarbonDriverItem(
            category=row.category,
            activity_type=row.activity_type,
            emission=round(float(row.total_emission), 4),
        )
        for row in rows
    ]


def generate_recommendations(
    user_id: int,
    month: int | None,
    year: int | None,
    db: Session,
    limit: int = 10,
) -> dict[str, Any]:
    """Generate personalized, quantity-based recommendations sorted by potential CO2e savings."""
    user = db.get(User, user_id)
    if not user:
        raise UserNotFoundError(f"User with ID {user_id} not found.")

    # Top carbon drivers based on actual stored emissions
    top_drivers = get_top_carbon_drivers(user_id=user_id, month=month, year=year, db=db, limit=3)

    # Aggregate user activities by (category, activity_type, unit) to avoid duplicates
    stmt = select(
        Activity.category,
        Activity.activity_type,
        Activity.unit,
        func.sum(Activity.quantity).label("total_quantity"),
        func.sum(Activity.emission).label("total_emission"),
    ).where(Activity.user_id == user_id)

    if year is not None:
        stmt = stmt.where(extract("year", Activity.activity_date) == year)
    if month is not None:
        stmt = stmt.where(extract("month", Activity.activity_date) == month)

    stmt = stmt.group_by(Activity.category, Activity.activity_type, Activity.unit)
    aggregated_activities = db.execute(stmt).all()

    recommendations: list[RecommendationItemResult] = []

    for row in aggregated_activities:
        cat = row.category.lower()
        act_type = row.activity_type.lower()
        unit = row.unit
        quantity = float(row.total_quantity)
        current_emission = float(row.total_emission)

        # Check mapped alternatives for this category & activity type
        alternatives = ALTERNATIVE_MAPPINGS.get(cat, {}).get(act_type, [])

        for alt_type in alternatives:
            try:
                # Look up alternative factor in DB
                alt_factor_record = get_emission_factor(
                    db=db,
                    category=cat,
                    activity_type=alt_type,
                    unit=unit,
                )
                alt_factor = float(alt_factor_record.factor)
            except EmissionFactorNotFoundError:
                # Do NOT invent or fabricate factors; skip if factor does not exist in DB
                continue
            except Exception:
                continue

            alt_emission = quantity * alt_factor
            potential_saving = current_emission - alt_emission

            # Only include recommendations with actual positive CO2e savings
            if potential_saving > 0:
                reduction_pct = (
                    (potential_saving / current_emission * 100) if current_emission > 0 else 0.0
                )
                title_str = f"Switch from {act_type.replace('_', ' ')} to {alt_type.replace('_', ' ')}"
                recommendations.append(
                    RecommendationItemResult(
                        title=title_str,
                        category=cat,
                        current_activity=act_type,
                        alternative_activity=alt_type,
                        quantity=quantity,
                        unit=unit,
                        current_emission=current_emission,
                        alternative_emission=alt_emission,
                        potential_saving=potential_saving,
                        saving_unit="kgCO2e",
                        reduction_percentage=reduction_pct,
                    )
                )

    # Primary ranking metric: potential_saving DESC
    recommendations.sort(key=lambda x: x.potential_saving, reverse=True)
    selected_recs = recommendations[:limit]

    return {
        "user_id": user_id,
        "month": month,
        "year": year,
        "top_drivers": [
            {
                "category": d.category,
                "activity_type": d.activity_type,
                "emission": d.emission,
            }
            for d in top_drivers
        ],
        "recommendations": [rec.to_dict() for rec in selected_recs],
    }
