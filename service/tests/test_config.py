"""
Test configuration and fixtures for the project.

This module provides fixtures and utilities for testing the application.
"""

import os
from typing import Annotated
import uuid
from unittest.mock import MagicMock, patch
from clerk_backend_api import Clerk

import pytest
from fastapi.testclient import TestClient
from fastapi import Request, Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.main import app
from app.models.user import User
from app.models.plan import Plan

from app.middlewares.auth_middleware import auth_dependency

mock_user = User(
    id=uuid.UUID("2f2129b5-388b-44c3-b125-0ffd3327587f"),
    clerk_id="clerk_id",
    email="test@example.com"
)


# Use an in-memory SQLite database for testing
@pytest.fixture(name="engine")
def engine_fixture():
    """Create an SQLite in-memory database engine for testing."""
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    return engine

def get_session(session_fixture):
    yield session_fixture

@pytest.fixture(name="session")
def session_fixture(engine):
    """Create a database session for testing."""
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture():
    """Create a FastAPI TestClient for testing API endpoints."""
    return TestClient(app)


@pytest.fixture(name="user")
def user_fixture():
    return mock_user


@pytest.fixture(name="test_plan")
def test_plan_fixture(user, session):
    """Create a test plan for testing."""
    plan = Plan(
        name="Test Plan",
        content="Test Content",
        is_favorite=False,
        user_id=user.id
    )
    session.add(plan)
    session.commit()
    session.refresh(plan)
    return plan


async def override_auth_dependency(session: Annotated[Session, Depends(get_session)]) -> Request:
    session.add(mock_user)
    session.commit()
    user = session.refresh(mock_user)
    request: Request
    request.state.user = user
    return request


app.dependency_overrides[auth_dependency] = override_auth_dependency
