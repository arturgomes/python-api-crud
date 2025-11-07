# 🧪 Test-Driven Development Guide

**Master TDD with Python, FastAPI, and Pytest**

This guide teaches test-driven development (TDD) specifically for Python web applications. Perfect for developers transitioning from TypeScript/JavaScript who want to learn testing best practices in Python.

---

## 🎯 What is TDD?

**Test-Driven Development** is a development methodology where you write tests *before* writing the actual code.

### The Red-Green-Refactor Cycle

```
🔴 RED → 💡 THINK → 🟢 GREEN → 🔄 REFACTOR → ✅ VERIFY
```

1. **🔴 Red**: Write a failing test
2. **💡 Think**: Understand what the test requires
3. **🟢 Green**: Write minimal code to make it pass
4. **🔄 Refactor**: Improve code quality without breaking tests
5. **✅ Verify**: Run all tests to ensure nothing broke

---

## 🤔 Why TDD for Learning Python?

### Benefits for Python Learners

1. **Tests as Specifications**: Tests show you exactly what to build
2. **Safe Experimentation**: Try different approaches without fear of breaking things
3. **Instant Validation**: Know immediately when your code works
4. **Learn Pythonic Patterns**: Well-written tests demonstrate idiomatic Python
5. **Build Confidence**: Working tests prove your understanding

### Comparing to TypeScript/Jest

**TypeScript (Jest)**:
```typescript
describe('User API', () => {
  it('should create a user', async () => {
    const response = await request(app)
      .post('/users')
      .send({ name: 'Alice', email: 'alice@example.com' });

    expect(response.status).toBe(201);
    expect(response.body.name).toBe('Alice');
  });
});
```

**Python (Pytest)**:
```python
@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"}
    )

    assert response.status_code == 201
    assert response.json()["name"] == "Alice"
```

**Key Differences**:
- Pytest uses `async def` for async tests
- No `describe` blocks - use file/function organization
- `assert` statements instead of `expect().toBe()`
- Fixtures instead of `beforeEach`/`afterEach`

---

## 📁 Project Structure

### Organizing Tests in Python

```
python-api-crud/
├── src/                    # Application code
│   ├── main.py
│   ├── models/
│   │   └── user.py
│   ├── handlers/
│   │   └── user_handlers.py
│   └── db/
│       └── connection.py
│
├── tests/                  # Test code (separate from src!)
│   ├── conftest.py        # Shared fixtures and configuration
│   ├── test_users.py      # User endpoint tests
│   ├── test_models.py     # Model tests
│   └── common/            # Shared test utilities
│       └── factories.py   # Test data factories
│
├── pytest.ini             # Pytest configuration
└── requirements.txt
```

**Why separate tests/?**
- Clear separation of concerns
- Easy to exclude from production builds
- Follows Python community standards

---

## 🏗️ Test Structure: Arrange-Act-Assert

Every test follows the **AAA pattern**:

```python
async def test_create_user(client: AsyncClient):
    # ARRANGE: Set up test data
    user_data = {
        "name": "Alice Johnson",
        "email": "alice@example.com"
    }

    # ACT: Perform the action
    response = await client.post("/users", json=user_data)

    # ASSERT: Verify expectations
    assert response.status_code == 201
    assert response.json()["name"] == "Alice Johnson"
    assert response.json()["email"] == "alice@example.com"
    assert "id" in response.json()
```

---

## 🚀 TDD in Practice: Building User CRUD

Let's walk through building a CRUD API using TDD.

### Step 1: Write the First Test (🔴 RED)

**File**: `tests/test_users.py`

```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    """Test creating a new user."""
    response = await client.post(
        "/users",
        json={
            "name": "Alice Johnson",
            "email": "alice@example.com"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Alice Johnson"
    assert data["email"] == "alice@example.com"
    assert "id" in data
    assert "created_at" in data
```

**Run it**: `pytest tests/test_users.py -v`

**Expected**: ❌ Test fails - endpoint doesn't exist yet!

### Step 2: Think About What's Needed (💡 THINK)

What do we need to make this pass?
1. User model (SQLAlchemy + Pydantic)
2. POST /users endpoint
3. Database session
4. User creation logic

### Step 3: Write Minimal Code (🟢 GREEN)

**Create the model** (`src/models/user.py`):

```python
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UserCreate(BaseModel):
    name: str
    email: EmailStr

class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
```

**Create the endpoint** (`src/handlers/user_handlers.py`):

```python
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from models.user import User, UserCreate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    db_user = User(**user.model_dump())
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return UserResponse.model_validate(db_user)
```

**Run test again**: `pytest tests/test_users.py -v`

**Expected**: ✅ Test passes!

### Step 4: Refactor (🔄 REFACTOR)

Now improve the code without changing behavior:

```python
# Add validation to UserCreate
from pydantic import Field

class UserCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr

    @validator('email')
    def email_must_be_lowercase(cls, v):
        return v.lower()
```

### Step 5: Verify (✅ VERIFY)

```bash
pytest tests/test_users.py -v
```

All tests still pass! ✅

---

## 🔁 Continuing the Cycle: READ Operation

