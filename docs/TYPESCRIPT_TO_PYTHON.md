# 🔄 TypeScript to Python Translation Guide

**Bridge your JavaScript/TypeScript knowledge to Python**

This guide maps familiar TypeScript concepts to their Python equivalents, helping you leverage your existing knowledge while learning Python web development with FastAPI.

---

## 🎯 Philosophy Differences

### TypeScript
- **Runtime**: Node.js / Browser (V8 engine)
- **Typing**: Optional static typing (via TypeScript compiler)
- **Execution**: JIT compiled JavaScript
- **Async**: Built-in event loop, just use `async/await`
- **Memory**: Garbage collected automatically

### Python
- **Runtime**: CPython interpreter (or PyPy, etc.)
- **Typing**: Optional type hints (checked by mypy/pyright)
- **Execution**: Interpreted bytecode
- **Async**: Explicit runtime (asyncio, must understand event loop)
- **Memory**: Garbage collected with reference counting

---

## 📦 Project Structure & Tooling

### Package Management

**TypeScript (npm/yarn)**
```json
{
  "dependencies": {
    "express": "^4.18.0",
    "typeorm": "^0.3.0"
  },
  "devDependencies": {
    "@types/node": "^18.0.0",
    "typescript": "^5.0.0"
  }
}
```

**Python (pip + requirements.txt or pyproject.toml)**
```txt
# requirements.txt
fastapi==0.104.1
sqlalchemy[asyncio]==2.0.23
uvicorn==0.24.0

# Development dependencies
pytest==7.4.3
mypy==1.7.0
ruff==0.1.6
```

**Key Differences**:
- Python uses virtual environments (`venv`) instead of `node_modules`
- No separate type package (types built into libraries or stubs)
- Simpler dependency resolution (no lockfiles by default, though tools exist)

### Scripts & Commands

| TypeScript (npm)          | Python (direct)            |
|---------------------------|----------------------------|
| `npm install`             | `pip install -r requirements.txt` |
| `npm run dev`             | `uvicorn main:app --reload` |
| `npm test`                | `pytest`                   |
| `npm run build`           | N/A (Python is interpreted) |
| `tsc --noEmit`            | `mypy src/`                |
| `eslint .`                | `ruff check src/`          |

---

## 🔤 Basic Syntax Comparison

### Variable Declaration

**TypeScript**
```typescript
const name: string = "Alice";
let count: number = 0;
var oldStyle: boolean = true; // avoid
```

**Python**
```python
name: str = "Alice"  # Type hint is optional but recommended
count: int = 0
# No 'const' - use UPPERCASE by convention for constants
PI: float = 3.14159
```

**Key Differences**:
- Python has no `const` keyword - immutability comes from data types
- Use `UPPERCASE` naming convention for constants
- Type hints are optional (runtime doesn't enforce them)
- No `var`/`let`/`const` distinction

### Functions

**TypeScript**
```typescript
// Regular function
function add(a: number, b: number): number {
  return a + b;
}

// Arrow function
const multiply = (a: number, b: number): number => a * b;

// Async function
async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/users/${id}`);
  return response.json();
}
```

**Python**
```python
# Regular function
def add(a: int, b: int) -> int:
    return a + b

# Lambda (limited to single expression)
multiply = lambda a, b: a * b

# Async function
async def fetch_user(user_id: str) -> User:
    response = await client.get(f"/users/{user_id}")
    return response.json()
```

**Key Differences**:
- Use `def` instead of `function`
- Lambda is limited (use for simple operations only)
- Type hints use `:` before type, `->` for return type
- Indentation defines scope (no braces `{}`)

### Classes

**TypeScript**
```typescript
class User {
  private id: string;
  public name: string;

  constructor(id: string, name: string) {
    this.id = id;
    this.name = name;
  }

  public greet(): string {
    return `Hello, ${this.name}`;
  }
}

const user = new User("123", "Alice");
```

**Python**
```python
class User:
    def __init__(self, user_id: str, name: str):
        self._id: str = user_id  # Convention: _ prefix for private
        self.name: str = name

    def greet(self) -> str:
        return f"Hello, {self.name}"

