"""
Phase 2: User CRUD API Tests (TDD)

These tests are PRE-WRITTEN to guide your implementation.
They will all fail initially. Your job is to make them pass one by one.

TDD Workflow:
1. 🔴 RED: Run tests, see them fail
2. 💡 UNDERSTAND: Read the test to understand requirements
3. 🟢 GREEN: Implement code to pass the test
4. 🔄 REFACTOR: Improve the code
5. ✅ VERIFY: Run tests again, move to next

Compare to Rust:
- Similar to Rust integration tests in tests/
- pytest is more flexible than Rust's built-in test framework
- Fixtures provide better test setup than Rust
"""

import pytest
from httpx import AsyncClient
from uuid import UUID


# ============================================================================
# Phase 2.1: CREATE User Tests
# ============================================================================

class TestCreateUser:
    """
    Tests for POST /users endpoint.

    TODO: Implement POST /users endpoint in src/handlers/user_handlers.py
    """

    @pytest.mark.asyncio
    async def test_create_user_success(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """
        Test successful user creation.

        Requirements:
        - POST /users with valid data should return 201
        - Response should include user with id, timestamps
        - User should be saved to database
        """
        response = await client.post("/users", json=sample_user_data)

        assert response.status_code == 201
        data = response.json()

        # Verify response structure
        assert "id" in data
        assert "name" in data
        assert "email" in data
        assert "created_at" in data
        assert "updated_at" in data

        # Verify data matches input
        assert data["name"] == sample_user_data["name"]
        assert data["email"] == sample_user_data["email"]

        # Verify id is valid UUID
        UUID(data["id"])  # Raises ValueError if invalid

    @pytest.mark.asyncio
    async def test_create_user_duplicate_email(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """
        Test that duplicate email returns error.

        Requirements:
        - First creation should succeed
        - Second creation with same email should return 400
        - Error message should indicate duplicate email
        """
        # First creation succeeds
        response1 = await client.post("/users", json=sample_user_data)
        assert response1.status_code == 201
        
        # Second creation with same email fails
        response2 = await client.post("/users", json=sample_user_data)
        assert response2.status_code == 400

        data = response2.json()
        assert "detail" in data
        assert "email" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_user_invalid_email(self, client: AsyncClient):
        """
        Test that invalid email returns validation error.

        Requirements:
        - Invalid email format should return 422
        - Pydantic should handle validation automatically
        """
        invalid_user = {
            "name": "Test User",
            "email": "not-an-email"
        }

        response = await client.post("/users", json=invalid_user)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_missing_name(self, client: AsyncClient):
        """Test that missing name returns validation error."""
        invalid_user = {
            "email": "test@example.com"
        }

        response = await client.post("/users", json=invalid_user)
        assert response.status_code == 422

    @pytest.mark.asyncio
    async def test_create_user_empty_name(self, client: AsyncClient):
        """Test that empty name returns validation error."""
        invalid_user = {
            "name": "",
            "email": "test@example.com"
        }

        response = await client.post("/users", json=invalid_user)
        assert response.status_code == 422


# ============================================================================
# Phase 2.2: READ User Tests
# ============================================================================

class TestGetUser:
    """
    Tests for GET /users/{id} endpoint.
    """

    @pytest.mark.asyncio
    async def test_get_user_success(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """
        Test successful user retrieval.

        Requirements:
        - GET /users/{id} should return 200
        - Response should match created user
        """
        # First create a user
        create_response = await client.post("/users", json=sample_user_data)
        assert create_response.status_code == 201
        created_user = create_response.json()

        # Then retrieve it
        user_id = created_user["id"]
        response = await client.get(f"/users/{user_id}")

        assert response.status_code == 200
        data = response.json()

        # Verify all fields match
        assert data["id"] == created_user["id"]
        assert data["name"] == created_user["name"]
        assert data["email"] == created_user["email"]
        assert data["created_at"] == created_user["created_at"]
        assert data["updated_at"] == created_user["updated_at"]

    @pytest.mark.asyncio
    async def test_get_user_not_found(self, client: AsyncClient):
        """
        Test that non-existent user returns 404.

        Requirements:
        - GET /users/{nonexistent-id} should return 404
        - Error message should be clear
        """
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        response = await client.get(f"/users/{fake_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data

    @pytest.mark.asyncio
    async def test_get_user_invalid_id(self, client: AsyncClient):
        """Test that invalid UUID returns error."""
        response = await client.get("/users/not-a-uuid")

        # FastAPI should return 422 for invalid UUID
        assert response.status_code == 422


# ============================================================================
# Phase 2.3: LIST Users Tests
# ============================================================================

class TestListUsers:
    """
    Tests for GET /users endpoint with pagination.
    """

    @pytest.mark.asyncio
    async def test_list_users_empty(self, client: AsyncClient):
        """
        Test listing users when database is empty.

        Requirements:
        - GET /users should return 200
        - Should return empty list
        - Should include pagination metadata
        """
        response = await client.get("/users")

        assert response.status_code == 200
        data = response.json()

        assert "users" in data
        assert isinstance(data["users"], list)
        assert len(data["users"]) == 0

        # Pagination metadata
        assert "total" in data
        assert data["total"] == 0
        assert "page" in data
        assert "page_size" in data

    @pytest.mark.asyncio
    async def test_list_users_with_data(
        self,
        client: AsyncClient,
        sample_users_data: list
    ):
        """
        Test listing users with data.

        Requirements:
        - Should return all users
        - Should include pagination metadata
        """
        # Create multiple users
        for user_data in sample_users_data:
            response = await client.post("/users", json=user_data)
            assert response.status_code == 201

        # List all users
        response = await client.get("/users")

        assert response.status_code == 200
        data = response.json()

        assert len(data["users"]) == len(sample_users_data)
        assert data["total"] == len(sample_users_data)

    @pytest.mark.asyncio
    async def test_list_users_pagination(
        self,
        client: AsyncClient,
        sample_users_data: list
    ):
        """
        Test pagination parameters.

        Requirements:
        - Should respect page and page_size parameters
        - Should return correct subset of users
        """
        # Create multiple users
        for user_data in sample_users_data:
            await client.post("/users", json=user_data)

        # Test pagination: page 1, size 2
        response = await client.get("/users?page=1&page_size=2")
        assert response.status_code == 200

        data = response.json()
        assert len(data["users"]) == 2
        assert data["page"] == 1
        assert data["page_size"] == 2
        assert data["total"] == len(sample_users_data)

        # Test pagination: page 2, size 2
        response = await client.get("/users?page=2&page_size=2")
        assert response.status_code == 200

        data = response.json()
        assert len(data["users"]) == 2
        assert data["page"] == 2

    @pytest.mark.asyncio
    async def test_list_users_last_page(
        self,
        client: AsyncClient,
        sample_users_data: list
    ):
        """Test that last page returns remaining users."""
        # Create users
        for user_data in sample_users_data:
            await client.post("/users", json=user_data)

        # Get last page (5 users, page_size=2, should have 1 user on page 3)
        response = await client.get("/users?page=3&page_size=2")
        assert response.status_code == 200

        data = response.json()
        assert len(data["users"]) == 1
        assert data["page"] == 3


# ============================================================================
# Phase 2.4: UPDATE User Tests
# ============================================================================

class TestUpdateUser:
    """
    Tests for PUT /users/{id} endpoint.
    """

    @pytest.mark.asyncio
    async def test_update_user_name(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """
        Test updating user name.

        Requirements:
        - PUT /users/{id} should return 200
        - Should update only specified fields
        - updated_at should change
        """
        # Create user
        create_response = await client.post("/users", json=sample_user_data)
        assert create_response.status_code == 201
        user = create_response.json()

        # Update name
        update_data = {"name": "Alice Smith"}
        response = await client.put(f"/users/{user['id']}", json=update_data)

        assert response.status_code == 200
        updated_user = response.json()

        assert updated_user["name"] == "Alice Smith"
        assert updated_user["email"] == user["email"]  # Email unchanged
        assert updated_user["updated_at"] != user["updated_at"]

    @pytest.mark.asyncio
    async def test_update_user_email(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test updating user email."""
        # Create user
        create_response = await client.post("/users", json=sample_user_data)
        user = create_response.json()

        # Update email
        update_data = {"email": "newemail@example.com"}
        response = await client.put(f"/users/{user['id']}", json=update_data)

        assert response.status_code == 200
        updated_user = response.json()

        assert updated_user["email"] == "newemail@example.com"
        assert updated_user["name"] == user["name"]  # Name unchanged

    @pytest.mark.asyncio
    async def test_update_user_both_fields(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test updating both name and email."""
        # Create user
        create_response = await client.post("/users", json=sample_user_data)
        user = create_response.json()

        # Update both fields
        update_data = {
            "name": "Bob Johnson",
            "email": "bob@example.com"
        }
        response = await client.put(f"/users/{user['id']}", json=update_data)

        assert response.status_code == 200
        updated_user = response.json()

        assert updated_user["name"] == "Bob Johnson"
        assert updated_user["email"] == "bob@example.com"

    @pytest.mark.asyncio
    async def test_update_user_not_found(self, client: AsyncClient):
        """Test updating non-existent user returns 404."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"
        update_data = {"name": "Test"}

        response = await client.put(f"/users/{fake_id}", json=update_data)
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_update_user_duplicate_email(
        self,
        client: AsyncClient,
        sample_users_data: list
    ):
        """Test that updating to existing email returns error."""
        # Create two users
        response1 = await client.post("/users", json=sample_users_data[0])
        user1 = response1.json()

        response2 = await client.post("/users", json=sample_users_data[1])
        user2 = response2.json()

        # Try to update user2's email to user1's email
        update_data = {"email": user1["email"]}
        response = await client.put(f"/users/{user2['id']}", json=update_data)

        assert response.status_code == 400


# ============================================================================
# Phase 2.5: DELETE User Tests
# ============================================================================

class TestDeleteUser:
    """
    Tests for DELETE /users/{id} endpoint.

    """

    @pytest.mark.asyncio
    async def test_delete_user_success(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """
        Test successful user deletion.

        Requirements:
        - DELETE /users/{id} should return 204
        - User should be removed from database
        - GET /users/{id} should return 404 after deletion
        """
        # Create user
        create_response = await client.post("/users", json=sample_user_data)
        user = create_response.json()

        # Delete user
        response = await client.delete(f"/users/{user['id']}")
        assert response.status_code == 204

        # Verify user is deleted
        get_response = await client.get(f"/users/{user['id']}")
        assert get_response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_user_not_found(self, client: AsyncClient):
        """Test deleting non-existent user returns 404."""
        fake_id = "123e4567-e89b-12d3-a456-426614174000"

        response = await client.delete(f"/users/{fake_id}")
        assert response.status_code == 404

    @pytest.mark.asyncio
    async def test_delete_user_idempotent(
        self,
        client: AsyncClient,
        sample_user_data: dict
    ):
        """Test that deleting same user twice returns 404 second time."""
        # Create user
        create_response = await client.post("/users", json=sample_user_data)
        user = create_response.json()

        # First deletion succeeds
        response1 = await client.delete(f"/users/{user['id']}")
        assert response1.status_code == 204

        # Second deletion returns 404
        response2 = await client.delete(f"/users/{user['id']}")
        assert response2.status_code == 404