### Test First (🔴 RED)

```python
@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, db_session: AsyncSession):
    """Test retrieving a user by ID."""
    # Arrange: Create a user first
    from models.user import User
    user = User(name="Alice", email="alice@example.com")
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    # Act: Get the user
    response = await client.get(f"/users/{user.id}")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == str(user.id)
    assert data["name"] == "Alice"
    assert data["email"] == "alice@example.com"
```

**Run**: ❌ Fails - endpoint doesn't exist

### Implementation (🟢 GREEN)

```python
from fastapi import HTTPException
from sqlalchemy import select
from uuid import UUID

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return UserResponse.model_validate(user)
```

**Run**: ✅ Passes!

### Add Edge Case Test

```python
@pytest.mark.asyncio
async def test_get_nonexistent_user(client: AsyncClient):
    """Test getting a user that doesn't exist."""
    from uuid import uuid4

    fake_id = uuid4()
    response = await client.get(f"/users/{fake_id}")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
```

---

## 🎨 Pytest Patterns for FastAPI

### Fixtures: Reusable Test Components

**conftest.py** - Shared fixtures for all tests:

```python
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from main import app
from db.connection import get_db
from models.user import Base
from config import settings

# Test database URL
TEST_DATABASE_URL = settings.DATABASE_URL.replace("pythoncrud", "pythoncrud_test")

# Test engine
engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    """Create test database tables."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Provide database session for tests."""
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Cleanup after test

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Provide HTTP client for API tests."""
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
```

**Fixture Scopes**:
- `function` (default): Run for each test
- `class`: Run once per test class
- `module`: Run once per file
- `session`: Run once for entire test session

### Parametrized Tests

Test multiple scenarios with one test function:

```python
@pytest.mark.parametrize("name,email,expected_status", [
    ("Alice", "alice@example.com", 201),
    ("Bob", "bob@example.com", 201),
    ("", "invalid@example.com", 422),  # Empty name
    ("Charlie", "not-an-email", 422),  # Invalid email
])
@pytest.mark.asyncio
async def test_create_user_validation(
    client: AsyncClient,
    name: str,
    email: str,
    expected_status: int
):
    response = await client.post(
        "/users",
        json={"name": name, "email": email}
    )
    assert response.status_code == expected_status
```

### Markers

Organize and filter tests:

```python
import pytest

@pytest.mark.slow
@pytest.mark.asyncio
async def test_complex_operation(client: AsyncClient):
    # This test takes a long time
    pass

@pytest.mark.smoke
@pytest.mark.asyncio
async def test_health_check(client: AsyncClient):
    # Critical test that should always run
    response = await client.get("/health")
    assert response.status_code == 200
```

Run specific markers:
```bash
pytest -m "smoke"           # Only smoke tests
pytest -m "not slow"        # Skip slow tests
pytest -m "smoke or critical"  # Either marker
```

---

## 🗄️ Database Testing Strategies

### Strategy 1: Transaction Rollback (Recommended)

**Best for**: Most tests - fast and isolated

```python
@pytest.fixture
async def db_session():
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()  # Undo all changes
```

**Pros**: Fast, automatic cleanup
**Cons**: Doesn't test transaction behavior

### Strategy 2: Truncate Tables

**Best for**: Integration tests

```python
@pytest.fixture
async def db_session():
    session = TestSessionLocal()
    yield session

    # Cleanup
    for table in reversed(Base.metadata.sorted_tables):
        await session.execute(table.delete())
    await session.commit()
    await session.close()
```

**Pros**: Tests real transactions
**Cons**: Slower, must handle order (foreign keys)

### Strategy 3: Separate Test Database

**Best for**: Full isolation

```python
# Use different database for tests
TEST_DATABASE_URL = "postgresql+asyncpg://...pythoncrud_test"
```

**Pros**: Complete isolation from dev data
**Cons**: Requires separate database setup

---

## 🏭 Test Data Factories

Create test data easily with factories:

```python
# tests/common/factories.py
from uuid import uuid4
from models.user import User

class UserFactory:
    @staticmethod
    def create(**kwargs):
        defaults = {
            "id": uuid4(),
            "name": "Test User",
            "email": f"test{uuid4().hex[:8]}@example.com"
        }
        defaults.update(kwargs)
        return User(**defaults)

# Usage in tests
@pytest.mark.asyncio
async def test_with_factory(db_session: AsyncSession):
    user = UserFactory.create(name="Alice")
    db_session.add(user)
    await db_session.commit()

    # ... test code
```

Or use **factory_boy** library:

```python
import factory
from factory.fuzzy import FuzzyText

class UserFactory(factory.Factory):
    class Meta:
        model = User

    name = factory.Faker('name')
    email = factory.Faker('email')

# Usage
user = UserFactory.create()
users = UserFactory.create_batch(10)
```

---

## 📊 Code Coverage

### Measuring Coverage

```bash
# Install coverage tool
pip install pytest-cov

# Run tests with coverage
pytest --cov=src tests/

# Generate HTML report
pytest --cov=src --cov-report=html tests/
open htmlcov/index.html
```

### Coverage Goals