user = User("123", "Alice")  # No 'new' keyword
```

**Key Differences**:
- No explicit access modifiers (`private`, `public`)
- Use naming conventions (`_private`, `__very_private`)
- Constructor is `__init__` (dunder/magic method)
- First parameter is always `self` (explicit vs implicit `this`)
- No `new` keyword for instantiation

---

## 🎨 Type System Comparison

### Basic Types

| TypeScript | Python | Notes |
|------------|--------|-------|
| `string` | `str` | Text |
| `number` | `int`, `float` | JS has one number type, Python separates |
| `boolean` | `bool` | True/False capitalized in Python |
| `any` | `Any` | From `typing` module |
| `unknown` | - | Use type guards or `Any` |
| `void` | `None` | Function returns nothing |
| `never` | `NoReturn` | Function never returns |
| `null`, `undefined` | `None` | Python has only None |

### Arrays & Lists

**TypeScript**
```typescript
const numbers: number[] = [1, 2, 3];
const users: Array<User> = [];
```

**Python**
```python
from typing import List

numbers: List[int] = [1, 2, 3]
users: List[User] = []

# Python 3.9+ - can use built-in types
numbers: list[int] = [1, 2, 3]
users: list[User] = []
```

### Objects & Dictionaries

**TypeScript**
```typescript
// Interface
interface User {
  id: string;
  name: string;
  email?: string;  // Optional
}

// Type alias
type UserRole = "admin" | "user";

// Object
const user: User = {
  id: "123",
  name: "Alice"
};
```

**Python**
```python
from typing import Optional, Literal
from pydantic import BaseModel

# Pydantic model (preferred for API schemas)
class User(BaseModel):
    id: str
    name: str
    email: Optional[str] = None  # Optional with default

# TypedDict (for dictionaries)
from typing import TypedDict

class UserDict(TypedDict):
    id: str
    name: str

# Literal types (like string unions)
UserRole = Literal["admin", "user"]

# Dictionary
user: dict[str, Any] = {
    "id": "123",
    "name": "Alice"
}
```

**Key Differences**:
- Python uses `Optional[T]` for nullable types
- Pydantic models provide runtime validation (huge advantage!)
- `dict` is built-in (no need for `{}` type syntax)
- Use `Literal` for string unions

### Generics

**TypeScript**
```typescript
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

class Box<T> {
  constructor(private value: T) {}

  getValue(): T {
    return this.value;
  }
}
```

**Python**
```python
from typing import TypeVar, Generic, Optional

T = TypeVar('T')

def first(arr: list[T]) -> Optional[T]:
    return arr[0] if arr else None

class Box(Generic[T]):
    def __init__(self, value: T):
        self._value = value

    def get_value(self) -> T:
        return self._value
```

---

## ⚡ Async Programming

### Basic Async/Await

**TypeScript (Node.js)**
```typescript
// Async is built into Node.js runtime
async function getUser(id: string): Promise<User> {
  const response = await fetch(`/users/${id}`);
  return response.json();
}

// Top-level await (ES2022+)
const user = await getUser("123");
```

**Python (asyncio)**
```python
import asyncio
from typing import Awaitable

# Need explicit async runtime
async def get_user(user_id: str) -> User:
    response = await client.get(f"/users/{user_id}")
    return response.json()

# Top-level await only in REPL or with asyncio.run()
async def main():
    user = await get_user("123")

# Run the event loop
if __name__ == "__main__":
    asyncio.run(main())
```

**Key Differences**:
- Python requires explicit event loop management
- FastAPI handles the event loop for you in web context
- Use `asyncio.run()` for CLI scripts
- Must import `asyncio` module

### Parallel Execution

**TypeScript**
```typescript
// Execute multiple promises in parallel
const [user, posts, comments] = await Promise.all([
  getUser(id),
  getPosts(id),
  getComments(id)
]);

// Race (first to complete wins)
const result = await Promise.race([
  fetchFromCache(),
  fetchFromDB()
]);
```

**Python**
```python
import asyncio

# Execute multiple coroutines in parallel
user, posts, comments = await asyncio.gather(
    get_user(user_id),
    get_posts(user_id),
    get_comments(user_id)
)

# Race (first to complete wins)
done, pending = await asyncio.wait(
    [fetch_from_cache(), fetch_from_db()],
    return_when=asyncio.FIRST_COMPLETED
)
result = done.pop().result()
```

---

## 🚨 Error Handling

### Exceptions vs Promises

**TypeScript**
```typescript
// Promise-based
async function getUser(id: string): Promise<User> {
  try {
    const response = await fetch(`/users/${id}`);
    if (!response.ok) {
      throw new Error(`User not found: ${id}`);
    }
    return response.json();
  } catch (error) {
    console.error("Failed to get user:", error);
    throw error;
  }
}

