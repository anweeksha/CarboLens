"""Domain services exports."""

from app.services.campus_engine import (
    get_campus_overview,
    get_campus_trend,
    get_department_analytics,
    get_hostel_analytics,
    get_leaderboard,
    get_user_benchmark,
)
from app.services.carbon_engine import CarbonCalculationResult, calculate_emission
from app.services.challenge_engine import (
    ChallengeDuplicateJoinError,
    ChallengeEngineError,
    ChallengeNotFoundError,
    ChallengeNotJoinableError,
    ChallengeNotJoinedError,
    ChallengeUserNotFoundError,
    get_challenge_leaderboard,
    get_challenge_progress,
    get_challenge_summary,
    join_challenge,
    list_challenges,
)
from app.services.emission_factor_service import get_emission_factor
from app.services.exceptions import (
    AmbiguousEmissionFactorError,
    CarbonEngineError,
    EmissionFactorNotFoundError,
    InvalidActivityDataError,
    InvalidQuantityError,
    UnitMismatchError,
    UserNotFoundError,
)
from app.services.recommendation_engine import generate_recommendations, get_top_carbon_drivers
from app.services.simulator import SimulationChangeItemInput, run_simulation

__all__ = [
    "AmbiguousEmissionFactorError",
    "CarbonCalculationResult",
    "CarbonEngineError",
    "ChallengeDuplicateJoinError",
    "ChallengeEngineError",
    "ChallengeNotFoundError",
    "ChallengeNotJoinableError",
    "ChallengeNotJoinedError",
    "ChallengeUserNotFoundError",
    "EmissionFactorNotFoundError",
    "InvalidActivityDataError",
    "InvalidQuantityError",
    "SimulationChangeItemInput",
    "UnitMismatchError",
    "UserNotFoundError",
    "calculate_emission",
    "generate_recommendations",
    "get_campus_overview",
    "get_campus_trend",
    "get_challenge_leaderboard",
    "get_challenge_progress",
    "get_challenge_summary",
    "get_department_analytics",
    "get_emission_factor",
    "get_hostel_analytics",
    "get_leaderboard",
    "get_top_carbon_drivers",
    "get_user_benchmark",
    "join_challenge",
    "list_challenges",
    "run_simulation",
]

