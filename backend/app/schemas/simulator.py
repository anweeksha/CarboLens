"""Pydantic schemas for What-If Simulator API requests and responses."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field, field_validator


class SimulationChangeItem(BaseModel):
    category: str = Field(..., description="Category: travel, electricity, food, or waste", json_schema_extra={"example": "travel"})
    from_activity: str = Field(..., description="Current activity type", json_schema_extra={"example": "car"})
    to_activity: str = Field(..., description="Hypothetical alternative activity type", json_schema_extra={"example": "bus"})
    quantity: float = Field(..., gt=0, description="Quantity of activity (must be > 0)", json_schema_extra={"example": 240.0})
    unit: str = Field(..., description="Unit of measurement", json_schema_extra={"example": "km"})
    region: str = Field(default="global", description="Optional region code", json_schema_extra={"example": "global"})

    @field_validator("quantity")
    @classmethod
    def validate_positive(cls, value: float) -> float:
        if value <= 0:
            raise ValueError("Quantity must be greater than 0")
        return value


class SimulationRequest(BaseModel):
    user_id: int = Field(..., description="User ID", json_schema_extra={"example": 1})
    changes: list[SimulationChangeItem] = Field(..., min_length=1, description="List of hypothetical activity changes")


class SimulationChangeResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str
    from_activity: str
    to_activity: str
    quantity: float
    unit: str
    current_emission: float = Field(..., description="Current emission in kgCO2e")
    projected_emission: float = Field(..., description="Hypothetical projected emission in kgCO2e")
    saving: float = Field(..., description="Hypothetical savings in kgCO2e")
    reduction_percentage: float = Field(..., description="Percentage reduction")


class SimulationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    current_total: float = Field(..., description="Total baseline emissions across proposed changes")
    projected_total: float = Field(..., description="Total projected emissions across proposed changes")
    total_saving: float = Field(..., description="Total projected CO2e savings")
    saving_unit: str = Field(default="kgCO2e")
    reduction_percentage: float = Field(..., description="Overall percentage reduction")
    changes: list[SimulationChangeResult]
