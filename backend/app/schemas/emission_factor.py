"""Pydantic schemas for emission factors."""

from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class EmissionFactorBase(BaseModel):
    category: str = Field(..., description="Activity category (e.g. travel, electricity, food, waste)", json_schema_extra={"example": "travel"})
    activity_type: str = Field(..., description="Specific activity type (e.g. car, bus, grid_electricity)", json_schema_extra={"example": "car"})
    unit: str = Field(..., description="Unit of measurement (e.g. km, kWh, meal, kg)", json_schema_extra={"example": "km"})
    factor: float = Field(..., gt=0, description="Emission factor value (kgCO2e per unit)", json_schema_extra={"example": 0.1709})
    source: str = Field(..., description="Published reference source for this factor", json_schema_extra={"example": "UK DEFRA 2024 Conversion Factors"})
    source_year: int = Field(..., description="Publication year of the emission factor source", json_schema_extra={"example": 2024})
    region: str = Field(default="global", description="Geographic region code", json_schema_extra={"example": "global"})


class EmissionFactorCreate(EmissionFactorBase):
    pass


class EmissionFactorResponse(EmissionFactorBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
