# 🗺️ Python CRUD API Learning Path

**A structured journey from TypeScript/JavaScript to Python web development**

This guide provides a **6-week progressive curriculum** for building a production-ready CRUD API with Python, FastAPI, and PostgreSQL. Perfect for developers transitioning from TypeScript/JavaScript who want to learn Python through hands-on experience.

---

## 🎯 Learning Philosophy

- **Learn by Doing**: Code first, theory later
- **Comparative Learning**: Leverage your TypeScript/JavaScript knowledge
- **Test-Driven Development**: Red-Green-Refactor cycle throughout
- **Incremental Progress**: Small, verified steps prevent overwhelm
- **Break Things**: The Python interpreter and type checker will teach you

---

## 📊 Prerequisites

- [x] Basic TypeScript/JavaScript knowledge
- [x] Understanding of REST APIs
- [x] Familiarity with async/await patterns
- [x] Basic SQL knowledge (helpful but not required)

**Time Commitment**: ~30-40 hours over 6 weeks (5-7 hours/week)

---

## 🚀 Phase 0: Python Fundamentals (Week 1)

**Goal**: Learn Python syntax through a simple calculator API
**Time**: 4-6 hours
**Approach**: Hands-on experimentation

### Step 1: Environment Setup (30 minutes)
- [ ] Install Python 3.11+
- [ ] Set up virtual environment
- [ ] Install FastAPI and dependencies
- [ ] Run your first FastAPI app

```bash
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows
pip install fastapi uvicorn
```

### Step 2: Calculator API (2-3 hours)
Build a simple calculator to learn Python basics:

**Features to implement**:
- [ ] Addition endpoint: `POST /calculate/add`
- [ ] Subtraction endpoint: `POST /calculate/subtract`
- [ ] Multiplication endpoint: `POST /calculate/multiply`
- [ ] Division endpoint: `POST /calculate/divide`

**Key Python concepts to learn**:
- Type hints: `def add(a: int, b: int) -> int:`
- Pydantic models for request/response validation
- FastAPI route decorators: `@app.post("/calculate/add")`
- Async/await (optional at this stage)

**Comparison to TypeScript**:
```typescript
// TypeScript
function add(a: number, b: number): number {
  return a + b;
}
```

```python
# Python
def add(a: int, b: int) -> int:
    return a + b
```

### Step 3: Add Error Handling (1 hour)
- [ ] Handle division by zero
- [ ] Validate input types
- [ ] Return proper HTTP status codes

**Learn**: Exception handling with `try/except` vs TypeScript's `try/catch`

### Step 4: Write Tests (1-2 hours)
- [ ] Install pytest
- [ ] Write test for each calculator operation
- [ ] Run tests: `pytest`

**🚨 Stuck?** See [TDD_GUIDE.md](./TDD_GUIDE.md) for testing patterns.

---

## 🗄️ Phase 1: Database Infrastructure (Week 2)

**Goal**: Set up PostgreSQL and learn SQLAlchemy ORM
**Time**: 6-8 hours
**Approach**: Database-first development

### Step 1: Database Setup (1 hour)
- [ ] Install PostgreSQL (or use Docker)
- [ ] Create database: `pythoncrud`
- [ ] Test connection with `psql`

```bash
docker-compose up -d  # If using Docker
psql postgresql://postgres:postgres@localhost:5432/pythoncrud
```

### Step 2: SQLAlchemy Models (2 hours)
**Learn**: ORM concepts similar to TypeORM/Prisma

- [ ] Create `User` model with SQLAlchemy
- [ ] Define table columns and types
- [ ] Add timestamps: `created_at`, `updated_at`

**Key concepts**:
- Declarative base: `Base = declarative_base()`
- Column definitions: `Column(String(255), nullable=False)`
- Relationships and foreign keys (for later)

**TypeScript comparison**:
```typescript
// TypeORM (TypeScript)
@Entity()
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;
}
```

```python
# SQLAlchemy (Python)
class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True)
    name = Column(String(255), nullable=False)
```

### Step 3: Alembic Migrations (2-3 hours)
**Learn**: Database migrations like TypeORM migrations or Prisma migrate

- [ ] Initialize Alembic: `alembic init migrations`
- [ ] Configure `env.py` with your database URL
- [ ] Create first migration: `alembic revision --autogenerate -m "create users"`
- [ ] Apply migration: `alembic upgrade head`

