"""
Pytest configuration and fixtures for MCP tools tests
"""

import pytest
import os
import sys

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlmodel import SQLModel, Session, create_engine
from app.models.task import Task


# Use in-memory SQLite for tests
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture(scope="function")
def test_engine():
    """Create a test database engine."""
    engine = create_engine(TEST_DATABASE_URL, echo=False)
    SQLModel.metadata.create_all(engine)
    yield engine
    SQLModel.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def test_session(test_engine):
    """Create a test database session."""
    with Session(test_engine) as session:
        yield session


@pytest.fixture(scope="function")
def test_user_id():
    """Provide a test user ID."""
    return "test-user-123"


@pytest.fixture(scope="function")
def sample_tasks(test_session, test_user_id):
    """Create sample tasks for testing."""
    tasks = [
        Task(user_id=test_user_id, title="Buy groceries", description="Milk, eggs, bread"),
        Task(user_id=test_user_id, title="Call mom", description="Wish her happy birthday", completed=True),
        Task(user_id=test_user_id, title="Finish project", description="Complete Phase III implementation"),
    ]
    for task in tasks:
        test_session.add(task)
    test_session.commit()
    for task in tasks:
        test_session.refresh(task)
    return tasks
