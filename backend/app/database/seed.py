"""Seed initial published benchmark emission factors, default campus entities, and demo user."""

from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.department import Department
from app.models.emission_factor import EmissionFactor
from app.models.hostel import Hostel
from app.models.user import User

# Published benchmark emission factors with source details
PUBLISHED_FACTORS = [
    # Travel
    {
        "category": "travel",
        "activity_type": "car",
        "unit": "km",
        "factor": 0.1709,
        "source": "UK DEFRA 2024 Greenhouse Gas Reporting Conversion Factors - Medium Petrol Car",
        "source_year": 2024,
        "region": "global",
    },
    {
        "category": "travel",
        "activity_type": "bus",
        "unit": "passenger_km",
        "factor": 0.0965,
        "source": "UK DEFRA 2024 Conversion Factors - Local Bus",
        "source_year": 2024,
        "region": "global",
    },
    {
        "category": "travel",
        "activity_type": "flight_domestic",
        "unit": "passenger_km",
        "factor": 0.2458,
        "source": "UK DEFRA 2024 Conversion Factors - Domestic Flight with radiative forcing",
        "source_year": 2024,
        "region": "global",
    },
    # Electricity
    {
        "category": "electricity",
        "activity_type": "grid_electricity",
        "unit": "kWh",
        "factor": 0.7160,
        "source": "CEA India CO2 Baseline Database v19 / UK DEFRA 2024 Grid average",
        "source_year": 2024,
        "region": "global",
    },
    # Food
    {
        "category": "food",
        "activity_type": "vegetarian_meal",
        "unit": "meal",
        "factor": 1.2000,
        "source": "World Resources Institute (WRI) Food Carbon Benchmark",
        "source_year": 2023,
        "region": "global",
    },
    {
        "category": "food",
        "activity_type": "non_vegetarian_meal",
        "unit": "meal",
        "factor": 3.5000,
        "source": "World Resources Institute (WRI) Food Carbon Benchmark",
        "source_year": 2023,
        "region": "global",
    },
    # Waste
    {
        "category": "waste",
        "activity_type": "plastic",
        "unit": "kg",
        "factor": 2.8900,
        "source": "UK DEFRA 2024 Waste Disposal - Mixed Plastics",
        "source_year": 2024,
        "region": "global",
    },
    {
        "category": "waste",
        "activity_type": "organic_waste",
        "unit": "kg",
        "factor": 0.5840,
        "source": "UK DEFRA 2024 Waste Disposal - Food & Organic Waste",
        "source_year": 2024,
        "region": "global",
    },
]

DEFAULT_DEPARTMENTS = [
    "Computer Science & Engineering",
    "Electrical Engineering",
    "Mechanical Engineering",
    "Civil Engineering",
]

DEFAULT_HOSTELS = [
    "Hostel Alpha",
    "Hostel Beta",
    "Hostel Gamma",
]


def seed_database(db: Session) -> None:
    """Seed published benchmark emission factors, departments, hostels, and default demo user if missing."""
    # Seed emission factors
    for item in PUBLISHED_FACTORS:
        existing = db.scalar(
            select(EmissionFactor).where(
                EmissionFactor.category == item["category"],
                EmissionFactor.activity_type == item["activity_type"],
                EmissionFactor.unit == item["unit"],
                EmissionFactor.region == item["region"],
            )
        )
        if not existing:
            ef = EmissionFactor(**item)
            db.add(ef)

    # Seed departments
    dept_map: dict[str, Department] = {}
    for dname in DEFAULT_DEPARTMENTS:
        existing_dept = db.scalar(select(Department).where(Department.name == dname))
        if not existing_dept:
            dept = Department(name=dname)
            db.add(dept)
            db.flush()
            dept_map[dname] = dept
        else:
            dept_map[dname] = existing_dept

    # Seed hostels
    hostel_map: dict[str, Hostel] = {}
    for hname in DEFAULT_HOSTELS:
        existing_hostel = db.scalar(select(Hostel).where(Hostel.name == hname))
        if not existing_hostel:
            hostel = Hostel(name=hname)
            db.add(hostel)
            db.flush()
            hostel_map[hname] = hostel
        else:
            hostel_map[hname] = existing_hostel

    # Seed default demo user (ID=1) if no users exist
    demo_user = db.scalar(select(User).where(User.id == 1))
    if not demo_user:
        cst_id = dept_map.get("Computer Science & Engineering").id if "Computer Science & Engineering" in dept_map else None
        alpha_id = hostel_map.get("Hostel Alpha").id if "Hostel Alpha" in hostel_map else None
        user = User(
            id=1,
            name="Demo CarbonLens User",
            email="demo@carbonlens.org",
            department_id=cst_id,
            hostel_id=alpha_id,
            year=2026,
            user_type="student",
        )
        db.add(user)

    db.commit()
