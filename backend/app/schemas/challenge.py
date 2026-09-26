"""Pydantic schemas for Challenge APIs."""

from __future__ import annotations

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class ChallengeJoinRequest(BaseModel):
    user_id: int = Field(..., description="ID of the user joining the challenge", json_schema_extra={"example": 1})


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class ChallengeResponse(BaseModel):
    """Single challenge listing item."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    category: str
    activity_type: str | None = None
    start_date: date
    end_date: date
    target: float
    target_unit: str
    status: str = Field(..., description="Derived status: active, upcoming, or completed")


class ChallengeListResponse(BaseModel):
    challenges: list[ChallengeResponse]
    count: int


class ChallengeJoinResponse(BaseModel):
    challenge_id: int
    user_id: int
    status: str = Field(..., description="Join status, e.g. 'joined'")
    baseline_emission: float
    baseline_status: str = Field(..., description="'calculated' or 'insufficient_baseline_data'")


class ChallengeProgressResponse(BaseModel):
    challenge_id: int
    user_id: int
    baseline_emission: float
    baseline_status: str
    current_emission: float
    saved_emission: float
    completion_percentage: float
    status: str


class ChallengeSummaryResponse(BaseModel):
    challenge_id: int
    name: str
    participants: int
    completed: int
    total_baseline_emission: float
    total_current_emission: float
    total_saved_emission: float
    average_saved_per_participant: float


class ChallengeLeaderboardItem(BaseModel):
    rank: int
    user_id: int
    user_name: str
    saved_emission: float
    completion_percentage: float


class ChallengeLeaderboardResponse(BaseModel):
    challenge_id: int
    leaderboard: list[ChallengeLeaderboardItem]
