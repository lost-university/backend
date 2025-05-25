import base64
from collections.abc import Sequence
from uuid import UUID

from sqlmodel import Session, select
from sqlalchemy import func, and_

from ..models.plan import Plan
from ..schemas.plan import PlanCreate, PlanRead, PlanUpdate


def get_plans(user_id: UUID, session: Session) -> Sequence[PlanRead]:
    subquery = (
        select(
            Plan.group_version_id,
            func.max(Plan.created_at).label("max_created_at")
        )
        .where(Plan.user_id == user_id)
        .group_by(Plan.group_version_id)
        .subquery()
    )
    statement = (
        select(Plan)
        .join(subquery,
              and_(
                  Plan.group_version_id == subquery.c.group_version_id,
                  Plan.created_at == subquery.c.max_created_at
              ))
        .where(Plan.user_id == user_id)
    )
    plans = session.exec(statement).all()
    return [PlanRead.model_validate(plan) for plan in plans]


def get_plan_by_public_slug(public_slug: str, session: Session) -> PlanRead:
    statement = (
        select(Plan)
        .where(Plan.public_slug == public_slug)
        .order_by(Plan.created_at.desc())
    )
    plan = session.exec(statement).first()
    if not plan:
        error_msg = "Plan not found"
        raise ValueError(error_msg)
    return PlanRead.model_validate(plan)


def get_plan_history(user_id: UUID, plan_id: UUID, session: Session) -> Sequence[PlanRead]:
    current_plan = session.get(Plan, plan_id)
    statement = (
        select(Plan)
        .where(Plan.group_version_id == current_plan.group_version_id)
        .order_by(Plan.created_at.desc())
    )
    plans = session.exec(statement).all()
    return [PlanRead.model_validate(plan) for plan in plans]


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
    current_plan = session.get(Plan, plan_id)
    if not current_plan or current_plan.user_id != user_id:
        error_msg = "Plan not found or access denied"
        raise ValueError(error_msg)
    statement = select(Plan).where(Plan.group_version_id == current_plan.group_version_id)
    plan_group = session.exec(statement).all()
    for plan in plan_group:
        session.delete(plan)
        session.commit()


def create_public_slug(group_id: UUID) -> str:
    slug = base64.urlsafe_b64encode(group_id.bytes).rstrip(b'=').decode('ascii')
    return slug

def update_plan(user_id: UUID, plan_id: UUID, plan_data: PlanUpdate, session: Session) -> PlanRead:
    current_plan = session.get(Plan, plan_id)
    new_plan_data = {
        "group_version_id": current_plan.group_version_id,
        "name": current_plan.name,
        "content": plan_data.content,
        "public_slug": current_plan.public_slug,
        "is_favorite": current_plan.is_favorite,
        "user_id": user_id
    }
    new_plan = Plan(**new_plan_data)
    session.add(new_plan)
    session.commit()
    session.refresh(new_plan)
    return PlanRead.model_validate(new_plan)