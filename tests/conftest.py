"""
pytest configuration and fixtures.

This file contains shared test fixtures used across all tests.

Compare to Rust:
- Like test helper functions and setup in Rust tests
- pytest fixtures provide dependency injection for tests
- More powerful than Rust's #[test] setup
"""

import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

# Import after adding src to path
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from main import app
from db.connection import engine, AsyncSessionLocal, get_db, init_db, drop_db


@pytest.fixture(scope="session", autouse=True)
async def setup_database():
    """
    Set up database once for all tests.

    Compare to Rust:
    - Like setting up test database once before all tests
    - More efficient than per-test setup
    """
    # Create tables once
    await init_db()
    yield
    # Drop tables after all tests
    await drop_db()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for each test with transaction rollback.

    Compare to Rust:
    - Like creating a test PgPool in Rust
    - Each test gets isolated session with automatic rollback
    - Ensures test isolation without recreating tables

    Yields:
        AsyncSession: Database session for testing
    """
    async with AsyncSessionLocal() as session:
        # Start a transaction
        async with session.begin():
            yield session
            # Rollback happens automatically when exiting the context


@pytest.fixture(scope="function")
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """
    Provide an HTTP client for testing the API.

    Compare to Rust:
    - Like reqwest::Client in Rust integration tests
    - Uses FastAPI's TestClient under the hood
    - Automatically uses test database

    Args:
        db_session: Database session fixture

    Yields:
        AsyncClient: HTTP client for making API requests
    """
    # Override the get_db dependency to use test database
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db

    from httpx import ASGITransport
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac

    # Clear overrides after test
    app.dependency_overrides.clear()


@pytest.fixture
def sample_user_data():
    """
    Provide sample user data for tests.

    Compare to Rust:
    - Like const TEST_USER in Rust tests
    - Reusable test data
    """
    return {
        "name": "Alice Johnson",
        "email": "alice@example.com"
    }


@pytest.fixture
def sample_users_data():
    """
    Provide multiple sample users for pagination tests.

    Compare to Rust:
    - Like vec![User {...}, User {...}] in Rust tests
    - Used for testing list endpoints
    """
    return [
        {"name": "Alice Johnson", "email": "alice@example.com"},
        {"name": "Bob Smith", "email": "bob@example.com"},
        {"name": "Charlie Brown", "email": "charlie@example.com"},
        {"name": "Diana Prince", "email": "diana@example.com"},
        {"name": "Eve Wilson", "email": "eve@example.com"},
    ]
