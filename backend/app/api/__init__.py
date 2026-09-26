"""HTTP routers assembly."""

from fastapi import APIRouter

from app.api.activities import router as activities_router
from app.api.campus import router as campus_router
from app.api.challenges import router as challenges_router
from app.api.electricity_bills import router as electricity_bills_router
from app.api.emission_factors import router as emission_factors_router
from app.api.footprint import router as footprint_router
from app.api.health import router as health_router
from app.api.leaderboard import router as leaderboard_router
from app.api.recommendations import router as recommendations_router
from app.api.simulator import router as simulator_router

api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(emission_factors_router)
api_router.include_router(activities_router)
api_router.include_router(footprint_router)
api_router.include_router(recommendations_router)
api_router.include_router(simulator_router)
api_router.include_router(campus_router)
api_router.include_router(leaderboard_router)
api_router.include_router(challenges_router)
api_router.include_router(electricity_bills_router)
