# Python CRUD API - TDD Learning Journey

A comprehensive TDD-driven tutorial for TypeScript/Rust engineers learning Python through building a production-ready REST API.

## 🎯 What You'll Build

A complete CRUD API with:
- **Phase 0**: Calculator API (warm-up)
- **Phase 1**: PostgreSQL infrastructure with Docker
- **Phase 2**: Full User CRUD operations (Create, Read, List, Update, Delete)

**Tech Stack**: FastAPI + SQLAlchemy 2.0 + PostgreSQL + Docker + pytest

## 🚀 Quick Start (3 Commands)

```bash
# 1. Start the database
docker-compose up -d

# 2. Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# 3. Run migrations and start server
alembic upgrade head
python src/main.py
```

## ✅ Prerequisites

- [ ] Python 3.11+ installed (`python --version`)
- [ ] Docker Desktop running
- [ ] PostgreSQL client (optional, for manual queries)
- [ ] TypeScript/JavaScript or Rust experience (assumed)

**Verification Commands:**
```bash
python --version  # Should show 3.11+
docker --version  # Should show 20.10+
pip --version     # Should show 23.0+
```

## 📚 Learning Path

Start here → **[LEARNING_PATH.md](docs/LEARNING_PATH.md)**

This is your step-by-step guide through the entire journey with:
- Clear checkpoints and validation commands
- "You are here" markers
- Troubleshooting help at each stage

## 🧠 Concept Reference

New to Python from TypeScript/Rust? Check **[PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md)** for:
- TypeScript/Rust → Python comparison tables
- Type hints and Pydantic validation
- Async/await patterns
- Common pitfalls and solutions

## 📖 Additional Resources

- **[TYPESCRIPT_TO_PYTHON.md](docs/TYPESCRIPT_TO_PYTHON.md)** - Deep dive concept comparisons
- **[QUICK_START.md](docs/QUICK_START.md)** - Learn by doing (minimal theory)
- **[TDD_GUIDE.md](docs/TDD_GUIDE.md)** - Red-Green-Refactor workflow

## 🎓 Learning Approach

### TDD Red-Green-Refactor Cycle

```
1. 🔴 RED: Run tests → See failures
2. 💡 UNDERSTAND: Read test requirements
3. 🟢 GREEN: Write code to pass tests
4. 🔄 REFACTOR: Clean up and improve
5. ✅ VERIFY: All tests pass → Move forward
```

Every operation follows this cycle. Tests are pre-written to guide your implementation.

## 📁 Project Structure

```
python-api-crud/
├── docs/                    # Learning guides
│   ├── LEARNING_PATH.md    # Start here!
│   ├── PYTHON_CONCEPTS.md  # Quick reference
│   └── ...
├── src/
│   ├── main.py             # Application entry + Phase 0 Calculator
│   ├── config.py           # Configuration
│   ├── models/             # Pydantic + SQLAlchemy models
│   ├── handlers/           # Request handlers
│   └── db/                 # Database utilities
├── tests/
│   ├── conftest.py         # pytest fixtures
│   ├── test_calculator.py  # Phase 0 tests
│   └── test_users.py       # Phase 2 tests
├── migrations/             # Alembic migrations
│   └── versions/
├── docker-compose.yml      # PostgreSQL setup
├── requirements.txt        # Dependencies
├── pyproject.toml         # Project metadata
└── alembic.ini            # Migration config
```

## 🧪 Running Tests

```bash
# Run all tests
pytest

# Run specific phase tests
pytest tests/test_calculator.py  # Phase 0
pytest tests/test_users.py       # Phase 2

# Run with output
pytest -v -s

# Run with coverage
pytest --cov=src --cov-report=html
```

## 🐛 Troubleshooting

### Database connection errors
```bash
# Check if PostgreSQL is running
docker ps

# Reset database
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Python environment issues
```bash
# Recreate virtual environment
deactivate
rm -rf venv
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Port already in use
```bash
# Change port in .env file
PORT=8080  # Try different port
```

## 🎯 Success Checkpoints

### Phase 0: Calculator ✅
```bash
python src/main.py
curl http://localhost:8000/calculate?a=5&b=3&op=add
# Should return: {"result":8.0}
```

### Phase 1: Database ✅
```bash
pytest tests/test_database.py
# All tests pass
```

### Phase 2: CRUD ✅
```bash
# Create user
curl -X POST http://localhost:8000/users \
  -H "Content-Type: application/json" \
  -d '{"name":"Alice","email":"alice@example.com"}'

# Get user
curl http://localhost:8000/users/1
```

### Interactive API Documentation
```bash
# Once server is running:
# Swagger UI:   http://localhost:8000/docs
# ReDoc:        http://localhost:8000/redoc
```

## 📝 Your Learning Journey

Track your progress:

- [ ] Phase 0: Calculator API working
- [ ] Phase 1: Database infrastructure setup
- [ ] Phase 2.1: CREATE user endpoint
- [ ] Phase 2.2: READ user endpoint
- [ ] Phase 2.3: LIST users with pagination
- [ ] Phase 2.4: UPDATE user endpoint
- [ ] Phase 2.5: DELETE user endpoint
- [ ] All tests passing
- [ ] Documentation complete

## 🤝 Learning Tips

1. **Tests guide you** - Read failing tests to understand requirements
2. **Type hints help** - FastAPI + Pydantic provide great IDE support
3. **Iterate quickly** - Red → Green → Refactor
4. **Compare to TypeScript/Rust** - Use the concept guides when confused
5. **Use the docs** - FastAPI auto-generates API documentation at `/docs`

## 🆕 Python Advantages You'll Discover

1. **Pydantic Validation** - Automatic request/response validation
2. **Type Hints** - Optional but powerful type system
3. **FastAPI** - Auto-generated OpenAPI docs and validation
4. **pytest** - Powerful testing with fixtures and parametrization
5. **Rich Ecosystem** - Mature libraries for everything

## 📚 Next Steps

Ready to start? Open **[docs/LEARNING_PATH.md](docs/LEARNING_PATH.md)** and begin your journey!

Have questions? Check **[docs/PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md)** for Python concepts.

Want to dive in immediately? See **[docs/QUICK_START.md](docs/QUICK_START.md)**.

---

**Built with ❤️ for TypeScript/Rust engineers learning Python**