// Result type pattern (not built-in)
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };
```

**Python**
```python
# Exception-based (similar to TypeScript)
async def get_user(user_id: str) -> User:
    try:
        response = await client.get(f"/users/{user_id}")
        if response.status_code != 200:
            raise ValueError(f"User not found: {user_id}")
        return response.json()
    except Exception as error:
        print(f"Failed to get user: {error}")
        raise

# Result type pattern (using library or custom)
from typing import Union

class Ok[T]:
    def __init__(self, value: T):
        self.value = value

class Err[E]:
    def __init__(self, error: E):
        self.error = error

Result = Union[Ok[T], Err[E]]
```

### Custom Exceptions

**TypeScript**
```typescript
class NotFoundError extends Error {
  constructor(message: string) {
    super(message);
    this.name = "NotFoundError";
  }
}

throw new NotFoundError("User not found");
```

**Python**
```python
class NotFoundError(Exception):
    """Raised when a resource is not found."""
    pass

raise NotFoundError("User not found")
```

---

## 🌐 Web Framework Comparison (Express vs FastAPI)

### Basic Server Setup

**TypeScript (Express)**
```typescript
import express from 'express';

const app = express();
app.use(express.json());

app.get('/users/:id', async (req, res) => {
  const user = await getUser(req.params.id);
  res.json(user);
});

app.listen(3000, () => {
  console.log('Server running on port 3000');
});
```

**Python (FastAPI)**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/users/{user_id}")
async def read_user(user_id: str) -> User:
    user = await get_user(user_id)
    return user  # Automatically serialized to JSON

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Key Differences**:
- FastAPI uses decorators for routes
- Automatic JSON serialization based on return type
- Built-in request/response validation
- No need for `express.json()` middleware

### Request Body Validation

**TypeScript (Express + class-validator)**
```typescript
import { IsString, IsEmail } from 'class-validator';

class CreateUserDto {
  @IsString()
  name: string;

  @IsEmail()
  email: string;
}

app.post('/users', async (req, res) => {
  const dto = plainToClass(CreateUserDto, req.body);
  const errors = await validate(dto);

  if (errors.length > 0) {
    return res.status(400).json({ errors });
  }

  const user = await createUser(dto);
  res.status(201).json(user);
});
```

**Python (FastAPI with Pydantic)**
```python
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr

@app.post("/users", status_code=201)
async def create_user(user: UserCreate) -> User:
    # Validation happens automatically!
    created_user = await create_user_in_db(user)
    return created_user
```

**Key Differences**:
- Pydantic validation is automatic (no manual validation needed)
- Type hints drive both validation and documentation
- Cleaner, less boilerplate code

---

## 🗄️ Database ORM Comparison (TypeORM vs SQLAlchemy)

### Model Definition

**TypeScript (TypeORM)**
```typescript
import { Entity, Column, PrimaryGeneratedColumn } from 'typeorm';

@Entity()
export class User {
  @PrimaryGeneratedColumn('uuid')
  id: string;

  @Column()
  name: string;

  @Column({ unique: true })
  email: string;

  @Column({ type: 'timestamp', default: () => 'CURRENT_TIMESTAMP' })
  createdAt: Date;
}
```

**Python (SQLAlchemy)**
```python
from sqlalchemy import Column, String, DateTime, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
```

### Queries

**TypeScript (TypeORM)**
```typescript
// Find one
const user = await userRepo.findOne({ where: { id } });

// Find many
const users = await userRepo.find({
  where: { email: Like('%@example.com') },
  take: 10,
  skip: 0
});

// Create
const user = userRepo.create({ name: "Alice", email: "alice@example.com" });
await userRepo.save(user);

// Update
await userRepo.update({ id }, { name: "Alice Smith" });

// Delete
await userRepo.delete({ id });
```

**Python (SQLAlchemy Async)**
```python
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# Find one
result = await session.execute(select(User).where(User.id == user_id))
user = result.scalar_one_or_none()

# Find many
result = await session.execute(
    select(User)
    .where(User.email.like('%@example.com'))
    .offset(0)
    .limit(10)
)
users = result.scalars().all()

# Create
user = User(name="Alice", email="alice@example.com")
session.add(user)
await session.commit()

# Update
user.name = "Alice Smith"
await session.commit()

