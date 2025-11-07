# Python Concepts - Quick Reference

Quick reference guide for TypeScript/Rust engineers learning Python.

---

## 📊 Comparison Tables

### Type Systems

| Concept | TypeScript | Rust | Python |
|---------|-----------|------|---------|
| **Type Checking** | Compile-time (optional) | Compile-time (strict) | Runtime (optional) |
| **Type Annotations** | `name: string` | `name: String` | `name: str` |
| **Optional Types** | `string \| null` | `Option<String>` | `Optional[str]` |
| **Union Types** | `string \| number` | `enum Value { Str(String), Num(i32) }` | `Union[str, int]` |
| **Generics** | `Array<T>` | `Vec<T>` | `List[T]` |
| **Type Inference** | Yes | Yes | Limited |

### Error Handling

| Concept | TypeScript | Rust | Python |
|---------|-----------|------|---------|
| **Mechanism** | try/catch | Result<T, E> | try/except |
| **Nullable** | null/undefined | Option<T> | None/Optional[T] |
| **Custom Errors** | Error classes | enum Error | Exception classes |
| **Propagation** | throw | ? operator | raise |

### Async/Await

| Concept | TypeScript | Rust | Python |
|---------|-----------|------|---------|
| **Runtime** | Event loop (Node.js) | Tokio | asyncio |
| **Syntax** | `async function` | `async fn` | `async def` |
| **Await** | `await promise` | `.await` | `await coroutine` |
| **Concurrency** | Single-threaded | Multi-threaded | Single-threaded (default) |

---

## 🐍 Python Fundamentals for TS/Rust Developers

### 1. Type Hints (Optional but Recommended)

```python
# Basic types
name: str = "Alice"
age: int = 30
score: float = 95.5
is_active: bool = True

# Collections
names: list[str] = ["Alice", "Bob"]
scores: dict[str, int] = {"Alice": 95, "Bob": 87}
unique_ids: set[int] = {1, 2, 3}

# Optional (nullable)
from typing import Optional
middle_name: Optional[str] = None  # Can be str or None

# Union types
from typing import Union
value: Union[int, str] = "hello"  # Can be int or str

# Functions
def greet(name: str) -> str:
    return f"Hello, {name}!"

# Async functions
async def fetch_user(id: int) -> Optional[User]:
    # ...
    pass
```

**Compare to Rust:**
```rust
// Rust requires explicit types
let name: String = "Alice".to_string();
let age: i32 = 30;
let middle_name: Option<String> = None;

async fn fetch_user(id: i32) -> Option<User> {
    // ...
}
```

**Compare to TypeScript:**
```typescript
// TypeScript similar to Python type hints
const name: string = "Alice";
const age: number = 30;
const middleName: string | null = null;

async function fetchUser(id: number): Promise<User | null> {
    // ...
}
```

---

### 2. None vs null vs Option

```python
# Python uses None
def find_user(id: int) -> Optional[User]:
    user = db.query(User).filter(User.id == id).first()
    if user is None:
        return None
    return user

# Check for None
if user is not None:
    print(user.name)

# Alternative: walrus operator (Python 3.8+)
if (user := find_user(123)) is not None:
    print(user.name)
```

**Compare to Rust:**
```rust
fn find_user(id: i32) -> Option<User> {
    // Returns Some(user) or None
}

// Pattern matching
match find_user(123) {
    Some(user) => println!("{}", user.name),
    None => println!("Not found")
}

// Or use if let
if let Some(user) = find_user(123) {
    println!("{}", user.name);
}
```

---

### 3. Error Handling

```python
# Python uses exceptions
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Division by zero")
    return a / b

# Try/except
try:
    result = divide(10, 0)
except ValueError as e:
    print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
finally:
    print("Cleanup")
```

**Compare to Rust:**
```rust
// Rust uses Result
fn divide(a: f64, b: f64) -> Result<f64, String> {
    if b == 0.0 {
        Err("Division by zero".to_string())
    } else {
        Ok(a / b)
    }
}

// Pattern matching
match divide(10.0, 0.0) {
    Ok(result) => println!("{}", result),
    Err(e) => println!("Error: {}", e)
}

// Or use ? operator
fn calculate() -> Result<f64, String> {
    let result = divide(10.0, 2.0)?;  // Propagates error
    Ok(result * 2.0)
}
```

