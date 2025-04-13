from fastapi import APIRouter, Depends, Request
from sqlmodel import Session

from ..middlewares.auth_middleware import auth_dependency
from ..database import get_session
from ..services.plan_service import get_plans

router = APIRouter(
    #prefix="plan"
)

@router.get("/plans", dependencies=[Depends(auth_dependency)])
def get_plans(request: Request, session: Session = Depends(get_session)):
    plans = get_plans(request.state.user.id, session)
    return {"plans":plans}