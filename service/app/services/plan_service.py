from typing import Sequence
from uuid import UUID

from sqlmodel import Session, select

from ..models.plan import Plan


def get_plans(id: UUID, session: Session) -> Sequence[Plan]:
    statement = select(Plan).where(Plan.user_id == id)
    
    return session.exec(statement).all()