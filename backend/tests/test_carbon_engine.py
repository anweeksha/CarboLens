"""Unit tests for Carbon Calculation Engine and Emission Factor Lookup."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.database.base import Base
from app.database.seed import seed_database
from app.models import load_models
from app.services.carbon_engine import calculate_emission
from app.services.exceptions import (
    EmissionFactorNotFoundError,
    InvalidQuantityError,
    UnitMismatchError,
)


@pytest.fixture
def db_session():
    """Create an in-memory SQLite database session with seeded benchmark factors."""
    load_models()
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    seed_database(session)
    try:
        yield session
    finally:
        session.close()


def test_valid_emission_calculation(db_session: Session):
    """Test 1: Valid emission calculation for car travel (120 km * 0.1709 = 20.508 kgCO2e)."""
    result = calculate_emission(
        category="travel",
        activity_type="car",
        quantity=120.0,
        unit="km",
        db=db_session,
    )
    assert result.category == "travel"
    assert result.activity_type == "car"
    assert result.quantity == 120.0
    assert result.unit == "km"
    assert result.emission_factor == 0.1709
    assert abs(result.emission - 20.508) < 1e-4
    assert "UK DEFRA" in result.factor_source
    assert result.factor_source_year == 2024


def test_negative_quantity_rejection(db_session: Session):
    """Test 2: Rejection of zero or negative activity quantities."""
    with pytest.raises(InvalidQuantityError, match="must be greater than 0"):
        calculate_emission(
            category="travel",
            activity_type="car",
            quantity=-10.0,
            unit="km",
            db=db_session,
        )

    with pytest.raises(InvalidQuantityError, match="must be greater than 0"):
        calculate_emission(
            category="electricity",
            activity_type="grid_electricity",
            quantity=0,
            unit="kWh",
            db=db_session,
        )


def test_missing_emission_factor(db_session: Session):
    """Test 3: Handling when an emission factor is not found in the database."""
    with pytest.raises(EmissionFactorNotFoundError, match="No emission factor found"):
        calculate_emission(
            category="travel",
            activity_type="spaceship",
            quantity=100.0,
            unit="km",
            db=db_session,
        )


def test_unit_mismatch(db_session: Session):
    """Test 4: Handling when requested unit does not match emission factor unit."""
    with pytest.raises(UnitMismatchError, match="incompatible with emission factor"):
        calculate_emission(
            category="travel",
            activity_type="car",
            quantity=120.0,
            unit="kWh",  # Car uses km, not kWh
            db=db_session,
        )
