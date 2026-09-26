"""Schemas package exports."""

from app.schemas.activity import ActivityCreate, ActivityResponse
from app.schemas.campus import (
    CampusOverviewResponse,
    CampusTrendItem,
    CampusTrendResponse,
    DepartmentAnalyticsItem,
    DepartmentAnalyticsResponse,
    HostelAnalyticsItem,
    HostelAnalyticsResponse,
    LeaderboardItem,
    LeaderboardResponse,
    UserBenchmarkResponse,
)
from app.schemas.challenge import (
    ChallengeJoinRequest,
    ChallengeJoinResponse,
    ChallengeLeaderboardItem,
    ChallengeLeaderboardResponse,
    ChallengeListResponse,
    ChallengeProgressResponse,
    ChallengeResponse,
    ChallengeSummaryResponse,
)
from app.schemas.department import DepartmentRead
from app.schemas.emission_factor import EmissionFactorCreate, EmissionFactorResponse
from app.schemas.footprint import (
    CategoryBreakdownResponse,
    FootprintResponse,
    MonthlyTrendItem,
    MonthlyTrendResponse,
)
from app.schemas.health import DatabaseHealthResponse, HealthResponse
from app.schemas.hostel import HostelRead
from app.schemas.recommendation import (
    RecommendationItem,
    RecommendationResponse,
    TopCarbonDriver,
)
from app.schemas.simulator import (
    SimulationChangeItem,
    SimulationChangeResult,
    SimulationRequest,
    SimulationResponse,
)
from app.schemas.user import UserRead

__all__ = [
    "ActivityCreate",
    "ActivityResponse",
    "CampusOverviewResponse",
    "CampusTrendItem",
    "CampusTrendResponse",
    "CategoryBreakdownResponse",
    "ChallengeJoinRequest",
    "ChallengeJoinResponse",
    "ChallengeLeaderboardItem",
    "ChallengeLeaderboardResponse",
    "ChallengeListResponse",
    "ChallengeProgressResponse",
    "ChallengeResponse",
    "ChallengeSummaryResponse",
    "DatabaseHealthResponse",
    "DepartmentAnalyticsItem",
    "DepartmentAnalyticsResponse",
    "DepartmentRead",
    "EmissionFactorCreate",
    "EmissionFactorResponse",
    "FootprintResponse",
    "HealthResponse",
    "HostelAnalyticsItem",
    "HostelAnalyticsResponse",
    "HostelRead",
    "LeaderboardItem",
    "LeaderboardResponse",
    "MonthlyTrendItem",
    "MonthlyTrendResponse",
    "RecommendationItem",
    "RecommendationResponse",
    "SimulationChangeItem",
    "SimulationChangeResult",
    "SimulationRequest",
    "SimulationResponse",
    "TopCarbonDriver",
    "UserBenchmarkResponse",
    "UserRead",
]

