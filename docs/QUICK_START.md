# ⚡ Quick Start Guide

**Skip the theory. Build the CRUD API in 3 hours.**

This is a hands-on, copy-paste-friendly guide for developers who want to learn Python/FastAPI by building. Perfect for experienced developers coming from TypeScript/JavaScript.

---

## 🎯 What You'll Build

A complete REST API with:
- ✅ FastAPI web framework
- ✅ PostgreSQL database
- ✅ SQLAlchemy async ORM
- ✅ Alembic migrations
- ✅ Full CRUD operations
- ✅ Pydantic validation
- ✅ Pytest tests
- ✅ Type hints throughout

**Time**: ~3 hours
**Prerequisites**: Basic REST API knowledge, PostgreSQL installed

---

## 🚀 Phase 1: Setup (15 minutes)

### Step 1: Create Project Directory

```bash
mkdir python-crud-api && cd python-crud-api
```

### Step 2: Virtual Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate    # Windows
```

### Step 3: Install Dependencies

```bash
# Create requirements.txt
cat > requirements.txt << 'EOF'
fastapi==0.104.1
uvicorn[standard]==0.24.0
sqlalchemy[asyncio]==2.0.23
asyncpg==0.29.0
alembic==1.12.1
pydantic[email]==2.5.0
pydantic-settings==2.1.0
psycopg2-binary==2.9.9
pytest==7.4.3
pytest-asyncio==0.21.1
httpx==0.25.1
EOF

# Install
pip install -r requirements.txt
```

**✅ Checkpoint**: Run `pip list` - you should see all packages installed.

---

## 🗄️ Phase 2: Database (20 minutes)

### Step 1: Start PostgreSQL

```bash
# Using Docker (recommended)
docker run --name postgres-crud \
  -e POSTGRES_USER=pythonuser \
  -e POSTGRES_PASSWORD=pythonpass \
  -e POSTGRES_DB=pythoncrud \
  -p 5432:5432 \
  -d postgres:16
```

Or use existing PostgreSQL and create database:
```bash
psql -U postgres
CREATE DATABASE pythoncrud;
CREATE USER pythonuser WITH PASSWORD 'pythonpass';
GRANT ALL PRIVILEGES ON DATABASE pythoncrud TO pythonuser;
\q
```

### Step 2: Configuration File

```bash
# Create src directory
mkdir -p src

# Create config.py
cat > src/config.py << 'EOF'
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://pythonuser:pythonpass@localhost:5432/pythoncrud"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()
EOF
```

### Step 3: Create .env File

```bash
cat > .env << 'EOF'
DATABASE_URL=postgresql+asyncpg://pythonuser:pythonpass@localhost:5432/pythoncrud
DEBUG=True
EOF
```

**✅ Checkpoint**: `python -c "from src.config import settings; print(settings.DATABASE_URL)"`

---

## 🏗️ Phase 3: Models (30 minutes)

### Step 1: Create User Model

```bash
mkdir -p src/models

cat > src/models/user.py << 'EOF'
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, ConfigDict
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# SQLAlchemy Model (Database)
class User(Base):
    __tablename__ = "users"

    id = Column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

# Pydantic Models (API Schemas)
class UserBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    email: EmailStr

class UserCreate(UserBase):
    pass

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
EOF

# Create __init__.py
touch src/models/__init__.py
```

### Step 2: Database Connection

```bash
mkdir -p src/db

cat > src/db/connection.py << 'EOF'
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config import settings
from models.user import Base

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
EOF

touch src/db/__init__.py
```

**✅ Checkpoint**: `python -c "from src.db.connection import engine; print(engine)"`

---

## 🔄 Phase 4: Migrations (20 minutes)

### Step 1: Initialize Alembic

```bash
alembic init migrations
```

### Step 2: Configure Alembic

Edit `migrations/env.py` - replace the imports and target_metadata sections:

```python
# Add at top (after existing imports)
from logging.config import fileConfig
import sys
from pathlib import Path

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# Add src to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

# Import models
from config import settings
from models.user import Base

# ... keep existing config setup ...

# Replace this line:
target_metadata = None
# With:
target_metadata = Base.metadata

# Add helper function before run_migrations_offline()
def get_url():
    """Convert async URL to sync for Alembic."""
    url = str(settings.DATABASE_URL)
    return url.replace("postgresql+asyncpg://", "postgresql://")