---

### 4. Async/Await

```python
import asyncio

# Async function
async def fetch_user(id: int) -> User:
    # Simulate async operation
    await asyncio.sleep(1)
    return User(id=id, name="Alice")

# Await async function
async def main():
    user = await fetch_user(123)
    print(user.name)

# Run async code
if __name__ == "__main__":
    asyncio.run(main())

# Multiple concurrent operations
async def fetch_multiple_users(ids: list[int]) -> list[User]:
    tasks = [fetch_user(id) for id in ids]
    users = await asyncio.gather(*tasks)  # Concurrent execution
    return users
```

**Compare to Rust (Tokio):**
```rust
use tokio;

async fn fetch_user(id: i32) -> User {
    tokio::time::sleep(Duration::from_secs(1)).await;
    User { id, name: "Alice".to_string() }
}

#[tokio::main]
async fn main() {
    let user = fetch_user(123).await;
    println!("{}", user.name);
}

// Multiple concurrent operations
async fn fetch_multiple_users(ids: Vec<i32>) -> Vec<User> {
    let tasks: Vec<_> = ids.into_iter()
        .map(|id| fetch_user(id))
        .collect();
    futures::future::join_all(tasks).await
}
```

---

### 5. Context Managers (with statement)

```python
# Automatic resource management
async with db_session() as session:
    user = await session.execute(select(User))
    # session automatically closed

# File handling
with open("file.txt", "r") as f:
    content = f.read()
    # file automatically closed

# Custom context manager
class DatabaseConnection:
    async def __aenter__(self):
        self.conn = await create_connection()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()
```

**Compare to Rust:**
```rust
// Rust uses RAII (Resource Acquisition Is Initialization)
// Resources automatically cleaned up when going out of scope

{
    let file = File::open("file.txt")?;
    // file automatically closed when leaving scope
}

// No direct equivalent to context managers
// Use Drop trait for custom cleanup
```

---

### 6. Decorators

```python
# Function decorators
@app.get("/users/{id}")
async def get_user(id: int):
    # Decorator registers route
    pass

# Class decorators
@dataclass
class User:
    id: int
    name: str

# Custom decorator
from functools import wraps

def log_calls(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        print(f"Calling {func.__name__}")
        result = await func(*args, **kwargs)
        print(f"Finished {func.__name__}")
        return result
    return wrapper

@log_calls
async def fetch_user(id: int):
    pass
```

**Compare to Rust:**
```rust
// Rust uses procedural macros
#[derive(Debug, Serialize, Deserialize)]
struct User {
    id: i32,
    name: String,
}

// Attribute macros
#[tokio::test]
async fn test_user() {
    // ...
}

// No direct equivalent to function decorators
// Use macros or function composition
```

---

## 🔧 Common Patterns

### 1. Pydantic Models

```python
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from uuid import UUID

class UserBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    email: EmailStr

class UserCreate(UserBase):
    """Request model for creating user"""
    pass

class UserResponse(UserBase):
    """Response model with all fields"""
    id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Allow creation from SQLAlchemy models

# Usage
user_data = UserCreate(name="Alice", email="alice@example.com")
# Automatically validated!

# Invalid data raises ValidationError
try:
    invalid = UserCreate(name="", email="not-an-email")
except ValidationError as e:
    print(e.errors())
```

**Compare to Rust (serde):**
```rust
use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};

#[derive(Deserialize)]
struct UserCreate {
    name: String,
    email: String,
}

#[derive(Serialize)]
struct UserResponse {
    id: Uuid,
    name: String,
    email: String,
    created_at: DateTime<Utc>,
    updated_at: DateTime<Utc>,
}

// Validation must be done manually or with validator crate
```

---

### 2. FastAPI Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# Dependency function
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

