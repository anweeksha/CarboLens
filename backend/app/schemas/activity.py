"""Pydantic schemas for activity logging and response."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ActivityCreate(BaseModel):
    user_id: int = Field(..., description="ID of the user logging the activity", json_schema_extra={"example": 1})
    category: str = Field(..., description="Category: travel, electricity, food, or waste", json_schema_extra={"example": "travel"})
    activity_type: str = Field(..., description="Specific activity type (e.g. car, bus, grid_electricity)", json_schema_extra={"example": "car"})
    quantity: float = Field(..., gt=0, description="Quantity of activity (must be > 0)", json_schema_extra={"example": 120.0})
    unit: str = Field(..., description="Unit of measurement", json_schema_extra={"example": "km"})
    activity_date: date = Field(..., description="Date of the activity (YYYY-MM-DD)", json_schema_extra={"example": "2026-09-26"})
    region: str = Field(default="global", description="Optional region code for location-specific emission factors", json_schema_extra={"example": "global"})
    activity_metadata: dict[str, Any] | None = Field(default=None, alias="metadata", description="Optional JSON metadata")

    @field_validator("quantity")
    @classmethod
    def validate_positive_quantity(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value

    @field_validator("category")
    @classmethod
    def validate_category(cls, value: str) -> str:
        clean = value.strip().lower()
        allowed = {"travel", "electricity", "food", "waste"}
        if clean not in allowed:
            raise ValueError(f"Category must be one of: {', '.join(sorted(allowed))}")
        return clean


class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    user_id: int
    category: str
    activity_type: str
    quantity: float
    unit: str
    activity_date: date
    emission: float = Field(..., description="Calculated CO2e emission in kgCO2e")
    emission_factor_used: float | None = Field(default=None, description="Emission factor value used at log time")
    emission_factor_source: str | None = Field(default=None, description="Source reference of the emission factor used")
    activity_metadata: dict[str, Any] | None = Field(
        default=None,
        validation_alias="activity_metadata",
        serialization_alias="metadata",
    )
    created_at: datetime