# In run_migrations_offline(), replace:
# url = config.get_main_option("sqlalchemy.url")
# With:
url = get_url()

# In run_migrations_online(), replace the connectable section:
configuration = config.get_section(config.config_ini_section, {})
configuration["sqlalchemy.url"] = get_url()

connectable = engine_from_config(
    configuration,
    prefix="sqlalchemy.",
    poolclass=pool.NullPool,
)
```

### Step 3: Create and Run Migration

```bash
# Create migration
alembic revision --autogenerate -m "create users table"

# Apply migration
alembic upgrade head
```

**✅ Checkpoint**: Connect to database and verify table exists:
```bash
psql postgresql://pythonuser:pythonpass@localhost:5432/pythoncrud -c "\d users"
```

---

## 🎯 Phase 5: CRUD Endpoints (90 minutes)

### Step 1: Create User Handlers

```bash
mkdir -p src/handlers

cat > src/handlers/user_handlers.py << 'EOF'
from uuid import UUID
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.connection import get_db
from models.user import User, UserCreate, UserUpdate, UserResponse

router = APIRouter(prefix="/users", tags=["users"])

# CREATE
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

# READ
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

# LIST
@router.get("", response_model=List[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_db)
) -> List[UserResponse]:
    result = await db.execute(
        select(User).offset(skip).limit(limit)
    )
    users = result.scalars().all()
    return [UserResponse.model_validate(user) for user in users]

# UPDATE
@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: UUID,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
) -> UserResponse:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_data = user_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(user, key, value)

    await db.commit()
    await db.refresh(user)
    return UserResponse.model_validate(user)

# DELETE
@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return None
EOF

touch src/handlers/__init__.py
```

### Step 2: Create Main Application

```bash
cat > src/main.py << 'EOF'
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from handlers.user_handlers import router as user_router

