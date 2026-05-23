import base64
import uuid
from collections.abc import Sequence

import pytest
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, select

from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanRead, PlanUpdate
from app.services.plan_service import (
    bookmark_plan,
    create_public_slug,
    delete_plan,
    get_plan_by_public_slug,
    get_plan_history,
    write_plan,
)


def _create_inmemory_session() -> Session:
    engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)
    SQLModel.metadata.create_all(engine)
    return Session(engine)


def test_create_public_slug_roundtrip() -> None:
    group_id = uuid.uuid4()
    slug = create_public_slug(group_id)
    # add padding to be decodable
    padded = slug + "=" * (-len(slug) % 4)
    decoded = base64.urlsafe_b64decode(padded.encode("ascii"))
    assert decoded == group_id.bytes


def test_write_and_get_plan_by_public_slug() -> None:
    session = _create_inmemory_session()

    user_id = uuid.uuid4()
    plan_data = PlanCreate(name="Unit Test", content="content")
    created = write_plan(user_id, plan_data, session)
    assert isinstance(created, PlanRead)

    fetched = get_plan_by_public_slug(created.public_slug, session)
    assert fetched.name == "Unit Test"
    assert fetched.content == "content"


def test_get_plan_by_public_slug_not_found_raises() -> None:
    session = _create_inmemory_session()
    with pytest.raises(ValueError, match="Plan not found"):
        get_plan_by_public_slug("nonexistentslug", session)


def test_bookmark_and_delete_plan_group() -> None:
    session = _create_inmemory_session()

    user_id = uuid.uuid4()
    plan_data = PlanCreate(name="Group Plan", content="v1")
    first = write_plan(user_id, plan_data, session)

    # create a second version (same group_version_id) via update flow
    update = PlanUpdate(content="v2")
    # emulate update_plan behavior by creating new Plan with same group_version_id
    current = session.get(Plan, first.id)
    new_plan = Plan(
        group_version_id=current.group_version_id,
        name=current.name,
        content=update.content,
        public_slug=current.public_slug,
        bookmark=current.bookmark,
        user_id=user_id,
    )
    session.add(new_plan)
    session.commit()

    # bookmark the latest plan
    bookmark_plan(user_id, new_plan.id, session)
    refreshed = session.get(Plan, new_plan.id)
    assert refreshed.bookmark is True

    # toggle back
    bookmark_plan(user_id, new_plan.id, session)
    refreshed = session.get(Plan, new_plan.id)
    assert refreshed.bookmark is False

    # delete by user should remove both versions in the group
    delete_plan(user_id, new_plan.id, session)
    remaining = session.exec(select(Plan)).all()
    assert len(remaining) == 0


def test_bookmark_plan_access_denied() -> None:
    session = _create_inmemory_session()
    user_id = uuid.uuid4()
    other_user = uuid.uuid4()
    plan_data = PlanCreate(name="Private", content="x")
    created = write_plan(user_id, plan_data, session)

    with pytest.raises(ValueError, match="access denied"):
        bookmark_plan(other_user, created.id, session)


def test_get_plan_history_returns_versions() -> None:
    session = _create_inmemory_session()
    user_id = uuid.uuid4()
    plan_data = PlanCreate(name="Hist", content="a")
    first = write_plan(user_id, plan_data, session)

    # create another version
    update = PlanUpdate(content="b")
    current = session.get(Plan, first.id)
    new_plan = Plan(
        group_version_id=current.group_version_id,
        name=current.name,
        content=update.content,
        public_slug=current.public_slug,
        bookmark=current.bookmark,
        user_id=user_id,
    )
    session.add(new_plan)
    session.commit()

    history = get_plan_history(new_plan.id, session)
    assert isinstance(history, Sequence)
    assert len(history) >= 2
