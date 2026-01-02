# Database Agent

## Purpose
Expert agent for database operations, schema management, migrations, and optimization across all phases.

## Responsibilities
- Design database schemas following project constitution
- Create and manage database migrations
- Optimize queries and add indexes
- Handle database seeding for development/testing
- Troubleshoot database connectivity issues
- Ensure data integrity and user isolation

## Database Stack by Phase

### Phase I (Console App)
- **Storage**: In-memory (Python data structures)
- **No persistence**: Data lost on exit

### Phase II-V (Web App onwards)
- **Database**: Neon Serverless PostgreSQL
- **ORM**: SQLModel (Python)
- **Migrations**: Alembic
- **Connection Pooling**: SQLAlchemy engine

## Database Schema

### Core Tables

#### users (Better Auth managed)
```sql
CREATE TABLE users (
    id          TEXT PRIMARY KEY,
    email       TEXT UNIQUE NOT NULL,
    name        TEXT,
    created_at  TIMESTAMP DEFAULT NOW()
);
```

#### tasks
```sql
CREATE TABLE tasks (
    id           SERIAL PRIMARY KEY,
    user_id      TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    title        VARCHAR(200) NOT NULL,
    description  TEXT,
    completed    BOOLEAN DEFAULT FALSE,
    priority     TEXT CHECK (priority IN ('high', 'medium', 'low')),  -- Phase II+
    due_date     TIMESTAMP,                                            -- Phase V
    created_at   TIMESTAMP DEFAULT NOW(),
    updated_at   TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_tasks_user_id ON tasks(user_id);
CREATE INDEX idx_tasks_completed ON tasks(completed);
CREATE INDEX idx_tasks_due_date ON tasks(due_date);  -- Phase V
```

#### conversations (Phase III+)
```sql
CREATE TABLE conversations (
    id          SERIAL PRIMARY KEY,
    user_id     TEXT NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    created_at  TIMESTAMP DEFAULT NOW(),
    updated_at  TIMESTAMP DEFAULT NOW()
);

-- Index
CREATE INDEX idx_conversations_user_id ON conversations(user_id);
```

#### messages (Phase III+)
```sql
CREATE TABLE messages (
    id               SERIAL PRIMARY KEY,
    conversation_id  INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    user_id          TEXT NOT NULL REFERENCES users(id),
    role            TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content         TEXT NOT NULL,
    created_at      TIMESTAMP DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## SQLModel Models

### Task Model
```python
# app/models.py
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)
    priority: Optional[str] = Field(default=None)  # Phase II+
    due_date: Optional[datetime] = None            # Phase V
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    # user: User = Relationship(back_populates="tasks")
```

### Conversation Model
```python
class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model
```python
class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    user_id: str = Field(foreign_key="users.id")
    role: str = Field()  # 'user' or 'assistant'
    content: str = Field()
    created_at: datetime = Field(default_factory=datetime.now)

    # Relationship
    conversation: Conversation = Relationship(back_populates="messages")
```

## Database Configuration

### Connection Setup
```python
# app/database.py
from sqlmodel import create_engine, Session
import os

DATABASE_URL = os.getenv("DATABASE_URL")

# Neon PostgreSQL connection
engine = create_engine(
    DATABASE_URL,
    echo=True,  # Set to False in production
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,     # Verify connections before using
    pool_recycle=3600,      # Recycle connections every hour
    connect_args={
        "sslmode": "require"  # Neon requires SSL
    }
)

def get_session():
    with Session(engine) as session:
        yield session
```

### Dependency Injection (FastAPI)
```python
from fastapi import Depends
from app.database import get_session

@app.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    session: Session = Depends(get_session)
):
    tasks = session.query(Task).filter(Task.user_id == user_id).all()
    return tasks
```

## Alembic Migrations

### Initial Setup
```bash
cd backend

# Initialize Alembic
uv run alembic init alembic

# Edit alembic.ini
# Set: sqlalchemy.url = postgresql://...

# Or use env variable (recommended)
# In alembic/env.py:
```

```python
# alembic/env.py
import os
from app.models import SQLModel

config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL"))
target_metadata = SQLModel.metadata
```

### Create Migration
```bash
# Auto-generate migration from models
uv run alembic revision --autogenerate -m "Create tasks table"

# Review generated migration in alembic/versions/
```

### Apply Migration
```bash
# Upgrade to latest
uv run alembic upgrade head

# Upgrade by specific revision
uv run alembic upgrade <revision>

# Downgrade
uv run alembic downgrade -1  # Down one revision
uv run alembic downgrade <revision>
```

### Migration History
```bash
# Show current version
uv run alembic current

# Show history
uv run alembic history

# Show pending migrations
uv run alembic heads
```

## Common Database Operations

### Create Record
```python
from app.models import Task
from app.database import get_session

async def create_task(task_data: dict, user_id: str):
    with Session(engine) as session:
        task = Task(
            user_id=user_id,
            title=task_data["title"],
            description=task_data.get("description"),
            completed=False
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task
```

### Read Records
```python
async def get_tasks(user_id: str, completed: Optional[bool] = None):
    with Session(engine) as session:
        query = session.query(Task).filter(Task.user_id == user_id)

        if completed is not None:
            query = query.filter(Task.completed == completed)

        tasks = query.order_by(Task.created_at.desc()).all()
        return tasks
```

