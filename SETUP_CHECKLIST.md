# ✅ Setup Checklist - Verify Your Python Learning Environment

Use this checklist to ensure everything is properly set up before starting.

---

## 📋 Prerequisites Check

### 1. Install Python 3.11+
```bash
# Check Python version
python --version  # or python3 --version

# If needed, install Python 3.11+
# macOS (using Homebrew):
brew install python@3.11

# Linux (Ubuntu/Debian):
sudo apt update
sudo apt install python3.11 python3.11-venv python3-pip

# Windows: Download from python.org
```

**Expected Output**:
```
Python 3.11.0 (or higher)
```

- [x] Python 3.11+ installed
- [x] pip installed

---

### 2. Install Docker Desktop
Download from: https://www.docker.com/products/docker-desktop

```bash
# Verify installation
docker --version
docker-compose --version
```

**Expected Output**:
```
Docker version 20.10.x or higher
Docker Compose version 2.x.x or higher
```

- [x] Docker installed
- [x] Docker Desktop running

---

## 🚀 Project Setup

### 1. Navigate to Project
```bash
cd python-api-crud
```

- [x] In project directory

### 2. Create Virtual Environment
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
# On Linux/macOS:
source venv/bin/activate

# On Windows:
venv\Scripts\activate

# You should see (venv) in your terminal prompt
```

- [x] Virtual environment created
- [x] Virtual environment activated

### 3. Install Dependencies
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

**Expected**: Installs FastAPI, SQLAlchemy, pytest, and other dependencies

- [x] Dependencies installed successfully

### 4. Copy Environment File
```bash
cp .env.example .env
```

**Verify**:
```bash
cat .env
```

Should see DATABASE_URL, PORT, etc.

- [x] .env file exists with correct values

### 5. Start Database
```bash
docker-compose up -d
```

**Expected**:
```
Creating python_crud_db ... done
```

**Verify it's running**:
```bash
docker ps
```

Should see a container named `python_crud_db` running

- [x] PostgreSQL container running

---

## 🧪 Phase 0: Calculator Verification

### 1. Run the Calculator
```bash
# Make sure virtual environment is activated
python src/main.py
```

**Expected Output**:
```
🚀 Python CRUD API v0.1.0
📍 Starting server on http://0.0.0.0:8000
📖 API docs available at http://localhost:8000/docs
🧪 Try: http://localhost:8000/calculate?a=5&b=3&op=add
```

- [x] Server starts without errors

### 2. Test Calculator (in new terminal)
```bash
# Test addition
curl "http://localhost:8000/calculate?a=10&b=5&op=add"
```

**Expected**: `{"result":15.0}`

```bash
# Test division
curl "http://localhost:8000/calculate?a=10&b=2&op=divide"
```

**Expected**: `{"result":5.0}`

```bash
# Test error case
curl "http://localhost:8000/calculate?a=10&b=0&op=divide"
```

**Expected**: `{"detail":"Division by zero"}`

- [x] Addition works
- [x] Division works
- [x] Error handling works

### 3. Check API Documentation
Open browser: http://localhost:8000/docs

**Expected**: Interactive Swagger UI with API documentation

- [x] Swagger UI loads
- [x] Calculator endpoint visible

### 4. Stop Server
Press `Ctrl+C` in the terminal running the server

- [x] Server stops cleanly

---

## 🧪 Test Infrastructure Check

### 1. Run Tests
```bash
# Make sure virtual environment is activated
pytest tests/test_calculator.py -v
```

**Expected**: All calculator tests pass ✅

```bash
# Run all tests (user tests will fail - that's expected!)
pytest -v
```

- [x] Calculator tests pass
- [x] User tests fail (expected - you'll implement them!)

---

## 🗄️ Phase 1: Database Verification

### 1. Initialize Alembic and Configure

First, initialize Alembic (creates configuration files):

```bash
# Initialize Alembic (if not already done)
alembic init migrations

# This creates:
# - alembic.ini (configuration file)
# - migrations/ (migration directory with env.py)
```

**Important**: Don't edit `alembic.ini`! Your database URL comes from `.env` via `config.py`.

### 2. Configure migrations/env.py

The `migrations/env.py` file needs to know about your models and database. Update it to:

1. Import your models and settings
2. Set `target_metadata = Base.metadata`
3. Convert async database URL to sync (Alembic uses psycopg2, not asyncpg)

**Key changes needed**:
- Add imports: `from config import settings` and `from models.user import Base`
- Replace `target_metadata = None` with `target_metadata = Base.metadata`
- Create `get_url()` function to convert `postgresql+asyncpg://` to `postgresql://`

See the tutorial in env.py or ask for guidance!

- [x] Alembic initialized
- [x] env.py configured with Base.metadata
- [x] URL conversion for sync driver

### 3. Install Sync Database Driver

