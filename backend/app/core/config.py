"""Application configuration loaded from environment variables.

Put the Supabase PostgreSQL URI in backend/.env as DATABASE_URL.
Never commit .env. Existing process environment variables are not overwritten.
"""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path
from urllib.parse import parse_qsl, urlencode, urlparse, urlunparse

from dotenv import load_dotenv
from pydantic import BaseModel, Field, field_validator

BACKEND_ROOT = Path(__file__).resolve().parents[2]
# override=False: real OS env (CI, hosting) wins over the local .env file.
load_dotenv(BACKEND_ROOT / ".env", override=False)


def _as_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


def _normalize_database_url(value: str) -> str:
    url = value.strip()
    if not url:
        return url

    if "://" in url and "@" in url:
        scheme, rest = url.split("://", 1)
        credentials, hostinfo = rest.rsplit("@", 1)
        if ":" in credentials:
            username, password = credentials.rsplit(":", 1)
            if password.startswith("[") and password.endswith("]"):
                url = f"{scheme}://{username}:{password[1:-1]}@{hostinfo}"

    if url.startswith("postgres://"):
        url = url.replace("postgres://", "postgresql://", 1)
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg2://", 1)

    parsed = urlparse(url)
    hostname = (parsed.hostname or "").lower()
    if "supabase" in hostname:
        query = dict(parse_qsl(parsed.query, keep_blank_values=True))
        query.setdefault("sslmode", "require")
        url = urlunparse(parsed._replace(query=urlencode(query)))
    return url


class Settings(BaseModel):
    app_name: str = Field(default="CarbonLens API")
    database_url: str = Field(default="")
    gemini_api_key: str = Field(default="")
    db_echo: bool = Field(default=False)
    cors_allowed_origins: list[str] = Field(
        default_factory=lambda: [
            "http://localhost:3000",
            "http://127.0.0.1:3000",
            "http://localhost:5173",
            "http://127.0.0.1:5173",
        ]
    )

    @field_validator("database_url")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        return _normalize_database_url(value)

    @field_validator("cors_allowed_origins", mode="before")
    @classmethod
    def normalize_cors_allowed_origins(cls, value: str | list[str] | None) -> list[str]:
        if value is None or value == "":
            return []
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        return [str(value).strip()]

    @property
    def has_database_url(self) -> bool:
        return bool(self.database_url)


@lru_cache
def get_settings() -> Settings:
    return Settings(
        app_name=os.getenv("APP_NAME", "CarbonLens API"),
        database_url=os.getenv("DATABASE_URL", ""),
        gemini_api_key=os.getenv("GEMINI_API_KEY", ""),
        db_echo=_as_bool(os.getenv("DB_ECHO"), False),
        cors_allowed_origins=os.getenv(
            "CORS_ALLOWED_ORIGINS",
            "http://localhost:3000,http://127.0.0.1:3000,http://localhost:5173,http://127.0.0.1:5173",
        ),
    )
