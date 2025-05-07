"""
Tests for the plan router endpoints.

This module tests the API endpoints defined in plan_router.py.
"""
import uuid
import os
from unittest.mock import patch

import pytest
from fastapi import status
from sqlmodel import Session

from app.models.plan import Plan
from app.schemas.plan import PlanCreate

import pytest

def test_get_plans(test_plan, client):
    response = client.get("/api/plans")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == test_plan.name


def test_create_plan(client, mock_auth, session, monkeypatch):
    """Test the POST /api/plan endpoint."""
    # Create test data
    _, user_id = mock_auth
    plan_data = {
        "name": "New Plan",
        "content": "New Content",
        "is_favorite": True
    }

    # Mock the database session
    with patch("app.routers.plan_router.get_session") as mock_get_session:
        mock_get_session.return_value = session

        # Make the request
        response = client.post("/api/plan", json=plan_data)

        # Check the response
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["name"] == plan_data["name"]
        assert data["content"] == plan_data["content"]
        assert data["is_favorite"] == plan_data["is_favorite"]
        assert data["user_id"] == str(user_id)

        # Verify the plan was created in the database
        created_plan = session.get(Plan, uuid.UUID(data["id"]))
        assert created_plan is not None
        assert created_plan.name == plan_data["name"]
        assert created_plan.content == plan_data["content"]
        assert created_plan.is_favorite == plan_data["is_favorite"]
        assert created_plan.user_id == user_id


def test_delete_plan(client, mock_auth, session, test_plan):
    """Test the DELETE /api/plan/{plan_id} endpoint."""
    # Mock the database session
    with patch("app.routers.plan_router.get_session") as mock_get_session:
        mock_get_session.return_value = session

        # Make the request
        response = client.delete(f"/api/plan/{test_plan.id}")

        # Check the response
        assert response.status_code == status.HTTP_204_NO_CONTENT

        # Verify the plan was deleted from the database
        deleted_plan = session.get(Plan, test_plan.id)
        assert deleted_plan is None


def test_delete_plan_not_found(client, mock_auth, session):
    """Test the DELETE /api/plan/{plan_id} endpoint with a non-existent plan."""
    # Generate a random UUID that doesn't exist
    non_existent_id = uuid.uuid4()

    # Mock the database session
    with patch("app.routers.plan_router.get_session") as mock_get_session:
        mock_get_session.return_value = session

        # Make the request
        response = client.delete(f"/api/plan/{non_existent_id}")

        # Check the response
        assert response.status_code == status.HTTP_404_NOT_FOUND
