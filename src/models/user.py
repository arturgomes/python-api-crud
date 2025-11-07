"""
User models - both database (SQLAlchemy) and API (Pydantic) models.

This module contains:
1. User (SQLAlchemy) - Database table definition
2. UserCreate (Pydantic) - Request body for creating users
3. UserUpdate (Pydantic) - Request body for updating users
4. UserResponse (Pydantic) - Response body for user data

Compare to Rust:
- SQLAlchemy User is like a struct with sqlx::FromRow
- Pydantic models are like structs with serde
- Python uses two separate model types (DB vs API)
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base

# Base class for SQLAlchemy models
Base = declarative_base()


# ============================================================================
# SQLAlchemy Model (Database)
# ============================================================================

class User(Base):
    """
    SQLAlchemy model representing the users table.

    Compare to Rust:
    - Like a struct with #[derive(FromRow)]
    - Defines the database schema
    - Used by SQLAlchemy ORM for queries

    Attributes:
        id: Primary key (UUID)
        name: User's name
        email: User's email (unique)
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    id = Column(
        PGUUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        nullable=False
    )
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )
    updated_at = Column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<User(id={self.id}, name={self.name}, email={self.email})>"


# ============================================================================
# Pydantic Models (API Schemas)
# ============================================================================

class UserBase(BaseModel):
    """
    Base Pydantic model with common user fields.

    Compare to Rust:
    - Like a base struct for other user types
    - DRY principle: shared fields defined once
    """
    name: str = Field(..., min_length=1, max_length=255, description="User's name")
    email: EmailStr = Field(..., description="User's email address")

    class Config:
        from_attributes = True  # Allows creating from SQLAlchemy models
        json_schema_extra = {
            "example": {
                "name": "Alice Johnson",
                "email": "alice@example.com"
            }
        }


class UserCreate(UserBase):
    """
    Pydantic model for creating a new user.

    Compare to Rust:
    - Like a struct with #[derive(Deserialize)]
    - Used to validate POST /users request body
    - Automatically validated by FastAPI

    Example:
        POST /users
        {
            "name": "Alice Johnson",
            "email": "alice@example.com"
        }
    """
    pass


class UserUpdate(BaseModel):
    """
    Pydantic model for updating a user.

    Compare to Rust:
    - Like a struct with Option<T> fields
    - All fields optional for partial updates
    - Used to validate PUT /users/{id} request body

    Example:
        PUT /users/{id}
        {
            "name": "Alice Smith"  # Only update name
        }
    """
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    email: Optional[EmailStr] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Alice Smith"
            }
        }


class UserResponse(UserBase):
    """
    Pydantic model for user responses.

    Compare to Rust:
    - Like a struct with #[derive(Serialize)]
    - Used for GET /users/{id} and other responses
    - Automatically serialized to JSON by FastAPI

    Attributes:
        id: User's unique identifier
        name: User's name
        email: User's email
        created_at: When the user was created
        updated_at: When the user was last updated
    """
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Can be created from SQLAlchemy User
        json_schema_extra = {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Alice Johnson",
                "email": "alice@example.com",
                "created_at": "2024-01-01T12:00:00Z",
                "updated_at": "2024-01-01T12:00:00Z"
            }
        }
