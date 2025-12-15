"""
Database connection and session management
Task: T-004 - Initialize Database Connection
"""

from sqlmodel import create_engine, Session, SQLModel
from typing import Generator
from backend.app.core.config import settings


# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=True,  # Log SQL statements (set to False in production)
    pool_pre_ping=True,  # Verify connections before using
)


def create_db_and_tables():
    """Create all database tables based on SQLModel metadata"""
    SQLModel.metadata.create_all(engine)


def get_session() -> Generator[Session, None, None]:
    """
    Dependency function to get database session.
    Use with FastAPI's Depends() for dependency injection.

    Yields:
        Session: SQLModel database session
    """
    with Session(engine) as session:
        yield session
