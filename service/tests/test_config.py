from typing import Annotated

import pytest
from fastapi import Depends, Request, HTTPException
from sqlmodel import Session
from fastapi.testclient import TestClient

from app.main import app
from app.database import get_session, create_db_and_tables, drop_tables
from app.middlewares.auth_middleware import auth_dependency
from app.services.user_service import create_user, get_user_by_clerk_id


CLERKID = "test_clerk_id"
AUTH_TOKEN = "test_auth_token"


@pytest.fixture(scope="function", autouse=True)
def db_session():
    create_db_and_tables()
    yield
    drop_tables()


@pytest.fixture
def test_client():
    return TestClient(app)


@pytest.fixture
def get_valid_auth_header():
    return {"Authorization": f"{AUTH_TOKEN}"}


async def override_auth_dependency(request: Request, session: Annotated[Session, Depends(get_session)]) -> Request:
    authorization = request.headers.get("Authorization")
    print(authorization)

    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    if authorization != AUTH_TOKEN:
        raise HTTPException(status_code=401, detail="Unauthorized")

    create_user(CLERKID, "test@email.com", session)
    user = get_user_by_clerk_id("test_clerk_id", session)

    request.state.user = user
    return request


app.dependency_overrides[auth_dependency] = override_auth_dependency
