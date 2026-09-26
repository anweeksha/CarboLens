"""Electricity bill OCR and confirmation API routes."""

from __future__ import annotations

import logging
from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.activity import Activity
from app.models.user import User
from app.schemas.activity import ActivityResponse
from app.schemas.electricity_bill import (
    ElectricityBillConfirmationRequest,
    ElectricityBillConfirmationResponse,
    ElectricityBillExtractionResponse,
)
from app.services.carbon_engine import calculate_emission
from app.services.electricity_ocr_service import (
    MAX_FILE_SIZE_BYTES,
    ALLOWED_MIME_TYPES,
    GeminiOCRServiceError,
    _sanitize_secret,
    extract_bill_data,
)
from app.services.exceptions import EmissionFactorNotFoundError, InvalidQuantityError, UnitMismatchError, UserNotFoundError

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/electricity-bills", tags=["electricity-bills"])


def _normalize_bill_unit(unit: str | None) -> str:
    if not unit:
        return "kWh"
    normalized = unit.strip().lower()
    if normalized in {"unit", "units", "kwh", "kilowatt_hour", "kilowatt_hours"}:
        return "kWh"
    return unit.strip()


def _validate_extracted_consumption(consumption: float | None, *, source_label: str = "Extracted consumption") -> float:
    if consumption is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{source_label} is missing or could not be confidently extracted. Please provide the electricity consumption manually.",
        )
    if consumption <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{source_label} must be greater than 0.",
        )
    return float(consumption)


@router.post(
    "/extract",
    response_model=ElectricityBillExtractionResponse,
    summary="Extract structured data from an electricity bill upload",
)
async def extract_electricity_bill(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
) -> dict:
    """Validate uploaded file type/size, call Gemini OCR, and return structured extraction; no raw bill is stored."""
    if not file or not file.filename:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No bill file was uploaded.")

    if file.content_type not in ALLOWED_MIME_TYPES and not file.filename.lower().endswith((".png", ".jpg", ".jpeg", ".webp", ".pdf")):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Unsupported file type. Please upload a JPG, PNG, WEBP, or PDF electricity bill.")

    file_bytes = await file.read()
    if not file_bytes or len(file_bytes) == 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Uploaded bill file is empty.")
    if len(file_bytes) > MAX_FILE_SIZE_BYTES:
        raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE, detail="Uploaded bill is too large. Please upload a bill smaller than 10 MB.")

    try:
        extracted = extract_bill_data(file_bytes=file_bytes, file_name=file.filename, mime_type=file.content_type or "application/octet-stream")
    except GeminiOCRServiceError as exc:
        sanitized = _sanitize_secret(str(exc))
        logger.error("Gemini electricity OCR extraction failed: %s", sanitized)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Gemini electricity bill extraction failed: {sanitized}")
    except Exception as exc:
        sanitized = _sanitize_secret(str(exc))
        logger.error("Unexpected electricity OCR failure: %s", sanitized)
        raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"Gemini electricity bill extraction failed: {sanitized}")

    consumption = _validate_extracted_consumption(extracted.get("extracted_consumption"), source_label="Extracted electricity consumption")
    normalized = {
        "status": extracted.get("status", "success"),
        "consumption": float(consumption),
        "unit": _normalize_bill_unit(extracted.get("unit") or "kWh"),
        "billing_start_date": extracted.get("billing_start_date"),
        "billing_end_date": extracted.get("billing_end_date"),
        "provider": extracted.get("provider"),
        "bill_amount": extracted.get("bill_amount"),
        "confidence": extracted.get("confidence"),
        "needs_confirmation": extracted.get("needs_confirmation") or [],
        "source": extracted.get("source") or "gemini",
        "validation": extracted.get("validation"),
        "message": extracted.get("message"),
    }
    return normalized


@router.post(
    "/confirm",
    response_model=ElectricityBillConfirmationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Confirm extracted electricity bill data and create an activity",
)
def confirm_electricity_bill(
    payload: ElectricityBillConfirmationRequest,
    db: Session = Depends(get_db),
) -> Activity:
    """Validate the confirmed values and create a grid electricity activity using the existing carbon engine."""
    if payload.consumption <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Consumption must be greater than 0.")

    user = db.get(User, payload.user_id)
    if not user:
        if payload.user_id == 1:
            user = User(
                id=1,
                name="Demo CarbonLens User",
                email="demo@carbonlens.org",
                user_type="student",
            )
            db.add(user)
            db.commit()
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with ID {payload.user_id} not found.")

    if payload.billing_start_date and payload.billing_end_date and payload.billing_end_date < payload.billing_start_date:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Billing end date cannot be earlier than billing start date.")

    normalized_unit = _normalize_bill_unit(payload.unit)
    if normalized_unit not in {"kWh", "kwh", "kilowatt_hour", "kilowatt_hours"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Confirmed bill consumption unit must be kWh.")

    activity_date = payload.billing_end_date or payload.billing_start_date or date.today()

    try:
        calc_result = calculate_emission(
            category="electricity",
            activity_type="grid_electricity",
            quantity=payload.consumption,
            unit=normalized_unit,
            db=db,
            region=payload.region,
        )
    except InvalidQuantityError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except UnitMismatchError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    except EmissionFactorNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No suitable electricity emission factor is configured for grid_electricity/kWh. Please add the required emission factor before confirming the bill.",
        )
    except UserNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))

    activity = Activity(
        user_id=payload.user_id,
        category=calc_result.category,
        activity_type=calc_result.activity_type,
        quantity=payload.consumption,
        unit=normalized_unit,
        activity_date=activity_date,
        emission=calc_result.emission,
        emission_factor_used=calc_result.emission_factor,
        emission_factor_source=f"{calc_result.factor_source} ({calc_result.factor_source_year})",
        activity_metadata={
            "source": "electricity_bill_ocr",
            "provider": payload.provider,
            "bill_amount": payload.bill_amount,
            "billing_start_date": payload.billing_start_date.isoformat() if payload.billing_start_date else None,
            "billing_end_date": payload.billing_end_date.isoformat() if payload.billing_end_date else None,
            "meter_identifier": payload.meter_identifier,
        },
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity
