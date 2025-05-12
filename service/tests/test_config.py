from collections.abc import Iterator
from typing import Annotated

import pytest
from fastapi import Depends, HTTPException, Request
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.database import create_db_and_tables, drop_tables, get_session
from app.main import app
from app.middlewares.auth_middleware import auth_dependency
from app.services.user_service import create_user, get_user_by_clerk_id

CLERKID = "test_clerk_id"
TEST_AUTH = "test_auth_token"


@pytest.fixture(autouse=True)
def db_session() -> Iterator[None]:
    create_db_and_tables()
    yield
    drop_tables()


@pytest.fixture
def test_client() -> TestClient:
    return TestClient(app)


@pytest.fixture
def get_valid_auth_header() -> dict[str, str]:
    return {"Authorization": f"{TEST_AUTH}"}


async def override_auth_dependency(request: Request, session: Annotated[Session, Depends(get_session)]) -> Request:
    authorization = request.headers.get("Authorization")
    print(authorization)

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if authorization != TEST_AUTH:
        raise HTTPException(status_code=401, detail="Unauthorized")

    create_user(CLERKID, "test@email.com", session)
    user = get_user_by_clerk_id("test_clerk_id", session)

    request.state.user = user
    return request


app.dependency_overrides[auth_dependency] = override_auth_dependency
