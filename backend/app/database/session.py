"""SQLAlchemy engine and session factory.

DATABASE_URL is read from the environment (see backend/.env). Credentials are
never hardcoded.
"""

from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings

_engine: Engine | None = None
SessionLocal = sessionmaker(autocommit=False, autoflush=False, class_=Session)


class DatabaseNotConfiguredError(RuntimeError):
    """Raised when DATABASE_URL is missing."""


def get_engine() -> Engine:
    """Create (once) and return the SQLAlchemy engine bound to DATABASE_URL."""
    global _engine
    if _engine is None:
        settings = get_settings()
        if not settings.has_database_url:
            raise DatabaseNotConfiguredError(
                "DATABASE_URL is not set. Copy backend/.env.example to backend/.env "
                "and paste your Supabase PostgreSQL connection string."
            )
        _engine = create_engine(
            settings.database_url,
            echo=settings.db_echo,
            pool_pre_ping=True,
        )
        SessionLocal.configure(bind=_engine)
    return _engine


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency: yield one session per request, then close it."""
    get_engine()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def check_connection() -> None:
    """Run SELECT 1 against PostgreSQL. Raises if the database is unreachable."""
    with get_engine().connect() as connection:
        connection.execute(text("SELECT 1"))
