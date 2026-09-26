"""Pydantic schemas for carbon footprint, category breakdown, and monthly trends."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class FootprintResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., json_schema_extra={"example": 1})
    month: int = Field(..., ge=1, le=12, json_schema_extra={"example": 9})
    year: int = Field(..., json_schema_extra={"example": 2026})
    total_emission: float = Field(..., description="Total carbon emission in kgCO2e", json_schema_extra={"example": 120.5})
    unit: str = Field(default="kgCO2e", json_schema_extra={"example": "kgCO2e"})


class CategoryBreakdownResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    travel: float = Field(default=0.0, description="Emissions from travel (kgCO2e)")
    electricity: float = Field(default=0.0, description="Emissions from electricity (kgCO2e)")
    food: float = Field(default=0.0, description="Emissions from food (kgCO2e)")
    waste: float = Field(default=0.0, description="Emissions from waste (kgCO2e)")


class MonthlyTrendItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    month: str = Field(..., description="Year and month in YYYY-MM format", json_schema_extra={"example": "2026-09"})
    emission: float = Field(..., description="Total emissions for the month in kgCO2e", json_schema_extra={"example": 120.5})


class MonthlyTrendResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int
    trend: list[MonthlyTrendItem]
