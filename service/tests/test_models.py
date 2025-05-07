"""
Tests for the models.

This module tests the models defined in the app/models directory.
"""

import uuid
from datetime import datetime

from sqlmodel import Session, SQLModel, select

from app.models.plan import Plan
from app.models.user import User


def test_user_model(engine):
    """Test the User model."""
    # Create an in-memory database for testing
    SQLModel.metadata.create_all(engine)

    # Create a test user
    user_id = uuid.uuid4()
    clerk_id = "test_clerk_id"
    email = "test@example.com"

    user = User(
        id=user_id,
        clerk_id=clerk_id,
        email=email
    )

    # Test that the user attributes are set correctly
    assert user.id == user_id
    assert user.clerk_id == clerk_id
    assert user.email == email

    # Test that the user can be saved to the database
    with Session(engine) as session:
        session.add(user)
        session.commit()
        session.refresh(user)

        # Retrieve the user from the database
        db_user = session.get(User, user_id)
        assert db_user is not None
        assert db_user.id == user_id
        assert db_user.clerk_id == clerk_id
        assert db_user.email == email


def test_plan_model(engine):
    """Test the Plan model."""
    # Create an in-memory database for testing
    SQLModel.metadata.create_all(engine)

    # Create a test user
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        clerk_id="test_clerk_id",
        email="test@example.com"
    )

    # Create a test plan
    plan_id = uuid.uuid4()
    group_version_id = uuid.uuid4()
    name = "Test Plan"
    content = "Test Content"
    is_favorite = True
    created_at = datetime.now()

    plan = Plan(
        id=plan_id,
        group_version_id=group_version_id,
        name=name,
        content=content,
        is_favorite=is_favorite,
        created_at=created_at,
        user_id=user_id
    )

    # Test that the plan attributes are set correctly
    assert plan.id == plan_id
    assert plan.group_version_id == group_version_id
    assert plan.name == name
    assert plan.content == content
    assert plan.is_favorite == is_favorite
    assert plan.created_at == created_at
    assert plan.user_id == user_id
    
    # Test that the plan can be saved to the database
    with Session(engine) as session:
        # Add the user first (for foreign key constraint)
        session.add(user)
        session.commit()
        
        # Add the plan
        session.add(plan)
        session.commit()
        session.refresh(plan)
        
        # Retrieve the plan from the database
        db_plan = session.get(Plan, plan_id)
        assert db_plan is not None
        assert db_plan.id == plan_id
        assert db_plan.group_version_id == group_version_id
        assert db_plan.name == name
        assert db_plan.content == content
        assert db_plan.is_favorite == is_favorite
        assert db_plan.created_at == created_at
        assert db_plan.user_id == user_id


def test_plan_default_values():
    """Test the default values for the Plan model."""
    # Create a test plan with minimal required fields
    user_id = uuid.uuid4()
    name = "Test Plan"
    content = "Test Content"
    
    plan = Plan(
        name=name,
        content=content,
        user_id=user_id
    )
    
    # Test that the default values are set correctly
    assert plan.id is not None  # UUID should be generated
    assert plan.group_version_id is not None  # UUID should be generated
    assert plan.name == name
    assert plan.content == content
    assert plan.is_favorite is False  # Default value
    assert plan.created_at is not None  # Datetime should be generated
    assert plan.user_id == user_id


def test_plan_user_relationship(engine):
    """Test the relationship between Plan and User models."""
    # Create an in-memory database for testing
    SQLModel.metadata.create_all(engine)
    
    # Create a test user
    user_id = uuid.uuid4()
    user = User(
        id=user_id,
        clerk_id="test_clerk_id",
        email="test@example.com"
    )
    
    # Create test plans for the user
    plans = [
        Plan(name="Plan 1", content="Content 1", user_id=user_id),
        Plan(name="Plan 2", content="Content 2", user_id=user_id),
    ]
    
    # Save to the database
    with Session(engine) as session:
        session.add(user)
        session.commit()
        
        for plan in plans:
            session.add(plan)
        session.commit()
        
        # Query plans for the user
        statement = select(Plan).where(Plan.user_id == user_id)
        results = session.exec(statement).all()
        
        # Verify the results
        assert len(results) == 2
        for i, plan in enumerate(results):
            assert plan.name == plans[i].name
            assert plan.content == plans[i].content
            assert plan.user_id == user_id