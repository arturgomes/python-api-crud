# Python CRUD API - Implementation Task

<task>
You are an expert Python educator helping TypeScript/Rust engineers learn Python through Test-Driven Development (TDD). The developer is experienced with design patterns, DRY principles, and clean code.

<objective>
Create a comprehensive TDD-based learning tutorial for building a User CRUD API in Python with FastAPI. The tutorial should:
- Start with pre-written failing tests that drive development
- Include a simple Calculator API example first (Phase 0) to demonstrate patterns
- Progress incrementally from simple to complex
- Result in a fully working, containerized application
- Teach Python concepts through the red-green-refactor cycle
</objective>

<tutorial_structure>
PHASE 0: Simple Working Example (Calculator API)
- Create a minimal "Calculator API" with endpoints as a warm-up:
  * GET /calculate (calculator with query parameters)
  * GET / (health check / welcome)
- Pre-written tests for these endpoints
- Demonstrates: FastAPI setup, routing, validation with Pydantic, testing with pytest
- Goal: Get something working quickly to understand the workflow

PHASE 1: Project Setup & Infrastructure
- Docker Compose setup (PostgreSQL)
- Database connection with SQLAlchemy 2.0 async
- Alembic for migrations
- Test database setup with pytest fixtures
- Pre-written infrastructure tests (DB connectivity, migrations)

PHASE 2: TDD User CRUD (one operation at a time)
Each operation follows: Test → Implement → Pass → Refactor

2.1: CREATE User
- Pre-written integration tests for POST /users
- Pre-written validation tests
- Implement to pass tests

2.2: READ User by ID
- Pre-written tests for GET /users/{id}
- Handle 404 cases
- Implement to pass tests

2.3: LIST Users (with pagination)
- Pre-written tests for GET /users
- Test pagination edge cases
- Implement to pass tests

2.4: UPDATE User
- Pre-written tests for PUT /users/{id}
- Test partial updates
- Implement to pass tests

2.5: DELETE User
- Pre-written tests for DELETE /users/{id}
- Test idempotency
- Implement to pass tests
</tutorial_structure>

<requirements>
TECHNICAL STACK:
- FastAPI web framework
- SQLAlchemy 2.0 with async support
- PostgreSQL (via asyncpg driver)
- Docker & Docker Compose
- pytest with pytest-asyncio
- Pydantic 2.0 for validation
- Alembic for migrations

PROJECT STRUCTURE:
```
python-api-crud/
├── docker-compose.yml
├── requirements.txt
├── pyproject.toml
├── .env.example
├── alembic.ini
├── README.md
├── START_HERE.md
├── SETUP_CHECKLIST.md
├── LEARNING_PATH.md
├── task.md (this file)
├── migrations/
│   └── versions/
│       └── 001_create_users.py
├── src/
│   ├── main.py              # Application entry + Phase 0 Calculator
│   ├── config.py            # Configuration with pydantic-settings
│   ├── models/
│   │   ├── __init__.py
│   │   └── user.py          # SQLAlchemy + Pydantic models
│   ├── handlers/
│   │   ├── __init__.py
│   │   └── user_handlers.py # TODO: Implement handlers
│   └── db/
│       ├── __init__.py
│       └── connection.py     # Database session management
├── tests/
│   ├── conftest.py          # pytest fixtures
│   ├── test_calculator.py   # Phase 0 tests (passing)
│   └── test_users.py        # Phase 2 tests (failing initially)
└── docs/
    ├── LEARNING_PATH.md
    ├── PYTHON_CONCEPTS.md
    ├── TYPESCRIPT_TO_PYTHON.md
    ├── QUICK_START.md
    ├── TDD_GUIDE.md
    └── PROJECT_SUMMARY.md
```

DOCKER SETUP:
- PostgreSQL 16 container
- Uses port 5433 (to avoid conflict with Rust project on 5432)
- Volume persistence
- Health checks