# Use in route
@app.get("/users/{id}")
async def get_user(
    id: UUID,  # Path parameter
    db: AsyncSession = Depends(get_db)  # Injected dependency
):
    user = await db.execute(select(User).where(User.id == id))
    return user.scalar_one_or_none()

# Multiple dependencies
async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    # Decode token, get user
    pass

@app.get("/me")
async def read_users_me(
    current_user: User = Depends(get_current_user)
):
    return current_user
```

**Compare to Rust (Axum):**
```rust
// Axum uses extractors
async fn get_user(
    Path(id): Path<Uuid>,  // Path extractor
    State(pool): State<PgPool>  // State extractor
) -> Result<Json<User>, AppError> {
    let user = sqlx::query_as!(User, "SELECT * FROM users WHERE id = $1", id)
        .fetch_one(&pool)
        .await?;
    Ok(Json(user))
}
```

---

### 3. SQLAlchemy Queries

```python
from sqlalchemy import select, insert, update, delete, func

# SELECT
result = await db.execute(
    select(User)
    .where(User.email == "alice@example.com")
    .order_by(User.created_at.desc())
)
user = result.scalar_one_or_none()

# COUNT
result = await db.execute(select(func.count(User.id)))
total = result.scalar()

# INSERT
new_user = User(name="Alice", email="alice@example.com")
db.add(new_user)
await db.commit()
await db.refresh(new_user)  # Get generated fields

# UPDATE (method 1: update object)
user.name = "Bob"
await db.commit()

# UPDATE (method 2: statement)
await db.execute(
    update(User)
    .where(User.id == user_id)
    .values(name="Bob")
)
await db.commit()

# DELETE
await db.execute(
    delete(User).where(User.id == user_id)
)
await db.commit()

# Pagination
page = 1
page_size = 10
offset = (page - 1) * page_size

result = await db.execute(
    select(User)
    .order_by(User.created_at.desc())
    .offset(offset)
    .limit(page_size)
)
users = result.scalars().all()
```

---

## 🎯 Python Idioms

### 1. List Comprehensions

```python
# List comprehension
squares = [x**2 for x in range(10)]

# With condition
even_squares = [x**2 for x in range(10) if x % 2 == 0]

# Dict comprehension
user_dict = {user.id: user.name for user in users}

# Set comprehension
unique_emails = {user.email.lower() for user in users}
```

### 2. Unpacking

```python
# Tuple unpacking
name, email = "Alice", "alice@example.com"

# List unpacking
first, *rest, last = [1, 2, 3, 4, 5]

# Dict unpacking
defaults = {"page": 1, "page_size": 10}
params = {**defaults, "page": 2}  # Merge dicts
```

### 3. String Formatting

```python
name = "Alice"
age = 30

# f-strings (recommended)
message = f"Hello, {name}! You are {age} years old."

# With expressions
message = f"Next year you'll be {age + 1}!"

# Formatting
price = 19.99
message = f"Price: ${price:.2f}"  # "Price: $19.99"
```

---

## ⚠️ Common Pitfalls

### 1. Mutable Default Arguments

```python
# ❌ Wrong: Mutable default
def add_item(item, items=[]):
    items.append(item)
    return items

# ✅ Correct: Use None
def add_item(item, items=None):
    if items is None:
        items = []
    items.append(item)
    return items
```

### 2. Late Binding Closures

```python
# ❌ Wrong
functions = []
for i in range(5):
    functions.append(lambda: i)  # All will return 4!

# ✅ Correct
functions = []
for i in range(5):
    functions.append(lambda i=i: i)  # Capture i
```

### 3. Forgetting await

```python
# ❌ Wrong: Missing await
async def get_user(id: int):
    user = db.execute(select(User))  # Returns coroutine, not User!
    return user

# ✅ Correct
async def get_user(id: int):
    user = await db.execute(select(User))
    return user
```

---

## 📚 Resources

- [Python Official Tutorial](https://docs.python.org/3/tutorial/)
- [Real Python](https://realpython.com/)
- [Python Type Hints Cheat Sheet](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLAlchemy 2.0 Documentation](https://docs.sqlalchemy.org/en/20/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
