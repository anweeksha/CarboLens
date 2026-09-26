"""ORM models.

Importing `load_models` registers every model on Base.metadata for create_all.
"""

from app.models.activity import Activity
from app.models.challenge import Challenge
from app.models.challenge_progress import ChallengeProgress
from app.models.department import Department
from app.models.emission_factor import EmissionFactor
from app.models.hostel import Hostel
from app.models.user import User


def load_models() -> None:
    """Ensure model modules are imported so metadata is complete."""
    return None


__all__ = [
    "Activity",
    "Challenge",
    "ChallengeProgress",
    "Department",
    "EmissionFactor",
    "Hostel",
    "User",
    "load_models",
]
