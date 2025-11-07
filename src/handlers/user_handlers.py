"""
User CRUD handlers - Phase 2 Implementation (TODO)

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
from sqlalchemy import select, insert, update, delete
from uuid import UUID
from typing import List

from db.connection import get_db
from models.user import User, UserCreate, UserUpdate, UserResponse

# Create router
router = APIRouter(prefix="/users", tags=["users"])


# ============================================================================
# TODO: Phase 2.1 - CREATE User
# ============================================================================

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Create a new user.

    Test file: tests/test_users.py::TestCreateUser

    Requirements:
    - Accept UserCreate model (name, email)
    - Validate email format (Pydantic does this automatically)
    - Check for duplicate email (return 400 if exists)
    - Insert into database
    - Return UserResponse with all fields including id and timestamps

    Hints:
    - Use SQLAlchemy's select to check for existing email
    - Use insert() or db.add() to create user
    - Catch IntegrityError for unique constraint violations
    - Don't forget db.commit() and db.refresh() to get generated fields
    """
    # TODO: Implement user creation
    # 1. Check if email already exists
    # 2. Create new user
    # 3. Save to database
    # 4. Return UserResponse
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User creation not implemented yet. Check tests/test_users.py for requirements."
    )


# ============================================================================
# TODO: Phase 2.2 - READ User
# ============================================================================

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    """
    Get a user by ID.

    Test file: tests/test_users.py::TestGetUser

    Requirements:
    - Accept UUID path parameter
    - Query database for user
    - Return 404 if user not found
    - Return UserResponse if found

    Hints:
    - Use select(User).where(User.id == user_id)
    - Use db.execute() then .scalar_one_or_none()
    - Raise HTTPException(404) if user not found
    """
    # TODO: Implement user retrieval
    # 1. Query user by ID
    # 2. Return 404 if not found
    # 3. Return UserResponse if found
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User retrieval not implemented yet. Check tests/test_users.py for requirements."
    )


# ============================================================================
# TODO: Phase 2.3 - LIST Users (with pagination)
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
    # TODO: Implement user listing with pagination
    # 1. Get total count
    # 2. Query paginated users
    # 3. Return dict with users and metadata
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User listing not implemented yet. Check tests/test_users.py for requirements."
    )


# ============================================================================
# TODO: Phase 2.4 - UPDATE User
# ============================================================================

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Update a user.

    Test file: tests/test_users.py::TestUpdateUser

    Requirements:
    - Accept UUID path parameter
    - Accept UserUpdate model (optional name, optional email)
    - Only update fields that are provided (partial update)
    - Return 404 if user not found
    - Return 400 if email already exists (different user)
    - Return updated UserResponse

    Hints:
    - First check if user exists
    - Build update dict with only provided fields: user_data.model_dump(exclude_unset=True)
    - Check for email uniqueness if email is being updated
    - Use update().where().values() or update object attributes
    - updated_at will be automatically updated by trigger
    """
    # TODO: Implement user update
    # 1. Find user by ID (404 if not found)
    # 2. Check for duplicate email if updating email
    # 3. Update only provided fields
    # 4. Save and return updated user
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="User update not implemented yet. Check tests/test_users.py for requirements."
    )


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
