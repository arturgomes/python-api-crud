"""
Phase 0: Calculator API Tests

These tests verify the calculator endpoint works correctly.
This is your first working example to understand the testing pattern.

Compare to Rust:
- Similar to Rust integration tests
- Uses httpx.AsyncClient like reqwest in Rust
- pytest fixtures provide test setup/teardown
"""

import pytest
from httpx import AsyncClient


class TestCalculator:
    """Test suite for calculator endpoint."""

    @pytest.mark.asyncio
    async def test_root_endpoint(self, client: AsyncClient):
        """
        Test the root endpoint returns welcome message.

        Compare to Rust:
        - Like #[tokio::test] async fn test_root()
        - client.get() is like reqwest::get()
        """
        response = await client.get("/")
        assert response.status_code == 200

        data = response.json()
        assert "message" in data
        assert "version" in data
        assert "phase" in data

    @pytest.mark.asyncio
    async def test_addition(self, client: AsyncClient):
        """Test addition operation."""
        response = await client.get("/calculate?a=10&b=5&op=add")
        assert response.status_code == 200

        data = response.json()
        assert data["result"] == 15.0

    @pytest.mark.asyncio
    async def test_subtraction(self, client: AsyncClient):
        """Test subtraction operation."""
        response = await client.get("/calculate?a=10&b=5&op=subtract")
        assert response.status_code == 200

        data = response.json()
        assert data["result"] == 5.0

    @pytest.mark.asyncio
    async def test_multiplication(self, client: AsyncClient):
        """Test multiplication operation."""
        response = await client.get("/calculate?a=10&b=5&op=multiply")
        assert response.status_code == 200

        data = response.json()
        assert data["result"] == 50.0

    @pytest.mark.asyncio
    async def test_division(self, client: AsyncClient):
        """Test division operation."""
        response = await client.get("/calculate?a=10&b=5&op=divide")
        assert response.status_code == 200

        data = response.json()
        assert data["result"] == 2.0

    @pytest.mark.asyncio
    async def test_division_by_zero(self, client: AsyncClient):
        """
        Test that division by zero returns error.

        Compare to Rust:
        - Like testing for Err(AppError::DivisionByZero)
        - HTTP 400 error with error message
        """
        response = await client.get("/calculate?a=10&b=0&op=divide")
        assert response.status_code == 400

        data = response.json()
        assert "detail" in data
        assert "zero" in data["detail"].lower()

    @pytest.mark.asyncio
    async def test_invalid_operation(self, client: AsyncClient):
        """Test that invalid operation returns error."""
        response = await client.get("/calculate?a=10&b=5&op=invalid")
        assert response.status_code == 422  # FastAPI validation error

    @pytest.mark.asyncio
    async def test_missing_parameters(self, client: AsyncClient):
        """Test that missing parameters return error."""
        response = await client.get("/calculate?a=10&op=add")
        assert response.status_code == 422  # FastAPI validation error

    @pytest.mark.asyncio
    @pytest.mark.parametrize("a,b,op,expected", [
        (5, 3, "add", 8.0),
        (5, 3, "subtract", 2.0),
        (5, 3, "multiply", 15.0),
        (6, 3, "divide", 2.0),
        (-5, 3, "add", -2.0),
        (0, 5, "multiply", 0.0),
    ])
    async def test_calculator_parametrized(
        self,
        client: AsyncClient,
        a: float,
        b: float,
        op: str,
        expected: float
    ):
        """
        Parametrized test for multiple calculator scenarios.

        Compare to Rust:
        - pytest.mark.parametrize is more powerful than Rust's test cases
        - Automatically generates multiple test cases
        - Each parameter combination is a separate test
        """
        response = await client.get(f"/calculate?a={a}&b={b}&op={op}")
        assert response.status_code == 200

        data = response.json()
        assert data["result"] == expected
