from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session

from ..database import get_session
from ..middlewares.auth_middleware import auth_dependency
from ..schemas.plan import PlanCreate, PlanRead
from ..services import plan_service

router = APIRouter()


@router.get("/api/plans", dependencies=[Depends(auth_dependency)])
async def get_plans(
    request: Request, session: Annotated[Session, Depends(get_session)]
) -> dict[str, Sequence[PlanRead]]:
    plans = plan_service.get_plans(request.state.user.id, session)
    return {"plans": plans}


@router.post("/api/plan", dependencies=[Depends(auth_dependency)], status_code=201)
async def create_plan(plan_data: PlanCreate, session: Annotated[Session, Depends(get_session)]) -> PlanRead:
    try:
        created_plan = plan_service.write_plan(plan_data, session)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create plan: {str(e)}") from e
    return PlanRead.model_validate(created_plan)
