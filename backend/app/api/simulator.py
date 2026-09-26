"""What-If Simulator API router."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.schemas.simulator import SimulationRequest, SimulationResponse
from app.services.exceptions import (
    EmissionFactorNotFoundError,
    InvalidQuantityError,
    UnitMismatchError,
    UserNotFoundError,
)
from app.services.simulator import SimulationChangeItemInput, run_simulation

router = APIRouter(tags=["simulator"])


@router.post(
    "/simulate",
    response_model=SimulationResponse,
    summary="Simulate hypothetical carbon reduction scenarios",
)
def simulate_changes(
    payload: SimulationRequest,
    db: Session = Depends(get_db),
) -> dict:
    """Run a hypothetical What-If carbon simulation for proposed activity changes.

    This operation is strictly read-only and does not alter the database.
    """
    change_inputs = [
        SimulationChangeItemInput(
            category=item.category,
            from_activity=item.from_activity,
            to_activity=item.to_activity,
            quantity=item.quantity,
            unit=item.unit,
            region=item.region,
        )
        for item in payload.changes
    ]

    try:
        return run_simulation(
            user_id=payload.user_id,
            changes=change_inputs,
            db=db,
        )
    except UserNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except EmissionFactorNotFoundError as exc:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(exc),
        )
    except UnitMismatchError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
    except InvalidQuantityError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        )
