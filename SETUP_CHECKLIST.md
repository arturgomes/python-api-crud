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

- [ ] Python 3.11+ installed
- [ ] pip installed

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

- [ ] Docker installed
- [ ] Docker Desktop running

---

## 🚀 Project Setup

### 1. Navigate to Project
```bash
cd python-api-crud
```

- [ ] In project directory

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

- [ ] Virtual environment created
- [ ] Virtual environment activated

### 3. Install Dependencies
```bash
pip3 install --upgrade pip
pip3 install -r requirements.txt
```

**Expected**: Installs FastAPI, SQLAlchemy, pytest, and other dependencies

- [ ] Dependencies installed successfully

### 4. Copy Environment File
```bash
cp .env.example .env
```

**Verify**:
```bash
cat .env
```

Should see DATABASE_URL, PORT, etc.

- [ ] .env file exists with correct values

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

- [ ] PostgreSQL container running

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

- [ ] Server starts without errors

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

- [ ] Addition works
- [ ] Division works
- [ ] Error handling works

### 3. Check API Documentation
Open browser: http://localhost:8000/docs

**Expected**: Interactive Swagger UI with API documentation

- [ ] Swagger UI loads
- [ ] Calculator endpoint visible

### 4. Stop Server
Press `Ctrl+C` in the terminal running the server

- [ ] Server stops cleanly

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

- [ ] Calculator tests pass
- [ ] User tests fail (expected - you'll implement them!)

---

## 🗄️ Phase 1: Database Verification

### 1. Initialize Database (Using Alembic)

First, create the Alembic configuration:

```bash
# Initialize Alembic
alembic init migrations

# This creates:
# - alembic.ini (configuration)
# - migrations/ (migration directory)
```

Then edit `alembic.ini` and update:
```ini
sqlalchemy.url = postgresql+asyncpg://pythonuser:pythonpass@localhost:5433/pythoncrud
```

- [ ] Alembic initialized

### 2. Create Initial Migration
```bash
# Create migration for users table
alembic revision -m "create users table"

# Edit the generated file in migrations/versions/
# Add the SQL to create users table (see migrations/001_create_users.sql)
```

- [ ] Migration created

### 3. Run Migrations
```bash
alembic upgrade head
```

**Expected**:
```
INFO [alembic.runtime.migration] Running upgrade -> <revision>, create users table
```

- [ ] Migrations applied successfully

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

- [ ] Can connect to database
- [ ] Users table exists
- [ ] Table has correct schema

---

## 📚 Documentation Check

Verify all documentation files exist:

```bash
ls -la docs/
```

**Expected files**:
- [ ] LEARNING_PATH.md
- [ ] PYTHON_CONCEPTS.md
- [ ] TYPESCRIPT_TO_PYTHON.md
- [ ] QUICK_START.md
- [ ] TDD_GUIDE.md
- [ ] PROJECT_SUMMARY.md

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
