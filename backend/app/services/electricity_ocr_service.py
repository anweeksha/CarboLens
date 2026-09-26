"""Gemini-powered electricity bill OCR extraction service.

The service extracts structured bill information only; it does not calculate CO2e.
It returns neutral structured values or nulls for fields that cannot be confidently read.
"""

from __future__ import annotations

import base64
import json
import logging
import re
from datetime import date
from typing import Any
from urllib import error, request

from app.core.config import get_settings

logger = logging.getLogger(__name__)

MAX_FILE_SIZE_BYTES = 10 * 1024 * 1024
ALLOWED_MIME_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
    "application/pdf",
}


class GeminiOCRServiceError(RuntimeError):
    """Raised when Gemini OCR extraction fails."""


def _sanitize_secret(value: str | None) -> str:
    if not value:
        return ""
    sanitized = value
    sanitized = re.sub(r"(?i)GEMINI_API_KEY\s*[:=]\s*[^\s,;]+", "API_KEY=[REDACTED]", sanitized)
    sanitized = re.sub(r"(?i)gemini_api_key\s*[:=]\s*[^\s,;]+", "API_KEY=[REDACTED]", sanitized)
    sanitized = re.sub(r"(?i)GEMINI_API_KEY", "API_KEY", sanitized)
    sanitized = re.sub(r"(?i)gemini_api_key", "API_KEY", sanitized)
    return sanitized


def _normalize_unit(value: Any) -> str | None:
    if value is None:
        return None
    cleaned = str(value).strip().lower()
    if cleaned in {"", "unknown", "n/a", "na", "none"}:
        return None
    if cleaned in {"unit", "units"}:
        return "kWh"
    return cleaned.replace(" ", "_")


def _parse_float(value: Any) -> float | None:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        text = value.strip()
        if not text or text.lower() in {"unknown", "n/a", "na", "none"}:
            return None
        text = text.replace(",", "")
        try:
            return float(text)
        except ValueError:
            return None
    return None


def _parse_date(value: Any) -> date | None:
    if value is None:
        return None
    if isinstance(value, date):
        return value
    if not isinstance(value, str):
        return None
    text = value.strip()
    if not text or text.lower() in {"unknown", "n/a", "na", "none"}:
        return None
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y", "%Y/%m/%d"):
        try:
            return __import__("datetime").datetime.strptime(text, fmt).date()
        except ValueError:
            continue
    return None


def _coerce_extracted_payload(raw_payload: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(raw_payload, dict):
        raw_payload = {}

    consumption = _parse_float(raw_payload.get("extracted_consumption"))
    unit = _normalize_unit(raw_payload.get("unit") or "kWh")
    if unit is None:
        unit = "kWh"

    if consumption is not None and consumption <= 0:
        consumption = None

    return {
        "status": str(raw_payload.get("status", "success")).strip() or "success",
        "extracted_consumption": consumption,
        "unit": unit,
        "billing_start_date": _parse_date(raw_payload.get("billing_start_date")),
        "billing_end_date": _parse_date(raw_payload.get("billing_end_date")),
        "provider": (str(raw_payload.get("provider") or "").strip() or None) if raw_payload.get("provider") else None,
        "bill_amount": _parse_float(raw_payload.get("bill_amount")),
        "confidence": float(raw_payload["confidence"]) if isinstance(raw_payload.get("confidence"), (int, float)) else None,
        "needs_confirmation": list(raw_payload.get("needs_confirmation") or []),
        "source": str(raw_payload.get("source") or "gemini").strip() or "gemini",
        "validation": raw_payload.get("validation") if isinstance(raw_payload.get("validation"), dict) else None,
        "message": raw_payload.get("message"),
    }


class GeminiBillExtractor:
    """Thin Gemini REST client for structured electricity bill extraction."""

    def __init__(self, api_key: str | None = None):
        settings = get_settings()
        self.api_key = api_key if api_key is not None else settings.gemini_api_key

    def extract_bill(self, *, file_bytes: bytes, file_name: str, mime_type: str) -> dict[str, Any]:
        if not self.api_key:
            raise GeminiOCRServiceError("Gemini API key is not configured. Set GEMINI_API_KEY in the environment.")

        inline_data = base64.b64encode(file_bytes).decode("ascii")
        prompt = (
            "Extract only structured information from this electricity bill. "
            "Respond with valid JSON only. Include keys: "
            "status, extracted_consumption, unit, billing_start_date, billing_end_date, provider, bill_amount, "
            "confidence, needs_confirmation, validation, message. "
            "Use null for missing values. Do not calculate emissions. Do not guess missing values. "
            "Return only JSON, no markdown fences."
        )
        payload = {
            "contents": [{
                "parts": [
                    {"text": prompt},
                    {"inline_data": {"mime_type": mime_type, "data": inline_data}},
                ]
            }],
            "generationConfig": {"response_mime_type": "application/json"},
        }

        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self.api_key}"
        req = request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=60) as response:
                body = response.read().decode("utf-8")
        except error.HTTPError as exc:
            body = exc.read().decode("utf-8", errors="replace")
            raise GeminiOCRServiceError(f"Gemini API request failed: {_sanitize_secret(body)[:500]}") from exc
        except Exception as exc:  # pragma: no cover - network fallback
            raise GeminiOCRServiceError(f"Gemini OCR service error: {_sanitize_secret(str(exc))}") from exc

        try:
            response_json = json.loads(body)
        except json.JSONDecodeError as exc:
            raise GeminiOCRServiceError("Gemini returned invalid JSON for the electricity bill extraction request.") from exc

        candidates = response_json.get("candidates") or []
        if not candidates:
            raise GeminiOCRServiceError("Gemini returned no OCR candidates for the electricity bill.")

        parts = candidates[0].get("content", {}).get("parts", [])
        text_output = ""
        for part in parts:
            if isinstance(part, dict) and "text" in part:
                text_output += str(part["text"])

        if not text_output:
            raise GeminiOCRServiceError("Gemini did not return any extracted bill text.")

        try:
            parsed = json.loads(text_output)
        except json.JSONDecodeError:
            stripped = text_output.strip()
            if stripped.startswith("```"):
                stripped = stripped.strip("`")
                if stripped.lower().startswith("json"):
                    stripped = stripped[4:].lstrip()
            try:
                parsed = json.loads(stripped)
            except json.JSONDecodeError as exc:
                raise GeminiOCRServiceError("Gemini returned malformed JSON while extracting the electricity bill.") from exc

        return _coerce_extracted_payload(parsed)


def extract_bill_data(*, file_bytes: bytes, file_name: str, mime_type: str) -> dict[str, Any]:
    """Public helper that performs Gemini OCR and returns normalized structured data."""
    extractor = GeminiBillExtractor()
    try:
        return extractor.extract_bill(file_bytes=file_bytes, file_name=file_name, mime_type=mime_type)
    except GeminiOCRServiceError:
        raise
    except Exception as exc:
        sanitized = _sanitize_secret(str(exc))
        logger.error("Gemini electricity OCR failed: %s", sanitized)
        raise GeminiOCRServiceError(f"Gemini electricity OCR failed: {sanitized}")
