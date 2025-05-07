"""
Pytest configuration file.

This file is automatically discovered by pytest and makes fixtures available to all test files.
"""

# Import fixtures from test_config.py to make them available to all tests
from .test_config import (
    engine_fixture as engine,
    session_fixture as session,
    client_fixture as client,
    test_plan_fixture as test_plan,
    user_fixture as user
)