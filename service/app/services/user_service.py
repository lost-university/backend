from sqlmodel import Session, select

from ..models.user import User


def get_user_by_clerk_id(clerk_id: str, session: Session) -> User | None:
    statement = select(User).where(User.clerk_id == clerk_id)

    return session.exec(statement).first()


def create_user(clerk_id: str, email: str, session: Session) -> User:
    user = User(clerk_id=clerk_id, email=email)

    session.add(user)
    session.commit()
    session.refresh(user)

    return user
