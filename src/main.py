"""
Main application module - Phase 0: Calculator API

This is the entry point for the FastAPI application.
Starting with a simple calculator to learn the patterns before building the full CRUD API.

Learning Goals:
1. FastAPI setup and routing
2. Query parameters and validation
3. Error handling patterns
4. JSON responses
5. Testing patterns with pytest

Compare to Rust:
- FastAPI is like Axum (async web framework)
- Type hints replace Rust's strict typing (but less strict)
- Pydantic handles serialization (like serde)
- asyncio is like Tokio (but different model)
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, ConfigDict
from enum import Enum
from typing import Optional
import uvicorn

from config import settings


# ============================================================================
# PHASE 0: CALCULATOR API
# ============================================================================

class Operation(str, Enum):
    """
    Enum for calculator operations.

    Compare to Rust:
    - Similar to Rust's enum, but simpler
    - str, Enum gives us string-based enum
    - FastAPI automatically validates against these values
    """
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"
    DIVIDE = "divide"


class CalculatorResponse(BaseModel):
    """
    Response model for calculator.

    Compare to Rust:
    - Like a struct with #[derive(Serialize)]
    - Pydantic handles JSON serialization automatically
    - Type hints provide validation
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "result": 15.0
            }
        }
    )

    result: float


class ErrorResponse(BaseModel):
    """
    Error response model.

    Compare to Rust:
    - Like Result<T, E> but for HTTP responses
    - FastAPI automatically formats errors
    """
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "error": "Division by zero"
            }
        }
    )

    error: str


# Create FastAPI application
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="A TDD-driven CRUD API for learning Python",
    debug=settings.DEBUG
)

# Add CORS middleware
# Compare to Rust: Similar to tower_http::cors in Axum
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """
    Root endpoint - health check.

    Compare to Rust:
    - async fn in Rust is async def in Python
    - Return value is automatically serialized to JSON
    - No explicit Result<Json<Value>, Error> needed
    """
    return {
        "message": f"Welcome to {settings.APP_NAME}",
        "version": settings.APP_VERSION,
        "phase": "0 - Calculator API",
        "docs": "/docs"  # FastAPI auto-generates OpenAPI docs!
    }


@app.get(
    "/calculate",
    response_model=CalculatorResponse,
    responses={400: {"model": ErrorResponse}}
)
async def calculate(
    a: float = Query(..., description="First number"),
    b: float = Query(..., description="Second number"),
    op: Operation = Query(..., description="Operation to perform")
) -> CalculatorResponse:
    """
    Calculator endpoint - Phase 0 example.

    Args:
        a: First number
        b: Second number
        op: Operation (add, subtract, multiply, divide)

    Returns:
        CalculatorResponse with result

    Raises:
        HTTPException: If division by zero

    Compare to Rust:
    - Query(...) is like extracting query params in Axum
    - Type hints provide validation (Pydantic)
    - HTTPException is like returning Err(AppError)
    - No need for explicit Json<> wrapping

    Example:
        GET /calculate?a=10&b=5&op=add
        Response: {"result": 15.0}
    """
    # Perform calculation based on operation
    # Compare to Rust: Similar to match statement
    if op == Operation.ADD:
        result = a + b
    elif op == Operation.SUBTRACT:
        result = a - b
    elif op == Operation.MULTIPLY:
        result = a * b
    elif op == Operation.DIVIDE:
        # Error handling
        # Compare to Rust: Like returning Err(...)
        if b == 0:
            raise HTTPException(
                status_code=400,
                detail="Division by zero"
            )
        result = a / b
    else:
        # This shouldn't happen due to Enum validation
        raise HTTPException(
            status_code=400,
            detail=f"Invalid operation: {op}"
        )

    return CalculatorResponse(result=result)


# ============================================================================
# PHASE 2: USER CRUD API (TODO)
# ============================================================================

# TODO: Phase 2 - Add user routes here
# The tests in tests/test_users.py will guide you through implementation
#
# You'll add:
# - POST   /users       - Create user
# - GET    /users/{id}  - Get user by ID
# - GET    /users       - List users with pagination
# - PUT    /users/{id}  - Update user
# - DELETE /users/{id}  - Delete user


# ============================================================================
# APPLICATION ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    """
    Run the application.

    Compare to Rust:
    - Similar to tokio::main + axum::serve
    - uvicorn is like the Tokio runtime
    - Auto-reloads on code changes in debug mode
    """
    print(f"🚀 {settings.APP_NAME} v{settings.APP_VERSION}")
    print(f"📍 Starting server on http://{settings.HOST}:{settings.PORT}")
    print(f"📖 API docs available at http://localhost:{settings.PORT}/docs")
    print(f"🧪 Try: http://localhost:{settings.PORT}/calculate?a=5&b=3&op=add")
    print()

    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,  # Auto-reload on code changes
        log_level="info"
    )
