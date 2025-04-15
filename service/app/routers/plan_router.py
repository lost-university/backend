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
async def get_plans(request: Request, session: Annotated[Session, Depends(get_session)]) -> dict[str, Sequence[PlanRead]]:
    plans = plan_service.get_plans(request.state.user.id, session)
    return {"plans":plans}