- **✅ 80%+**: Good coverage for most projects
- **🎯 90%+**: Excellent coverage
- **⚠️ 100%**: Not always necessary - focus on critical paths

**What to prioritize**:
1. Business logic
2. Data validation
3. Error handling
4. API endpoints

**What to skip**:
- Configuration files
- Simple getters/setters
- Third-party code

---

## 🎯 Best Practices

### 1. One Thing Per Test

**❌ Bad**:
```python
async def test_user_crud(client: AsyncClient):
    # Create
    response = await client.post("/users", json={...})
    assert response.status_code == 201

    # Read
    user_id = response.json()["id"]
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200

    # Update
    response = await client.put(f"/users/{user_id}", json={...})
    assert response.status_code == 200

    # Delete
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204
```

**✅ Good**:
```python
async def test_create_user(client: AsyncClient):
    response = await client.post("/users", json={...})
    assert response.status_code == 201

async def test_read_user(client: AsyncClient):
    # Setup: create user first
    # Test: read user
    pass

# Separate test for each operation
```

### 2. Descriptive Test Names

**❌ Bad**:
```python
def test_user():
def test_1():
def test_endpoint():
```

**✅ Good**:
```python
def test_create_user_with_valid_email():
def test_get_user_returns_404_when_not_found():
def test_update_user_email_must_be_unique():
```

### 3. Test Independence

**❌ Bad**:
```python
# test_users.py
USER_ID = None  # Global state!

async def test_create():
    global USER_ID
    response = await client.post(...)
    USER_ID = response.json()["id"]

async def test_get():
    global USER_ID
    response = await client.get(f"/users/{USER_ID}")  # Depends on test_create!
```

**✅ Good**:
```python
async def test_create(client: AsyncClient):
    response = await client.post(...)
    # Test is complete and independent

async def test_get(client: AsyncClient, db_session: AsyncSession):
    # Create test data within this test
    user = UserFactory.create()
    db_session.add(user)
    await db_session.commit()

    response = await client.get(f"/users/{user.id}")
```

### 4. Consistent Cleanup

**Use fixtures for setup/teardown**:

```python
@pytest.fixture
async def created_user(db_session: AsyncSession):
    """Fixture that provides a user and cleans up after."""
    user = UserFactory.create()
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    yield user

    # Cleanup (if not using transaction rollback)
    await db_session.delete(user)
    await db_session.commit()
```

---

## 🚀 Running Tests

### Common Commands

```bash
# Run all tests
pytest

# Verbose output
pytest -v

# Run specific file
pytest tests/test_users.py

# Run specific test
pytest tests/test_users.py::test_create_user

# Run with coverage
pytest --cov=src tests/

# Stop on first failure
pytest -x

# Run last failed tests
pytest --lf

# Show print statements
pytest -s

# Run in parallel (install pytest-xdist)
pytest -n 4
```

### pytest.ini Configuration

```ini
[pytest]
# Minimum version
minversion = 7.0

# Test discovery patterns
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Async support
asyncio_mode = auto

# Output
addopts =
    -v
    --strict-markers
    --tb=short
    --cov=src
    --cov-report=term-missing

# Markers
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    smoke: critical tests that should always pass
    integration: tests that require external services
```

---

## 💡 TDD Tips for Python Learners

### Start Small

Don't try to test everything at once:
1. Start with happy path tests
2. Add edge cases
3. Add error cases
4. Add integration tests

### Use Tests to Learn

Write tests to understand how libraries work:

```python
def test_sqlalchemy_relationship():
    """Learning how SQLAlchemy relationships work."""
    user = User(name="Alice")
    post = Post(title="Test", author=user)

    assert post.author == user
    assert user.posts == [post]
```

### Let Tests Guide Design

If a test is hard to write, your code might be too complex:

**❌ Hard to test**:
```python
async def create_user(data):
    # Does too much - DB, validation, email sending
    user = User(**data)
    db.add(user)
    await db.commit()
    await send_welcome_email(user.email)
    await log_user_creation(user.id)
    return user
```

**✅ Easy to test**:
```python
async def create_user(data, db: AsyncSession):
    # Just creates user
    user = User(**data)
    db.add(user)
    await db.commit()
    return user

# Separate functions for other concerns
async def send_welcome_email(email: str): ...
async def log_user_creation(user_id: UUID): ...
```

---

## 📚 Next Steps

### Learning Path
1. **Basic Tests**: Start with simple endpoint tests
2. **Fixtures**: Learn to reuse test setup
3. **Parametrization**: Test multiple scenarios
4. **Mocking**: Learn to mock external dependencies
5. **Integration Tests**: Test full workflows

### Resources
- **Pytest Docs**: https://docs.pytest.org
- **FastAPI Testing**: https://fastapi.tiangolo.com/tutorial/testing/
- **Python Testing with pytest (Book)**: By Brian Okken

### Practice
- Write tests for all CRUD operations
- Test error cases (404, 400, 500)
- Test validation edge cases
- Write integration tests for full workflows

---

**🎊 Congratulations!** You now understand TDD in Python. Remember: **Write the test first, make it pass, then refactor.** 🚀