Alembic needs the sync PostgreSQL driver (your app uses the async one):

```bash
pip install psycopg2-binary
```

This allows Alembic to connect to PostgreSQL for running migrations.

- [x] psycopg2-binary installed

### 4. Create Initial Migration

Use autogenerate to create migration from your User model:

```bash
# Auto-generate migration from models
alembic revision --autogenerate -m "create users table"

# This creates a file in migrations/versions/
# Review the generated migration before applying!
```

**Expected**: Alembic detects your User model and generates the migration code.

- [x] Migration created
- [x] Reviewed generated migration file

### 5. Run Migrations

Apply the migration to create the users table:

```bash
alembic upgrade head
```

**Expected**:
```
INFO [alembic.runtime.migration] Running upgrade -> <revision>, create users table
```

- [x] Migrations applied successfully

### 4. Verify Database Connection
```bash
# Connect to PostgreSQL
docker exec -it python_crud_db psql -U pythonuser -d pythoncrud

# Inside psql:
\dt          # List tables (should see 'users' table)
\d users     # Describe users table
\q           # Quit
```

**Expected**: See users table with id, name, email, created_at, updated_at columns

- [x] Can connect to database
- [x] Users table exists
- [x] Table has correct schema

---

## 📚 Documentation Check

Verify all documentation files exist:

```bash
ls -la docs/
```

**Expected files**:
- [x] LEARNING_PATH.md
- [x] PYTHON_CONCEPTS.md
- [x] TYPESCRIPT_TO_PYTHON.md
- [x] QUICK_START.md
- [x] TDD_GUIDE.md
- [x] PROJECT_SUMMARY.md

```bash
ls -la *.md
```

- [ ] README.md exists
- [ ] task.md exists (implementation guide)
- [ ] SETUP_CHECKLIST.md exists (this file)
- [ ] START_HERE.md exists

---

## 📁 Project Structure Verification

```bash
tree -L 2 -I 'venv|__pycache__|*.pyc'
```

**Expected structure**:
```
python/
├── README.md
├── START_HERE.md
├── SETUP_CHECKLIST.md
├── docker-compose.yml
├── .env
├── .env.example
├── requirements.txt
├── pyproject.toml
├── alembic.ini
├── docs/
│   ├── LEARNING_PATH.md
│   ├── PYTHON_CONCEPTS.md
│   ├── TYPESCRIPT_TO_PYTHON.md
│   ├── QUICK_START.md
│   ├── TDD_GUIDE.md
│   └── PROJECT_SUMMARY.md
├── migrations/
│   └── versions/
├── src/
│   ├── main.py
│   ├── config.py
│   ├── db/
│   ├── models/
│   └── handlers/
└── tests/
    ├── conftest.py
    ├── test_calculator.py
    └── test_users.py
```

- [ ] Project structure matches

---

## 🎯 Ready to Start!

If all checkboxes are checked, you're ready to begin!

### Choose Your Learning Path:

**Option 1: Structured Learning (Recommended)**
→ Open [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) and follow Phase 0

**Option 2: Conceptual First**
→ Read [docs/TYPESCRIPT_TO_PYTHON.md](docs/TYPESCRIPT_TO_PYTHON.md), then LEARNING_PATH

**Option 3: Learn by Doing**
→ Jump into [docs/QUICK_START.md](docs/QUICK_START.md)

---

## 🆘 Troubleshooting

### Python version issues
```bash
# Use python3 explicitly
python3 --version
python3 -m venv venv
```

### Virtual environment activation issues
```bash
# Linux/macOS
source venv/bin/activate

# Windows PowerShell
venv\Scripts\Activate.ps1

# Windows CMD
venv\Scripts\activate.bat
```

### Docker permission denied (Linux)
```bash
# Add user to docker group
sudo usermod -aG docker $USER
# Then log out and back in
```

### Port 8000 already in use
Edit `.env`:
```
PORT=8080
```

### Port 5432 conflict with Rust project
```bash
# The docker-compose.yml uses port 5433 to avoid conflict
# DATABASE_URL should use localhost:5433
```

### Database connection fails
```bash
# Reset database
docker-compose down -v
docker-compose up -d
alembic upgrade head
```

### Import errors
```bash
# Make sure virtual environment is activated
# Reinstall dependencies
pip install -r requirements.txt
```

---

## 📞 Getting Help

**Python errors**: Read the traceback from bottom to top

**Documentation**: All guides are in the `docs/` folder

**Stuck?**: Check [docs/PYTHON_CONCEPTS.md](docs/PYTHON_CONCEPTS.md) for concept explanations

**Type hints**: Use an IDE with Python support (VS Code with Python extension, PyCharm)

---

**Everything working?** Time to start learning! 🚀

Head to [docs/LEARNING_PATH.md](docs/LEARNING_PATH.md) to begin your journey.
