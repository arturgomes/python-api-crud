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


@pytest.fixture(scope="session")
def event_loop():
    """
    Create an event loop for the entire test session.

    Compare to Rust:
    - Like #[tokio::test] but for all tests
    - pytest-asyncio needs this for async tests
    """
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session for each test.

    Compare to Rust:
    - Like creating a test PgPool in Rust
    - Each test gets a fresh session
    - Automatically rolls back after test

    Yields:
        AsyncSession: Database session for testing
    """
    # Create tables
    await init_db()

    async with AsyncSessionLocal() as session:
        yield session
        # Rollback any changes made during the test
        await session.rollback()

    # Drop tables after test
    await drop_db()


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

    async with AsyncClient(app=app, base_url="http://test") as ac:
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
