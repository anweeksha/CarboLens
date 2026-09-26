"""Explicit table creation and seeding.

Run from backend/:

    python -m app.database.init_db

Uses SQLAlchemy create_all: missing tables are created. Existing tables and
data are never dropped or rebuilt. Seeds published emission factors.
"""

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session

from app.database.base import Base
from app.database.seed import seed_database
from app.database.session import get_engine
from app.models import load_models


def init_db(engine: Engine | None = None) -> None:
    """Create missing tables and seed initial factors. Does not drop or recreate existing tables."""
    load_models()
    bind = engine or get_engine()
    Base.metadata.create_all(bind=bind)

    with Session(bind) as session:
        seed_database(session)


if __name__ == "__main__":
    init_db()
    print("CarbonLens database initialized and seeded successfully.")
