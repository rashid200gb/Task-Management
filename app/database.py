"""
Database connection — targets Neon (PostgreSQL) in production,
falls back to SQLite in-memory for tests.

Usage:
  Production (Neon):
    DATABASE_URL=postgresql+psycopg2://user:pass@ep-xxx.us-east-2.aws.neon.tech/taskdb?sslmode=require

  Tests:
    DATABASE_URL=sqlite:///./test.db   (set in conftest.py fixture)
"""
import os
from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL: str = os.environ.get(
    "DATABASE_URL",
    "sqlite:///./tasks.db"  # local fallback when no env var set
)

# SQLite needs check_same_thread=False; PostgreSQL ignores this arg
connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

engine = create_engine(DATABASE_URL, connect_args=connect_args, echo=False)


def create_db_and_tables() -> None:
    """Create all tables (idempotent — skips if already exist)."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """FastAPI dependency: yields a database session per request."""
    with Session(engine) as session:
        yield session
