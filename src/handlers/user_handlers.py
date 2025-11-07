"""
User CRUD handlers - Phase 2 Implementation 

This module contains the route handlers for user operations.

YOUR TASK:
Implement the following endpoints to make the tests in tests/test_users.py pass:

1. POST   /users       - Create a new user
2. GET    /users/{id}  - Get user by ID
3. GET    /users       - List users with pagination
4. PUT    /users/{id}  - Update user
5. DELETE /users/{id}  - Delete user

Compare to Rust:
- FastAPI router is like Axum's Router
- Path parameters use {id} syntax (like Axum)
- Depends() provides dependency injection (like State<T> in Axum)
- Return types are automatically serialized (like Json<T>)

TDD Workflow:
1. Run: pytest tests/test_users.py -v
2. Read the failing test to understand requirements
3. Implement the handler to make the test pass
4. Refactor and improve
5. Move to next test

Hints:
- Use FastAPI's APIRouter to organize routes
- Use Depends(get_db) to inject database session
- Use Pydantic models for request/response validation
- Handle exceptions and return appropriate HTTP status codes
- Use SQLAlchemy's select, insert, update, delete for queries
"""

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete, func
from uuid import UUID
from typing import List
from datetime import datetime, timezone

from db.connection import get_db
from models.user import User, UserCreate, UserUpdate, UserResponse

# Create router
router = APIRouter(prefix="/users", tags=["users"])


# ============================================================================
# Phase 2.1 - CREATE User
# ============================================================================

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    # Check for duplicate email - force fresh query with expire_all first
    db.expire_all()
    result = await db.execute(select(User).where(User.email == user_data.email))
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already exists")
        

    new_user = User(
        name=user_data.name,
        email=user_data.email
    )
    db.add(new_user)
    await db.flush()
    await db.refresh(new_user)
    return new_user
   


# ============================================================================
# Phase 2.3 - LIST Users (with pagination)
# ============================================================================

@router.get("", response_model=dict)
async def list_users(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    db: AsyncSession = Depends(get_db)
):
    """
    List users with pagination.

    Test file: tests/test_users.py::TestListUsers

    Requirements:
    - Accept page and page_size query parameters
    - Return paginated list of users
    - Include pagination metadata (total, page, page_size)
    - Order by created_at descending

    Response format:
    {
        "users": [...],
        "total": 100,
        "page": 1,
        "page_size": 10
    }

    Hints:
    - Use select(User).order_by(User.created_at.desc())
    - Use .offset((page - 1) * page_size)
    - Use .limit(page_size)
    - Get total count with select(func.count(User.id))
    """
    db.expire_all()
    # 1. Get total count
    count_result = await db.execute(select(func.count(User.id)))
    total = count_result.scalar()

    # 2. Query paginated users
    offset = (page - 1) * page_size
    query = select(User).order_by(User.created_at.desc()).offset(offset).limit(page_size)
    result = await db.execute(query)
    users = result.scalars().all()

    # 3. Convert User objects to UserResponse
    users_response = [UserResponse.model_validate(user) for user in users]

    # 4. Return dict with users and metadata
    return {
        "users": users_response,
        "total": total,
        "page": page,
        "page_size": page_size
    }


# ============================================================================
# Phase 2.2 - READ User
# ============================================================================

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    # Force fresh query to see data from previous requests in same test
    db.expire_all()
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user


# ============================================================================
# TODO: Phase 2.4 - UPDATE User
# ============================================================================

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    db.expire_all()
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_data.model_dump(exclude_unset=True)

    if "email" in update_data:
        result = await db.execute(
            select(User).where(
                User.email == update_data["email"],
                User.id != user_id 
            )
        )
        existing_user = result.scalar_one_or_none()
        
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already exists")
    
    for key, value in update_data.items():
        setattr(user, key, value)

    user.updated_at = datetime.now(timezone.utc)

    await db.flush()
    await db.refresh(user)

    return user


# ============================================================================
# TODO: Phase 2.5 - DELETE User
# ============================================================================

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Delete a user.

    Test file: tests/test_users.py::TestDeleteUser

    Requirements:
    - Accept UUID path parameter
    - Delete user from database
    - Return 404 if user not found
    - Return 204 (no content) on success

    Hints:
    - First check if user exists
    - Use delete().where() or db.delete()
    - Return Response(status_code=204) or just return None with status_code set in decorator
    """
    # TODO: Implement user deletion
    # 1. Find user by ID (404 if not found)
    # 2. Delete from database
    # 3. Return 204
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User deletion not implemented yet. Check tests/test_users.py for requirements."
    )


# ============================================================================
# Integration with main.py
# ============================================================================

# To use these handlers in main.py, add this line:
# from handlers.user_handlers import router as user_router
# app.include_router(user_router)
