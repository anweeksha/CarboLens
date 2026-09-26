"""Pydantic schemas for campus overview, department/hostel analytics, benchmarks, and leaderboards."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, Field


class CampusOverviewResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    month: int | None = Field(default=None, json_schema_extra={"example": 9})
    year: int | None = Field(default=None, json_schema_extra={"example": 2026})
    total_emission: float = Field(..., description="Total campus CO2e in kgCO2e", json_schema_extra={"example": 4500.5})
    active_users: int = Field(..., description="Number of users who logged activities in target period", json_schema_extra={"example": 150})
    average_per_active_user: float = Field(..., description="Average CO2e per active user", json_schema_extra={"example": 30.0033})
    unit: str = Field(default="kgCO2e", json_schema_extra={"example": "kgCO2e"})
    categories: dict[str, float] = Field(..., description="Emissions per category in kgCO2e")
    category_percentages: dict[str, float] = Field(..., description="Percentage share per category")


class CampusTrendItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    month: str = Field(..., description="Year-Month (YYYY-MM)", json_schema_extra={"example": "2026-09"})
    emission: float = Field(..., description="Campus emissions in kgCO2e", json_schema_extra={"example": 4500.5})


class CampusTrendResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    trend: list[CampusTrendItem]


class DepartmentAnalyticsItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    department: str = Field(..., json_schema_extra={"example": "Computer Science & Engineering"})
    users: int = Field(..., description="Total registered population", json_schema_extra={"example": 200})
    active_users: int = Field(..., description="Active user count", json_schema_extra={"example": 120})
    total_emission: float = Field(..., description="Total department emissions", json_schema_extra={"example": 1200.5})
    average_per_active_user: float = Field(..., description="Average per active user", json_schema_extra={"example": 10.0042})
    categories: dict[str, float] = Field(..., description="Category breakdown")


class DepartmentAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    departments: list[DepartmentAnalyticsItem]


class HostelAnalyticsItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hostel: str = Field(..., json_schema_extra={"example": "Hostel Alpha"})
    users: int = Field(..., description="Total registered population", json_schema_extra={"example": 150})
    active_users: int = Field(..., description="Active user count", json_schema_extra={"example": 90})
    total_emission: float = Field(..., description="Total hostel emissions", json_schema_extra={"example": 900.25})
    average_per_active_user: float = Field(..., description="Average per active user", json_schema_extra={"example": 10.0028})
    categories: dict[str, float] = Field(..., description="Category breakdown")


class HostelAnalyticsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    hostels: list[HostelAnalyticsItem]


class UserBenchmarkResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user_id: int = Field(..., json_schema_extra={"example": 1})
    month: int | None = Field(default=None, json_schema_extra={"example": 9})
    year: int | None = Field(default=None, json_schema_extra={"example": 2026})
    user_emission: float = Field(..., description="User emission in target period", json_schema_extra={"example": 25.5})
    campus_average: float = Field(..., description="Campus average per active user", json_schema_extra={"example": 30.0})
    difference: float = Field(..., description="User emission minus campus average", json_schema_extra={"example": -4.5})
    difference_percentage: float = Field(..., description="Percentage difference relative to campus average", json_schema_extra={"example": -15.0})
    benchmark_type: str = Field(default="Campus average per active user", json_schema_extra={"example": "Campus average per active user"})


class LeaderboardItem(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., json_schema_extra={"example": "Computer Science & Engineering"})
    users: int = Field(..., description="Total population", json_schema_extra={"example": 200})
    active_users: int = Field(..., description="Active users count", json_schema_extra={"example": 120})
    total_emission: float = Field(..., description="Total emissions", json_schema_extra={"example": 1200.5})
    average_per_active_user: float = Field(..., description="Per active user emission", json_schema_extra={"example": 10.0042})
    current_period_emission: float = Field(..., description="Emissions in current period")
    previous_period_emission: float = Field(..., description="Emissions in previous period")
    change_percentage: float = Field(..., description="Period-over-period change percentage")


class LeaderboardResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    entity_type: str = Field(..., json_schema_extra={"example": "department"})
    month: int = Field(..., json_schema_extra={"example": 9})
    year: int = Field(..., json_schema_extra={"example": 2026})
    leaderboard: list[LeaderboardItem]