**🚨 Stuck?** Check `SETUP_CHECKLIST.md` Phase 1 for detailed Alembic configuration.

### Step 4: Database Connection (1 hour)
- [ ] Create async database engine
- [ ] Set up session factory
- [ ] Implement dependency injection for FastAPI

**Learn**: AsyncIO and async context managers

### Step 5: Manual Testing (1 hour)
- [ ] Connect to database
- [ ] Create a test user manually
- [ ] Query the user back
- [ ] Verify timestamps work

---

## 👤 Phase 2: CRUD Operations (Weeks 3-4)

**Goal**: Implement all 5 CRUD endpoints with TDD
**Time**: 12-15 hours
**Approach**: Test-first, one endpoint at a time

Each operation follows the **Red-Green-Refactor** cycle:
1. 🔴 Read failing test
2. 💡 Understand what's needed
3. 🟢 Write minimal code to pass
4. 🔄 Refactor and improve
5. ✅ Verify all tests pass

### Operation 1: CREATE User (3 hours)

**Test-first approach**:
- [ ] Read `tests/test_users.py::test_create_user`
- [ ] Understand the expected behavior
- [ ] Implement `POST /users` endpoint
- [ ] Make test pass
- [ ] Refactor if needed

**What you'll learn**:
- Pydantic schemas for request validation
- SQLAlchemy async sessions
- Inserting data with ORM
- Returning created resource with 201 status

**Checkpoint**: ✅ Can create users via API

### Operation 2: READ User by ID (2 hours)

- [ ] Read `tests/test_users.py::test_get_user`
- [ ] Implement `GET /users/{id}` endpoint
- [ ] Handle user not found (404)
- [ ] Return user data

**What you'll learn**:
- Path parameters in FastAPI
- UUID handling
- Error responses with HTTPException
- Pydantic response models

**Checkpoint**: ✅ Can retrieve users by ID

### Operation 3: LIST Users (3 hours)

- [ ] Read `tests/test_users.py::test_list_users`
- [ ] Implement `GET /users` endpoint
- [ ] Add pagination (offset/limit)
- [ ] Return list of users

**What you'll learn**:
- Query parameters
- SQLAlchemy queries with filters
- List responses
- Pagination patterns

**Checkpoint**: ✅ Can list users with pagination

### Operation 4: UPDATE User (2 hours)

- [ ] Read `tests/test_users.py::test_update_user`
- [ ] Implement `PUT /users/{id}` endpoint
- [ ] Handle partial updates
- [ ] Return updated user

**What you'll learn**:
- Partial model updates
- Pydantic `Optional` fields
- Updating with SQLAlchemy
- Timestamp auto-updates

**Checkpoint**: ✅ Can update user data

### Operation 5: DELETE User (2 hours)

- [ ] Read `tests/test_users.py::test_delete_user`
- [ ] Implement `DELETE /users/{id}` endpoint
- [ ] Return 204 No Content
- [ ] Handle deletion of non-existent user

**What you'll learn**:
- DELETE operations with ORM
- Proper status codes for deletion
- Idempotent deletes

**Checkpoint**: ✅ Can delete users

---

## 🧪 Phase 3: Testing & Quality (Week 5)

**Goal**: Master testing patterns and code quality
**Time**: 5-7 hours
**Approach**: Test coverage and refactoring

### Step 1: Test Coverage (2 hours)
- [ ] Run coverage report: `pytest --cov=src tests/`
- [ ] Achieve >80% coverage
- [ ] Add missing test cases

### Step 2: Edge Cases (2 hours)
- [ ] Test invalid email formats
- [ ] Test duplicate email creation
- [ ] Test concurrent updates
- [ ] Test database connection failures

### Step 3: Integration Tests (2 hours)
- [ ] Write full workflow test (create → read → update → delete)
- [ ] Test pagination edge cases
- [ ] Test error scenarios

### Step 4: Code Quality (1 hour)
- [ ] Run linter: `ruff check src/`
- [ ] Run type checker: `mypy src/`
- [ ] Fix all warnings
- [ ] Add docstrings to public functions

