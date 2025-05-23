import base64
from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan
from ..schemas.plan import PlanCreate, PlanRead


def get_plans(user_id: UUID, session: Session) -> Sequence[PlanRead]:
    statement = select(Plan).where(Plan.user_id == user_id)

    plans = session.exec(statement).all()
    return [PlanRead.model_validate(plan) for plan in plans]


def get_plan_by_public_slug(public_slug: str, session: Session) -> PlanRead:
    statement = select(Plan).where(Plan.public_slug == public_slug)
    plan = session.exec(statement).first()
    if not plan:
        error_msg = "Plan not found"
        raise ValueError(error_msg)
    return PlanRead.model_validate(plan)


def write_plan(user_id: UUID, plan_data: PlanCreate, session: Session) -> PlanRead:
    plan_dict = plan_data.model_dump()
    plan_dict["user_id"] = user_id
    created_plan = Plan(**plan_dict)
    created_plan.public_slug = create_public_slug(created_plan.group_version_id)
    session.add(created_plan)
    session.commit()
    session.refresh(created_plan)
    return PlanRead.model_validate(created_plan)


def delete_plan(user_id: UUID, plan_id: UUID, session: Session) -> None:
    plan = session.get(Plan, plan_id)
    if not plan or plan.user_id != user_id:
        error_msg = "Plan not found or access denied"
        raise ValueError(error_msg)
    session.delete(plan)
    session.commit()


def create_public_slug(group_id: UUID) -> str:
    slug = base64.urlsafe_b64encode(group_id.bytes).rstrip(b'=').decode('ascii')
    return slug
