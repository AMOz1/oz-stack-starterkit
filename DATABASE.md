# SQLite Database Guide

This guide explains how to use the SQLite database integration in the Oz Stack Starter Kit.

## Overview

The Oz Stack Starter Kit includes a complete SQLite database setup using SQLAlchemy ORM and Alembic for migrations. This provides:

- Easy database access and querying with SQLAlchemy
- Type-safe database models
- Database schema versioning with Alembic
- Simple CRUD operations
- Integration with FastAPI and Pydantic

## Getting Started

### Database Configuration

The database connection is configured in `src/database/db.py`. By default, it uses a SQLite database located at `./app.db`.

You can change the database URL by setting the `DATABASE_URL` environment variable in your `.env` file:

```
DATABASE_URL=sqlite:///./custom_name.db
```

### Creating Models

Database models are defined in `src/database/models.py` using SQLAlchemy's declarative syntax.

Example of creating a new model:

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Relationship to other tables
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    
    # Relationship to User
    owner = relationship("User", back_populates="tasks")
```

### Schemas

Pydantic schemas for request/response validation are defined in `src/database/schemas.py`:

```python
from pydantic import BaseModel
from typing import Optional, List

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
```

### CRUD Operations

CRUD (Create, Read, Update, Delete) operations are implemented in `src/database/crud.py`:

```python
from sqlalchemy.orm import Session
from . import models, schemas

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(username=user.username, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
```

## Database Migrations

The Oz Stack Starter Kit uses Alembic for database migrations, which allows you to:

- Track database schema changes
- Upgrade and downgrade the database schema
- Generate migration scripts automatically

### Creating Migrations

To create a new migration after changing your models:

```bash
# Navigate to the src/database directory
cd src/database

# Generate a migration
alembic revision --autogenerate -m "Description of changes"
```

### Applying Migrations

To apply migrations:

```bash
# Navigate to the src/database directory
cd src/database

# Apply all pending migrations
alembic upgrade head

# Or apply a specific number of migrations
alembic upgrade +1
```

### Rolling Back Migrations

To roll back a migration:

```bash
# Navigate to the src/database directory
cd src/database

# Roll back one migration
alembic downgrade -1

# Roll back all migrations
alembic downgrade base
```

## Using the Database in FastAPI

### Dependency Injection

To use the database in your FastAPI routes:

```python
from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from src.database import crud, models, schemas, db

router = APIRouter()

@router.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(db.get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(db.get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db=db, user=user)
```

## SQLite-Specific Considerations

### Concurrency

SQLite has limitations with concurrent writes. If you need concurrent access, consider:

1. Using connection pooling with a small pool size
2. Adding retry logic for database write operations
3. For high concurrency needs, consider switching to PostgreSQL or MySQL

### Performance Tuning

To optimize SQLite performance:

1. Use indexes for frequently queried columns
2. Run `PRAGMA optimize` periodically
3. Use transactions for multiple operations
4. Enable Write-Ahead Logging (WAL) mode for better concurrency

```python
# In your db.py file
engine = create_engine(
    SQLITE_DATABASE_URL, 
    connect_args={
        "check_same_thread": False,
        "timeout": 30
    }
)

# Enable WAL mode
with engine.connect() as conn:
    conn.execute("PRAGMA journal_mode=WAL")
```

## Common SQLite Operations

### Querying Data

```python
# Get a single item
item = db.query(models.Item).filter(models.Item.id == item_id).first()

# Get multiple items with filtering
items = db.query(models.Item).filter(models.Item.is_active == True).all()

# Get items with ordering
items = db.query(models.Item).order_by(models.Item.created_at.desc()).all()

# Get items with pagination
items = db.query(models.Item).offset(skip).limit(limit).all()

# Get count of items
count = db.query(models.Item).filter(models.Item.status == "pending").count()
```

### Relationships

```python
# Get user with related tasks
user = db.query(models.User).options(joinedload(models.User.tasks)).filter(models.User.id == user_id).first()

# Access related items
for task in user.tasks:
    print(task.title)
```

### Raw SQL

If needed, you can execute raw SQL:

```python
from sqlalchemy import text

result = db.execute(text("SELECT * FROM users WHERE username = :username"), {"username": "john"})
users = result.fetchall()
```

## Backup and Restore

### Backing Up SQLite Database

```bash
# Using the sqlite3 command line tool
sqlite3 app.db ".backup app.db.backup"

# Using Python
import sqlite3
conn = sqlite3.connect('app.db')
backup_conn = sqlite3.connect('app.db.backup')
conn.backup(backup_conn)
backup_conn.close()
conn.close()
```

### Restoring SQLite Database

```bash
# Using the sqlite3 command line tool
sqlite3 app.db ".restore app.db.backup"

# Using Python
import sqlite3
backup_conn = sqlite3.connect('app.db.backup')
conn = sqlite3.connect('app.db')
backup_conn.backup(conn)
conn.close()
backup_conn.close()
```

## Testing with SQLite

For testing, you can use an in-memory SQLite database:

```python
# In your test setup
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Replace the normal get_db with our test database
app.dependency_overrides[get_db] = override_get_db
```