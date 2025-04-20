from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan


def get_plans(plan_id: UUID, session: Session) -> Sequence[Plan]:
    statement = select(Plan).where(Plan.user_id == plan_id)

    return session.exec(statement).all()


def write_plan(plan: Plan, session: Session) -> Plan:
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan
