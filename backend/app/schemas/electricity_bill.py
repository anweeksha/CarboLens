"""Pydantic schemas for electricity bill OCR and confirmation flows."""

from __future__ import annotations

from datetime import date, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator


class ElectricityBillExtractionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    status: str = Field(default="success", description="Extraction status")
    consumption: float | None = Field(default=None, description="Extracted electricity consumption in kWh")
    unit: str | None = Field(default=None, description="Consumption unit, typically kWh")
    billing_start_date: date | None = Field(default=None, description="Billing period start date")
    billing_end_date: date | None = Field(default=None, description="Billing period end date")
    provider: str | None = Field(default=None, description="Electricity provider name")
    bill_amount: float | None = Field(default=None, description="Bill amount if present")
    confidence: float | None = Field(default=None, description="OCR confidence score between 0 and 1")
    needs_confirmation: list[str] = Field(default_factory=list, description="Fields requiring user confirmation")
    source: str = Field(default="gemini", description="Extraction source")
    validation: dict[str, Any] | None = Field(default=None, description="Validation metadata for extracted fields")
    message: str | None = Field(default=None, description="Optional human-readable status message")

    @field_validator("unit")
    @classmethod
    def normalize_unit(cls, value: str | None) -> str | None:
        if value is None:
            return None
        cleaned = value.strip().lower()
        if cleaned in {"unit", "units"}:
            return "kWh"
        return value.strip()


class ElectricityBillConfirmationRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user confirming the bill")
    consumption: float = Field(..., description="Confirmed electricity consumption in kWh")
    unit: str = Field(..., min_length=1, description="Unit of the confirmed consumption value")
    billing_start_date: date | None = Field(default=None, description="Confirmed bill start date")
    billing_end_date: date | None = Field(default=None, description="Confirmed bill end date")
    provider: str | None = Field(default=None, description="Confirmed provider name")
    bill_amount: float | None = Field(default=None, gt=0, description="Confirmed bill amount if available")
    region: str = Field(default="global", description="Region to use for emission factor lookup")
    meter_identifier: str | None = Field(default=None, description="Optional meter/account identifier not persisted by default")

    @field_validator("unit")
    @classmethod
    def normalize_unit(cls, value: str) -> str:
        cleaned = value.strip().lower()
        if cleaned in {"unit", "units"}:
            return "kWh"
        return value.strip()

    @field_validator("billing_end_date")
    @classmethod
    def validate_date_window(cls, value: date | None):
        if value is None:
            return value
        return value

    @field_validator("region")
    @classmethod
    def normalize_region(cls, value: str) -> str:
        return value.strip().lower() or "global"


class ElectricityBillConfirmationResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)

    id: int
    user_id: int
    category: str
    activity_type: str
    quantity: float
    unit: str
    activity_date: date
    emission: float
    emission_factor_used: float | None = None
    emission_factor_source: str | None = None
    activity_metadata: dict[str, Any] | None = None
    created_at: datetime
