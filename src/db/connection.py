"""
Database connection and session management.

This module sets up:
- SQLAlchemy async engine
- Session factory
- Dependency injection for FastAPI

Compare to Rust:
- Like sqlx::PgPool in Rust
- Async engine similar to Tokio-based connection pool
- get_db() is like extracting State<PgPool> in Axum
"""

from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import Session

from config import settings
from models.user import Base


# Create async engine
# Compare to Rust: Like creating PgPool::connect()
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL queries in debug mode
    future=True
)

# Create session factory
# Compare to Rust: Like Arc<PgPool> that we clone for each request
AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency injection for database sessions.

    Yields a database session that will be automatically closed.

    Compare to Rust:
    - Like extracting State<PgPool> in Axum handlers
    - Automatically manages session lifecycle
    - FastAPI's Depends() system handles the cleanup

    Usage in FastAPI:
        @app.get("/users")
        async def get_users(db: AsyncSession = Depends(get_db)):
            # Use db here
            pass

    Yields:
        AsyncSession: Database session
    """
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()


async def init_db():
    """
    Initialize database - create all tables.

    This is mainly for testing. In production, use Alembic migrations.

    Compare to Rust:
    - Like running sqlx::migrate!() macro
    - Creates tables based on SQLAlchemy models
    - In Rust, you'd use SQLx migrations instead
    """
    async with engine.begin() as conn:
        # Use checkfirst=True to skip existing tables
        await conn.run_sync(Base.metadata.create_all)


async def drop_db():
    """
    Drop all database tables.

    Used for testing cleanup.

    Compare to Rust:
    - Like dropping the test database
    - Useful for clean test environments
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