app = FastAPI(
    title="Python CRUD API",
    version="0.1.0",
    description="A simple CRUD API built with FastAPI and PostgreSQL"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(user_router)

@app.get("/")
async def root():
    return {"message": "Python CRUD API is running"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
EOF
```

### Step 3: Run the Server

```bash
cd src
uvicorn main:app --reload --port 8000
```

**✅ Checkpoint**: Visit http://localhost:8000/docs - you should see Swagger UI!

---

## ✅ Phase 6: Test It! (20 minutes)

### Manual Testing with curl

```bash
# 1. CREATE a user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Johnson", "email": "alice@example.com"}'

# Save the returned ID for next steps
USER_ID="<paste-id-here>"

# 2. READ the user
curl http://localhost:8000/users/$USER_ID

# 3. LIST all users
curl "http://localhost:8000/users?skip=0&limit=10"

# 4. UPDATE the user
curl -X PUT http://localhost:8000/users/$USER_ID \
  -H "Content-Type: application/json" \
  -d '{"name": "Alice Smith"}'

# 5. DELETE the user
curl -X DELETE http://localhost:8000/users/$USER_ID
```

### Create Automated Tests

```bash
mkdir -p tests

cat > tests/conftest.py << 'EOF'
import pytest
import asyncio
from typing import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from main import app
from db.connection import get_db
from models.user import Base
from config import settings

# Test database
TEST_DATABASE_URL = settings.DATABASE_URL.replace("pythoncrud", "pythoncrud_test")

engine = create_async_engine(TEST_DATABASE_URL, echo=False)
TestSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session", autouse=True)
async def setup_test_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

@pytest.fixture
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with TestSessionLocal() as session:
        yield session
        await session.rollback()

@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    async def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
    app.dependency_overrides.clear()
EOF

cat > tests/test_users.py << 'EOF'
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_create_user(client: AsyncClient):
    response = await client.post(
        "/users",
        json={"name": "Test User", "email": "test@example.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert "id" in data

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient):
    # Create user first
    create_response = await client.post(
        "/users",
        json={"name": "Alice", "email": "alice@example.com"}
    )
    user_id = create_response.json()["id"]

    # Get user
    response = await client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["name"] == "Alice"

@pytest.mark.asyncio
async def test_list_users(client: AsyncClient):
    # Create users
    await client.post("/users", json={"name": "User 1", "email": "user1@example.com"})
    await client.post("/users", json={"name": "User 2", "email": "user2@example.com"})

    # List users
    response = await client.get("/users?skip=0&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2

@pytest.mark.asyncio
async def test_update_user(client: AsyncClient):
    # Create user
    create_response = await client.post(
        "/users",
        json={"name": "Old Name", "email": "old@example.com"}
    )
    user_id = create_response.json()["id"]

    # Update user
    response = await client.put(
        f"/users/{user_id}",
        json={"name": "New Name"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "New Name"
    assert data["email"] == "old@example.com"  # Unchanged

@pytest.mark.asyncio
async def test_delete_user(client: AsyncClient):
    # Create user
    create_response = await client.post(
        "/users",
        json={"name": "To Delete", "email": "delete@example.com"}
    )
    user_id = create_response.json()["id"]

    # Delete user
    response = await client.delete(f"/users/{user_id}")
    assert response.status_code == 204

    # Verify deleted
    get_response = await client.get(f"/users/{user_id}")
    assert get_response.status_code == 404
EOF
```

### Create Test Database

```bash
psql postgresql://pythonuser:pythonpass@localhost:5432/postgres -c "CREATE DATABASE pythoncrud_test;"

# Run migrations on test DB
DATABASE_URL="postgresql+asyncpg://pythonuser:pythonpass@localhost:5432/pythoncrud_test" \
  alembic upgrade head
```

### Run Tests

```bash
cd ..  # Back to project root
pytest tests/ -v
```

**✅ Checkpoint**: All tests should pass!

---

## 🎉 Success! You've Built a Complete CRUD API

### What You Just Learned

1. ✅ **FastAPI** - Modern Python web framework
2. ✅ **SQLAlchemy** - Async ORM for database operations
3. ✅ **Alembic** - Database migrations
4. ✅ **Pydantic** - Data validation and serialization
5. ✅ **Pytest** - Testing framework with async support
6. ✅ **Type Hints** - Python's type system
7. ✅ **Async/Await** - Asynchronous programming in Python

---

## 🚀 Next Steps

### Immediate Improvements

1. **Add Input Validation**
   ```python
   from pydantic import Field, validator

   class UserCreate(UserBase):
       name: str = Field(..., min_length=1, max_length=255)

       @validator('email')
       def email_must_be_lowercase(cls, v):
           return v.lower()
   ```

2. **Add Error Handling**
   ```python
   from fastapi import Request
   from fastapi.responses import JSONResponse

   @app.exception_handler(Exception)
   async def global_exception_handler(request: Request, exc: Exception):
       return JSONResponse(
           status_code=500,
           content={"detail": str(exc)}
       )
   ```

3. **Add Logging**
   ```python
   import logging

   logging.basicConfig(level=logging.INFO)
   logger = logging.getLogger(__name__)

   @router.post("/users")
   async def create_user(...):
       logger.info(f"Creating user: {user.email}")
       ...
   ```

### Learning Resources

- **Deep Dive**: Read [LEARNING_PATH.md](./LEARNING_PATH.md) for structured 6-week curriculum
- **Python Concepts**: Check [PYTHON_CONCEPTS.md](./PYTHON_CONCEPTS.md) for language features
- **TypeScript Comparison**: See [TYPESCRIPT_TO_PYTHON.md](./TYPESCRIPT_TO_PYTHON.md)
- **Testing Guide**: Explore [TDD_GUIDE.md](./TDD_GUIDE.md) for test-driven development

### Production Features to Add

- [ ] Authentication (JWT)
- [ ] Rate limiting
- [ ] Caching (Redis)
- [ ] Background tasks (Celery)
- [ ] Docker deployment
- [ ] CI/CD pipeline
- [ ] Monitoring and metrics

---

## 📚 Useful Commands Reference

```bash
# Virtual environment
python -m venv venv
source venv/bin/activate
deactivate

# Install packages
pip install <package>
pip install -r requirements.txt
pip freeze > requirements.txt

# Run server
uvicorn main:app --reload --port 8000

# Run tests
pytest
pytest -v
pytest --cov=src tests/
pytest tests/test_users.py::test_create_user

# Alembic migrations
alembic revision --autogenerate -m "description"
alembic upgrade head
alembic downgrade -1
alembic history

# Type checking
mypy src/

# Linting
ruff check src/
ruff format src/

# Database
psql postgresql://user:pass@localhost:5432/db
```

---

**🎊 Congratulations!** You've built a production-ready CRUD API in Python. Now you understand FastAPI, SQLAlchemy, and the Python async ecosystem. Keep coding! 🚀