# Delete
await session.delete(user)
await session.commit()
```

**Key Differences**:
- SQLAlchemy uses explicit `select()` queries
- Must manually commit changes
- More verbose but more explicit control

---

## 📚 Common Patterns

### Null/Undefined Handling

**TypeScript**
```typescript
// Null coalescing
const name = user.name ?? "Unknown";

// Optional chaining
const city = user?.address?.city;

// Nullish assignment
user.name ??= "Default";
```

**Python**
```python
# Equivalent using 'or' (for falsy values) or ternary
name = user.name or "Unknown"

# No optional chaining - use getattr or check manually
city = getattr(getattr(user, 'address', None), 'city', None)

# Or safer with walrus operator (Python 3.8+)
if address := getattr(user, 'address', None):
    city = getattr(address, 'city', None)

# Default assignment
user.name = user.name or "Default"
```

### Array/List Operations

**TypeScript**
```typescript
const numbers = [1, 2, 3, 4, 5];

// Map
const doubled = numbers.map(n => n * 2);

// Filter
const evens = numbers.filter(n => n % 2 === 0);

// Reduce
const sum = numbers.reduce((acc, n) => acc + n, 0);

// Find
const first = numbers.find(n => n > 3);

// Some/Every
const hasEven = numbers.some(n => n % 2 === 0);
const allPositive = numbers.every(n => n > 0);
```

**Python**
```python
numbers = [1, 2, 3, 4, 5]

# Map (prefer list comprehension)
doubled = [n * 2 for n in numbers]

# Filter (prefer list comprehension)
evens = [n for n in numbers if n % 2 == 0]

# Reduce
from functools import reduce
sum_result = reduce(lambda acc, n: acc + n, numbers, 0)
# Or just use built-in: sum(numbers)

# Find
first = next((n for n in numbers if n > 3), None)

# Some/Every
has_even = any(n % 2 == 0 for n in numbers)
all_positive = all(n > 0 for n in numbers)
```

**Key Difference**: Python prefers **list comprehensions** over map/filter

### Destructuring

**TypeScript**
```typescript
// Array destructuring
const [first, second, ...rest] = [1, 2, 3, 4, 5];

// Object destructuring
const { name, email } = user;
const { name: userName, email: userEmail } = user;
```

**Python**
```python
# Sequence unpacking (similar to array destructuring)
first, second, *rest = [1, 2, 3, 4, 5]

# No object destructuring - access attributes directly
name = user.name
email = user.email

# Or use getattr for dynamic access
user_name = getattr(user, 'name')
```

---

## 🔧 Development Workflow

### TypeScript Project
```bash
# Setup
npm init -y
npm install express typeorm
npm install -D typescript @types/node ts-node

# Development
npm run dev  # Uses ts-node or nodemon

# Type checking
tsc --noEmit

# Linting
eslint .

# Testing
jest
```

### Python Project
```bash
# Setup
python -m venv venv
source venv/bin/activate
pip install fastapi sqlalchemy uvicorn

# Development
uvicorn main:app --reload

# Type checking
mypy src/

# Linting
ruff check src/

# Testing
pytest
```

---

## 🎯 Mental Model Summary

### Key Mindset Shifts

1. **Indentation Matters**: Python uses indentation for scope (no braces)
2. **Explicit is Better**: Python philosophy values clarity over cleverness
3. **Duck Typing**: "If it quacks like a duck..." - Python cares about behavior, not types
4. **Batteries Included**: Rich standard library (like `itertools`, `collections`)
5. **One Way to Do It**: Python encourages "Pythonic" solutions (PEP 8, PEP 20)

### Common Gotchas for TypeScript Developers

1. **No Hoisting**: Variables must be defined before use
2. **Truthiness Different**: Empty list `[]` is falsy, `"0"` is truthy
3. **String Quotes**: Single and double quotes are identical (no template literals with ``)
4. **Integer Division**: `//` for integer division, `/` for float division
5. **No Semicolons**: Optional, but typically omitted
6. **Comparison**: Use `is` for identity, `==` for equality

---

## 📖 Next Steps

1. Read [PYTHON_CONCEPTS.md](./PYTHON_CONCEPTS.md) for deep dives into Python-specific features
2. Follow [LEARNING_PATH.md](./LEARNING_PATH.md) for structured hands-on learning
3. Reference [QUICK_START.md](./QUICK_START.md) for fast implementation patterns
4. Study [TDD_GUIDE.md](./TDD_GUIDE.md) for Python testing approaches

**Remember**: Your TypeScript knowledge is valuable! Python is just a different tool in your toolkit. 🚀