ALL TESTS PRE-WRITTEN:
- Unit tests for validation
- Integration tests for each endpoint
- Edge cases and error scenarios
- Database transaction tests
- All tests should FAIL initially (except calculator)
- Success = all tests passing (green)
</requirements>

<user_model>
User {
  id: UUID (auto-generated)
  email: str (unique, validated with EmailStr)
  name: str
  created_at: datetime (auto-generated)
  updated_at: datetime (auto-updated)
}

Two model types:
1. SQLAlchemy User (database table)
2. Pydantic models (UserCreate, UserUpdate, UserResponse)
</user_model>

<teaching_approach>
FOR EACH PHASE:
1. Explain what we're building and why
2. Show the failing tests first
3. Explain Python concepts needed to make tests pass
4. Compare to TypeScript/Rust equivalents
5. Implement minimal code to pass tests
6. Refactor and explain improvements
7. Verify all tests pass

KEY PYTHON CONCEPTS TO HIGHLIGHT:
- Type hints (vs TypeScript types, Rust's strict typing)
- Pydantic validation (runtime validation)
- Async/await with asyncio (vs Tokio, Node.js)
- FastAPI dependency injection (vs Axum's extractors)
- SQLAlchemy 2.0 ORM (vs SQLx in Rust)
- pytest fixtures (vs Rust test setup)
- Context managers (async with)
- Decorators (@app.get, @pytest.mark.asyncio)
</teaching_approach>

<deliverables>
1. LEARNING_PATH.md - Step-by-step guide with checkpoints:
   - "Start here: Run Phase 0 Calculator example"
   - "Checkpoint 1: All infrastructure tests pass"
   - "Checkpoint 2: CREATE tests pass"
   - etc.

2. README.md with:
   - Prerequisites (Python 3.11+, Docker)
   - Quick start commands
   - How to run tests: `pytest`
   - How to run app: `docker-compose up && python src/main.py`
   - How to verify: example curl commands
   - Link to auto-generated API docs at /docs

3. Complete working application:
   - docker-compose.yml (ready to run)
   - Alembic migrations
   - Pre-written comprehensive tests
   - Implementation code with educational comments
   - .env.example with all config

4. PYTHON_CONCEPTS.md:
   - Glossary of Python terms
   - TypeScript/Rust → Python comparison table
   - Common pitfalls and solutions
   - Resource links

5. Example requests file (requests.http or curl scripts)
</deliverables>

<verification_criteria>
WORKING MEANS:
✅ `docker-compose up` starts PostgreSQL
✅ `python -m venv venv && source venv/bin/activate` creates environment
✅ `pip install -r requirements.txt` installs dependencies
✅ `alembic upgrade head` runs migrations
✅ `python src/main.py` starts API server
✅ API responds to requests
✅ `pytest` shows calculator tests passing
✅ Calculator example works (Phase 0)
✅ User tests fail initially (Phase 2 - to be implemented)
✅ Auto-generated API docs at http://localhost:8000/docs
✅ Database persists data correctly
✅ Error handling returns proper status codes
✅ Validation works (invalid email fails, etc.)
</verification_criteria>

<style>
- Write idiomatic, clean Python code
- Follow PEP 8 style guide
- Use type hints everywhere (like TypeScript)
- Comprehensive docstrings explaining "why" not just "what"
- Tests should be self-documenting
- Use proper error handling (no bare except:)
- Follow Python naming conventions (snake_case)
- Make it feel like a real production codebase
- Progressive complexity: simple → advanced
</style>

<success_definition>
The tutorial is successful when:
- A TypeScript/Rust developer can clone, run `docker-compose up`, create venv, and see working API
- They can run `pytest` and see tests fail (except calculator)
- They can follow LEARNING_PATH.md to implement features
- Each implementation makes specific tests pass
- At the end, all tests are green and the API is production-ready
- They understand core Python concepts through practical application
- They can view auto-generated API docs at /docs
</success_definition>
</task>