### Update Record
```python
async def update_task(task_id: int, user_id: str, updates: dict):
    with Session(engine) as session:
        task = session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

        if not task:
            raise ValueError("Task not found")

        for key, value in updates.items():
            setattr(task, key, value)

        task.updated_at = datetime.now()
        session.commit()
        session.refresh(task)
        return task
```

### Delete Record
```python
async def delete_task(task_id: int, user_id: str):
    with Session(engine) as session:
        task = session.query(Task).filter(
            Task.id == task_id,
            Task.user_id == user_id
        ).first()

        if not task:
            raise ValueError("Task not found")

        session.delete(task)
        session.commit()
        return {"message": "Task deleted successfully"}
```

## Data Seeding

### Development Seed Data
```python
# scripts/seed.py
from app.database import engine
from app.models import Task, User
from sqlmodel import Session
import random

def seed_database():
    with Session(engine) as session:
        # Create test user (if not using Better Auth)
        user_id = "test-user-123"

        # Create sample tasks
        tasks = [
            Task(user_id=user_id, title="Buy groceries", description="Milk, bread, eggs", completed=False),
            Task(user_id=user_id, title="Finish project", description="Complete Phase II", completed=False),
            Task(user_id=user_id, title="Call dentist", description="Schedule appointment", completed=True),
            Task(user_id=user_id, title="Read book", description="Atomic Habits", completed=False),
            Task(user_id=user_id, title="Exercise", description="30 min cardio", completed=True),
        ]

        session.add_all(tasks)
        session.commit()
        print(f"Seeded {len(tasks)} tasks")

if __name__ == "__main__":
    seed_database()
```

Run: `uv run python scripts/seed.py`

## Query Optimization

### Add Indexes
```python
# In migration file
def upgrade():
    op.create_index('idx_tasks_user_id', 'tasks', ['user_id'])
    op.create_index('idx_tasks_completed', 'tasks', ['completed'])
    op.create_index('idx_tasks_due_date', 'tasks', ['due_date'])
```

### Use Query Explain
```python
from sqlalchemy import text

with Session(engine) as session:
    result = session.execute(
        text("EXPLAIN ANALYZE SELECT * FROM tasks WHERE user_id = :user_id"),
        {"user_id": "test-user"}
    )
    for row in result:
        print(row)
```

### Prevent N+1 Queries
```python
# Bad: N+1 query problem
tasks = session.query(Task).all()
for task in tasks:
    user = session.query(User).filter(User.id == task.user_id).first()  # N queries

# Good: Use join or eager loading
from sqlmodel import select
tasks = session.exec(
    select(Task).join(User).where(User.id == user_id)
).all()
```

## Data Integrity

### User Isolation
Always filter by `user_id`:
```python
# GOOD: User can only access their own tasks
tasks = session.query(Task).filter(
    Task.user_id == authenticated_user_id
).all()

# BAD: Exposes all users' tasks (security vulnerability)
tasks = session.query(Task).all()
```

### Foreign Key Constraints
```sql
-- Ensure cascading deletes
ALTER TABLE tasks
ADD CONSTRAINT fk_user
FOREIGN KEY (user_id)
REFERENCES users(id)
ON DELETE CASCADE;
```

### Data Validation
```python
from pydantic import BaseModel, Field

class TaskCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=1000)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, bread, eggs"
            }
        }
```

## Backup and Recovery

### Neon Database Backups
Neon provides automatic backups:
- Point-in-time recovery (PITR)
- Automated daily backups
- 7-day retention (free tier)

### Manual Backup
```bash
# Export database
pg_dump $DATABASE_URL > backup.sql

# Restore database
psql $DATABASE_URL < backup.sql
```

## Troubleshooting

### Connection Issues
```python
# Test connection
from sqlalchemy import text

try:
    with Session(engine) as session:
        session.exec(text("SELECT 1"))
        print("Database connection successful")
except Exception as e:
    print(f"Database connection failed: {e}")
```

### Migration Conflicts
```bash
# Check current state
uv run alembic current

# Resolve conflicts manually
# Edit migration file, then:
uv run alembic stamp head
```

### Query Performance
```bash
# Enable query logging
# In database.py: create_engine(..., echo=True)

# Analyze slow queries in Neon dashboard
```

## Success Criteria
- [ ] Database schema matches specification
- [ ] All migrations applied successfully
- [ ] Indexes created for frequently queried columns
- [ ] User data properly isolated
- [ ] Foreign key constraints enforced
- [ ] Connection pooling configured
- [ ] Seed data available for development
- [ ] Backup strategy in place
- [ ] Query performance optimized
- [ ] No N+1 query problems

## Related Agents
- `phase2-web.md` - Web app database integration
- `phase3-chatbot.md` - Conversation data persistence
- `deployment.md` - Database deployment
- `testing.md` - Database testing strategies

## Commands to Use
- `/sp.plan` - Design database schema
- `/sp.tasks` - Break down database tasks
- `/sp.implement` - Execute database changes
- `/sp.phr` - Document database decisions
- `/sp.adr` - Document schema architecture decisions

---

**Remember**: Database is the single source of truth. Design for stateless services, ensure user isolation, optimize queries, and always test migrations before production.