**Tools to explore**:
- `pytest` - Testing framework
- `pytest-asyncio` - Async test support
- `pytest-cov` - Coverage reporting
- `ruff` - Fast Python linter
- `mypy` - Static type checker

---

## 🚀 Phase 4: Production Ready (Week 6)

**Goal**: Prepare for deployment
**Time**: 4-6 hours
**Approach**: Production best practices

### Step 1: Configuration (1 hour)
- [ ] Environment-based config with Pydantic Settings
- [ ] `.env` file for local development
- [ ] Separate test/prod configurations

### Step 2: Error Handling (1 hour)
- [ ] Global exception handler
- [ ] Structured error responses
- [ ] Logging setup

### Step 3: API Documentation (1 hour)
- [ ] Customize OpenAPI docs
- [ ] Add endpoint descriptions
- [ ] Add request/response examples
- [ ] Test at `http://localhost:8000/docs`

### Step 4: Docker (1-2 hours)
- [ ] Create `Dockerfile`
- [ ] Create `docker-compose.yml`
- [ ] Test containerized app
- [ ] Document deployment steps

### Step 5: Optional Enhancements
- [ ] Add authentication (JWT)
- [ ] Add rate limiting
- [ ] Add CORS middleware
- [ ] Add health check endpoint
- [ ] Add metrics/monitoring

---

## 🎓 Learning Resources

### Python Concepts
See [PYTHON_CONCEPTS.md](./PYTHON_CONCEPTS.md) for deep dives into:
- Type hints and Pydantic
- Async/await and AsyncIO
- Context managers
- Decorators
- List comprehensions

### Language Comparison
See [TYPESCRIPT_TO_PYTHON.md](./TYPESCRIPT_TO_PYTHON.md) for:
- Syntax differences
- Type system comparison
- Async patterns
- Error handling
- Package management

### Testing Guide
See [TDD_GUIDE.md](./TDD_GUIDE.md) for:
- Red-Green-Refactor workflow
- Test structure patterns
- Database test strategies
- Pytest best practices

### Quick Reference
See [QUICK_START.md](./QUICK_START.md) for:
- Copy-paste code snippets
- Fast implementation guide
- Common commands

---

## 📈 Progress Tracking

### Week 1: Foundations
- [ ] Calculator API working
- [ ] Tests passing
- [ ] Python syntax comfortable

### Week 2: Database
- [ ] PostgreSQL running
- [ ] Alembic configured
- [ ] User model created

### Week 3-4: CRUD
- [ ] All 5 operations implemented
- [ ] All tests passing
- [ ] API documentation complete

### Week 5: Quality
- [ ] >80% test coverage
- [ ] No linter errors
- [ ] Type checking passes

### Week 6: Production
- [ ] Docker setup complete
- [ ] Environment config working
- [ ] Ready for deployment

---

## 🚨 Common Pitfalls

### "Import Error: No module named..."
- Ensure virtual environment is activated
- Run `pip install -r requirements.txt`

### "Database connection refused"
- Check PostgreSQL is running: `docker-compose ps`
- Verify connection string in `.env`

### "Tests failing after database changes"
- Run migrations: `alembic upgrade head`
- Check test database is clean

### "Type errors with mypy"
- Add type hints gradually
- Use `# type: ignore` for third-party libraries
- Start with `--ignore-missing-imports`

---

## 🎯 What's Next?

After completing this path, you'll be ready for:

1. **Advanced Python Patterns**
   - Dependency injection
   - Design patterns
   - Performance optimization

2. **Production Deployment**
   - AWS/GCP/Azure deployment
   - CI/CD pipelines
   - Monitoring and logging

3. **Advanced Features**
   - WebSocket support
   - Background tasks with Celery
   - Caching with Redis
   - Full-text search

4. **Ecosystem Exploration**
   - GraphQL with Strawberry
   - Django vs FastAPI
   - Alternative ORMs (Tortoise, Peewee)

---

## 💬 Getting Help

**Stuck on something?**
1. Read the error message carefully (Python errors are very descriptive!)
2. Check relevant doc file (PYTHON_CONCEPTS, TDD_GUIDE, etc.)
3. Run tests to see what's failing: `pytest -v`
4. Use the debugger: `import pdb; pdb.set_trace()`
5. Search Python docs: https://docs.python.org/3/

**Remember**: The best way to learn is by breaking things and fixing them! 🚀
