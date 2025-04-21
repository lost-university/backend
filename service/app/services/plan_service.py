from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan
from ..schemas.plan import PlanCreate


def get_plans(plan_id: UUID, session: Session) -> Sequence[Plan]:
    statement = select(Plan).where(Plan.user_id == plan_id)

    return session.exec(statement).all()


def write_plan(plan_data: PlanCreate, session: Session) -> Plan:
    plan = Plan(**plan_data.model_dump())
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
