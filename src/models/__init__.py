"""
Models package.

Contains both:
- SQLAlchemy models (database tables)
- Pydantic models (request/response schemas)

Compare to Rust:
- SQLAlchemy models are like structs with SQLx annotations
- Pydantic models are like structs with serde(Serialize, Deserialize)
"""

from .user import User, UserCreate, UserUpdate, UserResponse

__all__ = ["User", "UserCreate", "UserUpdate", "UserResponse"]
