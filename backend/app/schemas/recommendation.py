"""Pydantic schemas for personalized recommendation API responses."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class TopCarbonDriver(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    category: str = Field(..., json_schema_extra={"example": "travel"})
    activity_type: str = Field(..., json_schema_extra={"example": "car"})
    emission: float = Field(..., description="Total CO2e emission in kgCO2e", json_schema_extra={"example": 52.4})


class RecommendationItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., json_schema_extra={"example": "Switch from car to bus"})
    category: str = Field(..., json_schema_extra={"example": "travel"})
    current_activity: str = Field(..., json_schema_extra={"example": "car"})
    alternative_activity: str = Field(..., json_schema_extra={"example": "bus"})
    quantity: float = Field(..., json_schema_extra={"example": 240.0})
    unit: str = Field(..., json_schema_extra={"example": "km"})
    current_emission: float = Field(..., json_schema_extra={"example": 41.016})
    alternative_emission: float = Field(..., json_schema_extra={"example": 23.16})
    potential_saving: float = Field(..., json_schema_extra={"example": 17.856})
    saving_unit: str = Field(default="kgCO2e", json_schema_extra={"example": "kgCO2e"})
    reduction_percentage: float = Field(..., json_schema_extra={"example": 43.53})


class RecommendationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., json_schema_extra={"example": 1})
    month: int | None = Field(default=None, json_schema_extra={"example": 9})
    year: int | None = Field(default=None, json_schema_extra={"example": 2026})
    top_drivers: list[TopCarbonDriver]
    recommendations: list[RecommendationItem]
