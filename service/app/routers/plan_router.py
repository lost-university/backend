from collections.abc import Sequence
from typing import Annotated

from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from ..database import get_session
from ..middlewares.auth_middleware import auth_dependency
from ..schemas.plan import PlanRead
from ..services import plan_service

router = APIRouter()


@router.get("/plans", dependencies=[Depends(auth_dependency)])
async def get_plans(
    request: Request, session: Annotated[Session, Depends(get_session)]
) -> dict[str, Sequence[PlanRead]]:
    plans = plan_service.get_plans(request.state.user.id, session)
    return {"plans": plans}


@router.post("/plans", dependencies=[Depends(auth_dependency)], status_code=status.HTTP_201_CREATED)
async def create_plan(
    plan_data: PlanCreate,
    request: Request,
    session: Annotated[Session, Depends(get_session)]
) -> PlanRead:
    try:
        created_plan = plan_service.write_plan(plan_data, session)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create plan"
        ) from e
    return PlanRead.from_orm(created_plan)
