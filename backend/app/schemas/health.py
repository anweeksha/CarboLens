"""Health check schemas."""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["healthy"])
    service: str = Field(examples=["CarbonLens API"])


class DatabaseHealthResponse(BaseModel):
    status: str = Field(examples=["healthy"])
    database: str = Field(examples=["connected"])
