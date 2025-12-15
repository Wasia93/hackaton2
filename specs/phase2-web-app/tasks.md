# Phase II: Full-Stack Web Application - Task Breakdown

**Project**: Evolution of Todo - Phase II
**Generated**: 2025-12-15
**Total Tasks**: 40 atomic work units

---

## Task Organization

Tasks are grouped into 4 phases:
1. **Phase A: Backend Foundation** (T-001 to T-015)
2. **Phase B: Frontend Foundation** (T-016 to T-025)
3. **Phase C: Feature Implementation** (T-026 to T-035)
4. **Phase D: Integration & Deployment** (T-036 to T-040)

---

## Phase A: Backend Foundation

### T-001: Initialize Backend Directory Structure
**Dependencies**: None
**Files**: `backend/`, `backend/app/`, `backend/app/models/`, `backend/app/services/`, `backend/app/api/`, `backend/app/core/`

**Acceptance Criteria**:
- [ ] Create `backend/` directory at project root
- [ ] Create subdirectories: `app/models/`, `app/services/`, `app/api/`, `app/core/`
- [ ] Create `__init__.py` in all Python package directories
- [ ] Directory structure matches plan.md

**Implementation**:
```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── __init__.py
│   ├── services/
│   │   └── __init__.py
│   ├── api/
│   │   └── __init__.py
│   └── core/
│       └── __init__.py
├── requirements.txt
└── .env.example
```

---

### T-002: Create Backend Dependencies File
**Dependencies**: T-001
**Files**: `backend/requirements.txt`

**Acceptance Criteria**:
- [ ] All required packages listed with version constraints
- [ ] File can be installed via `pip install -r requirements.txt`
- [ ] No missing dependencies for FastAPI + SQLModel + PostgreSQL

**Implementation**:
```txt
fastapi==0.115.0
uvicorn[standard]==0.31.0
sqlmodel==0.0.22
psycopg2-binary==2.9.9
alembic==1.13.2
pydantic==2.9.2
pydantic-settings==2.5.2
python-jose[cryptography]==3.3.0
python-multipart==0.0.9
passlib[bcrypt]==1.7.4
```

---

### T-003: Create Backend Environment Configuration
**Dependencies**: T-001
**Files**: `backend/.env.example`, `backend/app/core/config.py`

**Acceptance Criteria**:
- [ ] `.env.example` contains all required environment variables
- [ ] `config.py` uses Pydantic Settings for type-safe config
- [ ] Database URL, JWT secret, and CORS origins configurable

**Implementation** (`backend/app/core/config.py`):
```python
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Todo API"
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    CORS_ORIGINS: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"

settings = Settings()
```

---

### T-004: Initialize Database Connection
**Dependencies**: T-002, T-003
**Files**: `backend/app/core/database.py`

**Acceptance Criteria**:
- [ ] SQLModel engine configured with Neon PostgreSQL URL
- [ ] Session factory created
- [ ] Connection tested successfully
- [ ] Supports dependency injection pattern

**Implementation**:
```python
from sqlmodel import create_engine, Session, SQLModel
from backend.app.core.config import settings

engine = create_engine(settings.DATABASE_URL, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

---

### T-005: Create User SQLModel
**Dependencies**: T-004
**Files**: `backend/app/models/user.py`

**Acceptance Criteria**:
- [ ] User model with all fields from plan.md schema
- [ ] Password hashing not stored in model (handled separately)
- [ ] Timestamps use datetime.utcnow
- [ ] Model validates email format

**Implementation**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    __tablename__ = "users"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### T-006: Create Better Auth User Model
**Dependencies**: T-005
**Files**: `backend/app/models/better_auth_user.py`

**Acceptance Criteria**:
- [ ] BetterAuthUser model mirrors Better Auth schema
- [ ] Contains hashed_password field
- [ ] Separate from User model for auth isolation
- [ ] Links to User via email

**Implementation**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class BetterAuthUser(SQLModel, table=True):
    __tablename__ = "better_auth_users"

    id: str = Field(primary_key=True)  # UUID from Better Auth
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(max_length=200)
    hashed_password: str
    email_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### T-007: Create Task SQLModel
**Dependencies**: T-005
**Files**: `backend/app/models/task.py`

**Acceptance Criteria**:
- [ ] Task model with all fields from plan.md schema
- [ ] user_id field links to Better Auth user ID (string UUID)
- [ ] Indexes on user_id and completed fields
- [ ] Timestamps auto-update

**Implementation**:
```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Task(SQLModel, table=True):
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, max_length=255)  # Better Auth UUID
    title: str = Field(max_length=200)
    description: str = Field(default="")
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### T-008: Create Alembic Migration Configuration
**Dependencies**: T-005, T-006, T-007
**Files**: `backend/alembic.ini`, `backend/alembic/env.py`

**Acceptance Criteria**:
- [ ] Alembic initialized in backend directory
- [ ] `alembic.ini` configured with correct database URL
- [ ] `env.py` imports all SQLModel models
- [ ] Can generate migrations successfully

**Implementation**:
```bash
cd backend
alembic init alembic
```

Update `alembic/env.py`:
```python
from backend.app.core.database import engine
from backend.app.models.user import User
from backend.app.models.better_auth_user import BetterAuthUser
from backend.app.models.task import Task
from sqlmodel import SQLModel

target_metadata = SQLModel.metadata
```

---

### T-009: Create Initial Database Migration
**Dependencies**: T-008
**Files**: `backend/alembic/versions/001_initial_schema.py`

**Acceptance Criteria**:
- [ ] Migration creates users, better_auth_users, and tasks tables
- [ ] All indexes and constraints created
- [ ] Migration runs successfully on Neon PostgreSQL
- [ ] Rollback works correctly

**Implementation**:
```bash
cd backend
alembic revision --autogenerate -m "Initial schema"
alembic upgrade head
```

---

### T-010: Create JWT Authentication Utilities
**Dependencies**: T-003
**Files**: `backend/app/core/security.py`

**Acceptance Criteria**:
- [ ] Function to create JWT access tokens
- [ ] Function to verify and decode JWT tokens
- [ ] Password hashing utilities (bcrypt)
- [ ] Token expiration handling

**Implementation**:
```python
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from backend.app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM)

def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

---

### T-011: Create Authentication Middleware
**Dependencies**: T-010
**Files**: `backend/app/core/auth.py`

**Acceptance Criteria**:
- [ ] Middleware extracts JWT from Authorization header
- [ ] Verifies token and extracts user_id
- [ ] Returns 401 for invalid/missing tokens
- [ ] Injects user_id into request context

**Implementation**:
```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from backend.app.core.security import verify_token

security = HTTPBearer()

async def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    token = credentials.credentials
    payload = verify_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )
    return user_id
```

---

### T-012: Create Task Service Layer
**Dependencies**: T-007, T-011
**Files**: `backend/app/services/task_service.py`

**Acceptance Criteria**:
- [ ] All CRUD operations implemented
- [ ] All queries filter by user_id (data isolation)
- [ ] Validation for title length and required fields
- [ ] Returns typed Task models

**Implementation**:
```python
from sqlmodel import Session, select
from backend.app.models.task import Task
from typing import Optional

class TaskService:
    def __init__(self, session: Session, user_id: str):
        self.session = session
        self.user_id = user_id

    def create_task(self, title: str, description: str = "") -> Task:
        if not title or len(title) > 200:
            raise ValueError("Title required and must be <= 200 chars")

        task = Task(
            user_id=self.user_id,
            title=title.strip(),
            description=description.strip()
        )
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        statement = select(Task).where(Task.user_id == self.user_id)
        return self.session.exec(statement).all()

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == self.user_id
        )
        return self.session.exec(statement).first()

    def update_task(self, task_id: int, title: Optional[str], description: Optional[str]) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        if title is not None:
            if len(title) > 200:
                raise ValueError("Title must be <= 200 chars")
            task.title = title.strip()

        if description is not None:
            task.description = description.strip()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task

    def delete_task(self, task_id: int) -> bool:
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()
        return True

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.completed = not task.completed
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)
        return task
```

---

### T-013: Create Task API Endpoints
**Dependencies**: T-012
**Files**: `backend/app/api/tasks.py`

**Acceptance Criteria**:
- [ ] All 6 endpoints from plan.md implemented
- [ ] All endpoints use authentication middleware
- [ ] Request/response models use Pydantic
- [ ] Proper HTTP status codes returned

**Implementation**:
```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.app.core.database import get_session
from backend.app.core.auth import get_current_user_id
from backend.app.services.task_service import TaskService
from backend.app.models.task import Task
from pydantic import BaseModel

router = APIRouter(prefix="/tasks", tags=["tasks"])

class CreateTaskRequest(BaseModel):
    title: str
    description: str = ""

class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None

@router.post("/", response_model=Task, status_code=status.HTTP_201_CREATED)
async def create_task(
    request: CreateTaskRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    return service.create_task(request.title, request.description)

@router.get("/", response_model=list[Task])
async def get_all_tasks(
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    return service.get_all_tasks()

@router.get("/{task_id}", response_model=Task)
async def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    task = service.get_task_by_id(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=Task)
async def update_task(
    task_id: int,
    request: UpdateTaskRequest,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    task = service.update_task(task_id, request.title, request.description)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    if not service.delete_task(task_id):
        raise HTTPException(status_code=404, detail="Task not found")

@router.patch("/{task_id}/toggle", response_model=Task)
async def toggle_task_completion(
    task_id: int,
    session: Session = Depends(get_session),
    user_id: str = Depends(get_current_user_id)
):
    service = TaskService(session, user_id)
    task = service.toggle_completion(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task
```

---

### T-014: Create FastAPI Application Entry Point
**Dependencies**: T-013
**Files**: `backend/app/main.py`

**Acceptance Criteria**:
- [ ] FastAPI app instance created
- [ ] CORS middleware configured
- [ ] Task router included
- [ ] Health check endpoint exists
- [ ] Can run with `uvicorn app.main:app`

**Implementation**:
```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.tasks import router as tasks_router

app = FastAPI(title=settings.PROJECT_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tasks_router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
```

---

### T-015: Test Backend API Endpoints
**Dependencies**: T-014
**Files**: `backend/tests/test_tasks.py`

**Acceptance Criteria**:
- [ ] All 6 task endpoints tested
- [ ] Tests verify authentication required
- [ ] Tests verify user data isolation
- [ ] All tests pass

**Implementation**:
```python
from fastapi.testclient import TestClient
from backend.app.main import app
from backend.app.core.security import create_access_token

client = TestClient(app)

def test_create_task_requires_auth():
    response = client.post("/tasks/", json={"title": "Test"})
    assert response.status_code == 401

def test_create_task_success():
    token = create_access_token({"sub": "user123"})
    response = client.post(
        "/tasks/",
        json={"title": "Test Task", "description": "Test"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert response.json()["title"] == "Test Task"
```

---

## Phase B: Frontend Foundation

### T-016: Initialize Next.js Project
**Dependencies**: None
**Files**: `frontend/`, `frontend/package.json`, `frontend/next.config.js`

**Acceptance Criteria**:
- [ ] Next.js 16+ with App Router
- [ ] TypeScript configured
- [ ] Tailwind CSS installed
- [ ] Project runs with `npm run dev`

**Implementation**:
```bash
npx create-next-app@latest frontend --typescript --tailwind --app --no-src-dir
cd frontend
npm install
```

---

### T-017: Install Better Auth
**Dependencies**: T-016
**Files**: `frontend/package.json`

**Acceptance Criteria**:
- [ ] Better Auth package installed
- [ ] Required peer dependencies installed
- [ ] Package.json updated correctly

**Implementation**:
```bash
cd frontend
npm install better-auth
```

---

### T-018: Configure Better Auth
**Dependencies**: T-017
**Files**: `frontend/lib/auth.ts`

**Acceptance Criteria**:
- [ ] Better Auth configured with JWT secret
- [ ] Session storage configured
- [ ] Auth endpoints defined
- [ ] Client instance exported

**Implementation**:
```typescript
import { BetterAuth } from "better-auth"

export const auth = new BetterAuth({
  secret: process.env.NEXT_PUBLIC_JWT_SECRET!,
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
  session: {
    cookieName: "todo-session",
    expiresIn: 60 * 60 * 24 * 7, // 7 days
  },
})
```

---

### T-019: Create API Client Utility
**Dependencies**: T-018
**Files**: `frontend/lib/api.ts`

**Acceptance Criteria**:
- [ ] Axios or fetch wrapper configured
- [ ] Automatically includes JWT token from Better Auth
- [ ] Base URL configurable via environment variable
- [ ] Error handling for 401 responses

**Implementation**:
```typescript
import { auth } from "./auth"

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000"

async function getAuthToken(): Promise<string | null> {
  const session = await auth.getSession()
  return session?.accessToken || null
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = await getAuthToken()

  const headers: HeadersInit = {
    "Content-Type": "application/json",
    ...options.headers,
  }

  if (token) {
    headers["Authorization"] = `Bearer ${token}`
  }

  const response = await fetch(`${API_URL}${endpoint}`, {
    ...options,
    headers,
  })

  if (!response.ok) {
    if (response.status === 401) {
      // Redirect to login
      window.location.href = "/login"
    }
    throw new Error(`API error: ${response.statusText}`)
  }

  return response.json()
}
```

---

### T-020: Create Task Type Definitions
**Dependencies**: None
**Files**: `frontend/types/task.ts`

**Acceptance Criteria**:
- [ ] Task interface matches backend model
- [ ] All fields typed correctly
- [ ] Exported for use across app

**Implementation**:
```typescript
export interface Task {
  id: number
  user_id: string
  title: string
  description: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface CreateTaskRequest {
  title: string
  description?: string
}

export interface UpdateTaskRequest {
  title?: string
  description?: string
}
```

---

### T-021: Create Login Page
**Dependencies**: T-018
**Files**: `frontend/app/login/page.tsx`

**Acceptance Criteria**:
- [ ] Form with email and password fields
- [ ] Calls Better Auth login function
- [ ] Redirects to dashboard on success
- [ ] Shows error messages on failure
- [ ] Link to registration page

**Implementation**:
```typescript
"use client"

import { useState } from "react"
import { auth } from "@/lib/auth"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function LoginPage() {
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    try {
      await auth.signIn({ email, password })
      router.push("/dashboard")
    } catch (err) {
      setError("Invalid email or password")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Login</h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2">Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Login
          </button>
        </form>

        <p className="mt-4 text-center">
          Don't have an account?{" "}
          <Link href="/register" className="text-blue-500">
            Register
          </Link>
        </p>
      </div>
    </div>
  )
}
```

---

### T-022: Create Registration Page
**Dependencies**: T-018
**Files**: `frontend/app/register/page.tsx`

**Acceptance Criteria**:
- [ ] Form with name, email, password fields
- [ ] Calls Better Auth registration function
- [ ] Redirects to dashboard on success
- [ ] Shows validation errors
- [ ] Link to login page

**Implementation**:
```typescript
"use client"

import { useState } from "react"
import { auth } from "@/lib/auth"
import { useRouter } from "next/navigation"
import Link from "next/link"

export default function RegisterPage() {
  const [name, setName] = useState("")
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")
  const [error, setError] = useState("")
  const router = useRouter()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (password.length < 8) {
      setError("Password must be at least 8 characters")
      return
    }

    try {
      await auth.signUp({ name, email, password })
      router.push("/dashboard")
    } catch (err) {
      setError("Registration failed. Email may already exist.")
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center">
      <div className="max-w-md w-full p-6 bg-white rounded-lg shadow">
        <h1 className="text-2xl font-bold mb-6">Register</h1>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2">Name</label>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2">Email</label>
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full border p-2 rounded"
              required
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2">Password</label>
            <input
              type="password"
              value={password"
              onChange={(e) => setPassword(e.target.value)}
              className="w-full border p-2 rounded"
              required
              minLength={8}
            />
          </div>

          <button
            type="submit"
            className="w-full bg-blue-500 text-white p-2 rounded hover:bg-blue-600"
          >
            Register
          </button>
        </form>

        <p className="mt-4 text-center">
          Already have an account?{" "}
          <Link href="/login" className="text-blue-500">
            Login
          </Link>
        </p>
      </div>
    </div>
  )
}
```

---

### T-023: Create Protected Route Wrapper
**Dependencies**: T-018
**Files**: `frontend/components/ProtectedRoute.tsx`

**Acceptance Criteria**:
- [ ] Checks if user is authenticated
- [ ] Redirects to login if not authenticated
- [ ] Shows loading state during check
- [ ] Wraps dashboard and other protected pages

**Implementation**:
```typescript
"use client"

import { useEffect, useState } from "react"
import { auth } from "@/lib/auth"
import { useRouter } from "next/navigation"

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode
}) {
  const [isAuthenticated, setIsAuthenticated] = useState(false)
  const [isLoading, setIsLoading] = useState(true)
  const router = useRouter()

  useEffect(() => {
    const checkAuth = async () => {
      const session = await auth.getSession()
      if (!session) {
        router.push("/login")
      } else {
        setIsAuthenticated(true)
      }
      setIsLoading(false)
    }

    checkAuth()
  }, [router])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div>Loading...</div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return null
  }

  return <>{children}</>
}
```

---

### T-024: Create Dashboard Layout
**Dependencies**: T-023
**Files**: `frontend/app/dashboard/layout.tsx`

**Acceptance Criteria**:
- [ ] Wraps all dashboard pages
- [ ] Uses ProtectedRoute wrapper
- [ ] Shows navigation header with logout button
- [ ] Responsive design

**Implementation**:
```typescript
import ProtectedRoute from "@/components/ProtectedRoute"
import { auth } from "@/lib/auth"

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const handleLogout = async () => {
    await auth.signOut()
    window.location.href = "/login"
  }

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-gray-100">
        <nav className="bg-white shadow p-4">
          <div className="max-w-7xl mx-auto flex justify-between items-center">
            <h1 className="text-xl font-bold">Todo App</h1>
            <button
              onClick={handleLogout}
              className="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600"
            >
              Logout
            </button>
          </div>
        </nav>

        <main className="max-w-7xl mx-auto p-6">
          {children}
        </main>
      </div>
    </ProtectedRoute>
  )
}
```

---

### T-025: Create Environment Variables File
**Dependencies**: T-016, T-018, T-019
**Files**: `frontend/.env.local.example`

**Acceptance Criteria**:
- [ ] All required environment variables documented
- [ ] Example values provided
- [ ] Instructions for setup included

**Implementation**:
```env
# API Backend URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth JWT Secret (must match backend)
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key-change-this

# Database URL (for Better Auth server-side)
DATABASE_URL=postgresql://user:pass@host/database
```

---

## Phase C: Feature Implementation

### T-026: Create Task List Component
**Dependencies**: T-020, T-024
**Files**: `frontend/components/TaskList.tsx`

**Acceptance Criteria**:
- [ ] Displays all tasks in a list
- [ ] Shows task title, description, completion status
- [ ] Handles empty state
- [ ] Responsive design

**Implementation**:
```typescript
import { Task } from "@/types/task"

interface TaskListProps {
  tasks: Task[]
  onToggle: (id: number) => void
  onEdit: (task: Task) => void
  onDelete: (id: number) => void
}

export default function TaskList({
  tasks,
  onToggle,
  onEdit,
  onDelete,
}: TaskListProps) {
  if (tasks.length === 0) {
    return (
      <div className="text-center text-gray-500 py-8">
        No tasks yet. Create your first task!
      </div>
    )
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <div
          key={task.id}
          className="bg-white p-4 rounded-lg shadow flex items-start gap-4"
        >
          <input
            type="checkbox"
            checked={task.completed}
            onChange={() => onToggle(task.id)}
            className="mt-1"
          />

          <div className="flex-1">
            <h3
              className={`font-semibold ${
                task.completed ? "line-through text-gray-500" : ""
              }`}
            >
              {task.title}
            </h3>
            {task.description && (
              <p className="text-gray-600 text-sm mt-1">
                {task.description}
              </p>
            )}
            <p className="text-xs text-gray-400 mt-2">
              {new Date(task.created_at).toLocaleDateString()}
            </p>
          </div>

          <div className="flex gap-2">
            <button
              onClick={() => onEdit(task)}
              className="text-blue-500 hover:text-blue-700"
            >
              Edit
            </button>
            <button
              onClick={() => onDelete(task.id)}
              className="text-red-500 hover:text-red-700"
            >
              Delete
            </button>
          </div>
        </div>
      ))}
    </div>
  )
}
```

---

### T-027: Create Add Task Form Component
**Dependencies**: T-020
**Files**: `frontend/components/AddTaskForm.tsx`

**Acceptance Criteria**:
- [ ] Form with title and description inputs
- [ ] Validates title is not empty
- [ ] Calls onCreate callback with form data
- [ ] Clears form after submission
- [ ] Shows validation errors

**Implementation**:
```typescript
"use client"

import { useState } from "react"
import { CreateTaskRequest } from "@/types/task"

interface AddTaskFormProps {
  onCreate: (data: CreateTaskRequest) => Promise<void>
}

export default function AddTaskForm({ onCreate }: AddTaskFormProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!title.trim()) {
      setError("Title is required")
      return
    }

    if (title.length > 200) {
      setError("Title must be 200 characters or less")
      return
    }

    setIsSubmitting(true)

    try {
      await onCreate({ title: title.trim(), description: description.trim() })
      setTitle("")
      setDescription("")
    } catch (err) {
      setError("Failed to create task")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <form onSubmit={handleSubmit} className="bg-white p-6 rounded-lg shadow mb-6">
      <h2 className="text-xl font-bold mb-4">Add New Task</h2>

      {error && (
        <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
          {error}
        </div>
      )}

      <div className="mb-4">
        <label className="block mb-2 font-semibold">Title *</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border p-2 rounded"
          placeholder="Enter task title..."
          maxLength={200}
          disabled={isSubmitting}
        />
      </div>

      <div className="mb-4">
        <label className="block mb-2 font-semibold">Description</label>
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          className="w-full border p-2 rounded"
          rows={3}
          placeholder="Enter task description (optional)..."
          disabled={isSubmitting}
        />
      </div>

      <button
        type="submit"
        disabled={isSubmitting}
        className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
      >
        {isSubmitting ? "Adding..." : "Add Task"}
      </button>
    </form>
  )
}
```

---

### T-028: Create Edit Task Modal Component
**Dependencies**: T-020
**Files**: `frontend/components/EditTaskModal.tsx`

**Acceptance Criteria**:
- [ ] Modal dialog with title and description inputs
- [ ] Pre-fills with current task data
- [ ] Validates inputs
- [ ] Calls onUpdate callback
- [ ] Closes on cancel or successful update

**Implementation**:
```typescript
"use client"

import { useState, useEffect } from "react"
import { Task, UpdateTaskRequest } from "@/types/task"

interface EditTaskModalProps {
  task: Task | null
  onUpdate: (id: number, data: UpdateTaskRequest) => Promise<void>
  onClose: () => void
}

export default function EditTaskModal({
  task,
  onUpdate,
  onClose,
}: EditTaskModalProps) {
  const [title, setTitle] = useState("")
  const [description, setDescription] = useState("")
  const [error, setError] = useState("")
  const [isSubmitting, setIsSubmitting] = useState(false)

  useEffect(() => {
    if (task) {
      setTitle(task.title)
      setDescription(task.description)
    }
  }, [task])

  if (!task) return null

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError("")

    if (!title.trim()) {
      setError("Title is required")
      return
    }

    if (title.length > 200) {
      setError("Title must be 200 characters or less")
      return
    }

    setIsSubmitting(true)

    try {
      await onUpdate(task.id, {
        title: title.trim(),
        description: description.trim(),
      })
      onClose()
    } catch (err) {
      setError("Failed to update task")
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
      <div className="bg-white p-6 rounded-lg shadow-lg max-w-md w-full">
        <h2 className="text-xl font-bold mb-4">Edit Task</h2>

        {error && (
          <div className="bg-red-100 text-red-700 p-3 rounded mb-4">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="mb-4">
            <label className="block mb-2 font-semibold">Title *</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              className="w-full border p-2 rounded"
              maxLength={200}
              disabled={isSubmitting}
            />
          </div>

          <div className="mb-4">
            <label className="block mb-2 font-semibold">Description</label>
            <textarea
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              className="w-full border p-2 rounded"
              rows={3}
              disabled={isSubmitting}
            />
          </div>

          <div className="flex gap-4">
            <button
              type="submit"
              disabled={isSubmitting}
              className="flex-1 bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-gray-400"
            >
              {isSubmitting ? "Saving..." : "Save Changes"}
            </button>
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              className="flex-1 bg-gray-300 px-4 py-2 rounded hover:bg-gray-400"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}
```

---

### T-029: Create Task API Service
**Dependencies**: T-019, T-020
**Files**: `frontend/services/taskService.ts`

**Acceptance Criteria**:
- [ ] All 6 API operations implemented
- [ ] Uses apiRequest utility
- [ ] Returns typed Task models
- [ ] Handles errors appropriately

**Implementation**:
```typescript
import { apiRequest } from "@/lib/api"
import { Task, CreateTaskRequest, UpdateTaskRequest } from "@/types/task"

export const taskService = {
  async getAllTasks(): Promise<Task[]> {
    return apiRequest<Task[]>("/tasks/")
  },

  async getTaskById(id: number): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}`)
  },

  async createTask(data: CreateTaskRequest): Promise<Task> {
    return apiRequest<Task>("/tasks/", {
      method: "POST",
      body: JSON.stringify(data),
    })
  },

  async updateTask(id: number, data: UpdateTaskRequest): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}`, {
      method: "PUT",
      body: JSON.stringify(data),
    })
  },

  async deleteTask(id: number): Promise<void> {
    return apiRequest<void>(`/tasks/${id}`, {
      method: "DELETE",
    })
  },

  async toggleCompletion(id: number): Promise<Task> {
    return apiRequest<Task>(`/tasks/${id}/toggle`, {
      method: "PATCH",
    })
  },
}
```

---

### T-030: Create Dashboard Page
**Dependencies**: T-024, T-026, T-027, T-028, T-029
**Files**: `frontend/app/dashboard/page.tsx`

**Acceptance Criteria**:
- [ ] Fetches all tasks on mount
- [ ] Displays AddTaskForm
- [ ] Displays TaskList
- [ ] Shows EditTaskModal when editing
- [ ] All CRUD operations work
- [ ] Shows loading and error states

**Implementation**:
```typescript
"use client"

import { useState, useEffect } from "react"
import { Task } from "@/types/task"
import { taskService } from "@/services/taskService"
import AddTaskForm from "@/components/AddTaskForm"
import TaskList from "@/components/TaskList"
import EditTaskModal from "@/components/EditTaskModal"

export default function DashboardPage() {
  const [tasks, setTasks] = useState<Task[]>([])
  const [editingTask, setEditingTask] = useState<Task | null>(null)
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState("")

  const fetchTasks = async () => {
    try {
      const data = await taskService.getAllTasks()
      setTasks(data)
    } catch (err) {
      setError("Failed to load tasks")
    } finally {
      setIsLoading(false)
    }
  }

  useEffect(() => {
    fetchTasks()
  }, [])

  const handleCreate = async (data: CreateTaskRequest) => {
    const newTask = await taskService.createTask(data)
    setTasks([...tasks, newTask])
  }

  const handleToggle = async (id: number) => {
    const updatedTask = await taskService.toggleCompletion(id)
    setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
  }

  const handleUpdate = async (id: number, data: UpdateTaskRequest) => {
    const updatedTask = await taskService.updateTask(id, data)
    setTasks(tasks.map((t) => (t.id === id ? updatedTask : t)))
  }

  const handleDelete = async (id: number) => {
    if (!confirm("Are you sure you want to delete this task?")) return
    await taskService.deleteTask(id)
    setTasks(tasks.filter((t) => t.id !== id))
  }

  if (isLoading) {
    return <div className="text-center py-8">Loading tasks...</div>
  }

  if (error) {
    return (
      <div className="bg-red-100 text-red-700 p-4 rounded">
        {error}
      </div>
    )
  }

  return (
    <div>
      <AddTaskForm onCreate={handleCreate} />

      <TaskList
        tasks={tasks}
        onToggle={handleToggle}
        onEdit={setEditingTask}
        onDelete={handleDelete}
      />

      <EditTaskModal
        task={editingTask}
        onUpdate={handleUpdate}
        onClose={() => setEditingTask(null)}
      />
    </div>
  )
}
```

---

### T-031: Create Home Page with CTA
**Dependencies**: T-016
**Files**: `frontend/app/page.tsx`

**Acceptance Criteria**:
- [ ] Landing page with app description
- [ ] Buttons to Login and Register
- [ ] Responsive design
- [ ] Professional appearance

**Implementation**:
```typescript
import Link from "next/link"

export default function HomePage() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-500 to-purple-600">
      <div className="text-center text-white p-8">
        <h1 className="text-5xl font-bold mb-4">Todo App</h1>
        <p className="text-xl mb-8">
          Your tasks, organized. Simple and powerful task management.
        </p>

        <div className="flex gap-4 justify-center">
          <Link
            href="/login"
            className="bg-white text-blue-600 px-8 py-3 rounded-lg font-semibold hover:bg-gray-100"
          >
            Login
          </Link>
          <Link
            href="/register"
            className="bg-transparent border-2 border-white px-8 py-3 rounded-lg font-semibold hover:bg-white hover:text-blue-600"
          >
            Register
          </Link>
        </div>
      </div>
    </div>
  )
}
```

---

### T-032: Add Filter/Sort Functionality to Dashboard
**Dependencies**: T-030
**Files**: `frontend/app/dashboard/page.tsx` (update)

**Acceptance Criteria**:
- [ ] Filter by completion status (All/Complete/Incomplete)
- [ ] Sort by creation date or title
- [ ] UI controls for filters
- [ ] Filters persist during CRUD operations

**Implementation** (additions to T-030):
```typescript
const [filter, setFilter] = useState<"all" | "completed" | "incomplete">("all")
const [sortBy, setSortBy] = useState<"date" | "title">("date")

const filteredAndSortedTasks = tasks
  .filter((task) => {
    if (filter === "completed") return task.completed
    if (filter === "incomplete") return !task.completed
    return true
  })
  .sort((a, b) => {
    if (sortBy === "title") {
      return a.title.localeCompare(b.title)
    }
    return new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
  })

// Add UI controls before TaskList:
<div className="bg-white p-4 rounded-lg shadow mb-6 flex gap-4">
  <select
    value={filter}
    onChange={(e) => setFilter(e.target.value as any)}
    className="border p-2 rounded"
  >
    <option value="all">All Tasks</option>
    <option value="completed">Completed</option>
    <option value="incomplete">Incomplete</option>
  </select>

  <select
    value={sortBy}
    onChange={(e) => setSortBy(e.target.value as any)}
    className="border p-2 rounded"
  >
    <option value="date">Sort by Date</option>
    <option value="title">Sort by Title</option>
  </select>
</div>

// Pass filteredAndSortedTasks to TaskList instead of tasks
```

---

### T-033: Add Task Statistics Component
**Dependencies**: T-030
**Files**: `frontend/components/TaskStats.tsx`

**Acceptance Criteria**:
- [ ] Shows total tasks count
- [ ] Shows completed tasks count
- [ ] Shows completion percentage
- [ ] Updates in real-time as tasks change

**Implementation**:
```typescript
import { Task } from "@/types/task"

interface TaskStatsProps {
  tasks: Task[]
}

export default function TaskStats({ tasks }: TaskStatsProps) {
  const total = tasks.length
  const completed = tasks.filter((t) => t.completed).length
  const percentage = total > 0 ? Math.round((completed / total) * 100) : 0

  return (
    <div className="bg-white p-6 rounded-lg shadow mb-6">
      <h2 className="text-xl font-bold mb-4">Statistics</h2>

      <div className="grid grid-cols-3 gap-4">
        <div className="text-center">
          <div className="text-3xl font-bold text-blue-600">{total}</div>
          <div className="text-sm text-gray-600">Total Tasks</div>
        </div>

        <div className="text-center">
          <div className="text-3xl font-bold text-green-600">{completed}</div>
          <div className="text-sm text-gray-600">Completed</div>
        </div>

        <div className="text-center">
          <div className="text-3xl font-bold text-purple-600">{percentage}%</div>
          <div className="text-sm text-gray-600">Progress</div>
        </div>
      </div>
    </div>
  )
}
```

---

### T-034: Add Loading Skeletons
**Dependencies**: T-030
**Files**: `frontend/components/TaskListSkeleton.tsx`

**Acceptance Criteria**:
- [ ] Skeleton UI for task list
- [ ] Shows while tasks are loading
- [ ] Matches actual task card layout
- [ ] Smooth animation

**Implementation**:
```typescript
export default function TaskListSkeleton() {
  return (
    <div className="space-y-4">
      {[1, 2, 3].map((i) => (
        <div
          key={i}
          className="bg-white p-4 rounded-lg shadow animate-pulse"
        >
          <div className="flex items-start gap-4">
            <div className="w-4 h-4 bg-gray-300 rounded mt-1"></div>

            <div className="flex-1">
              <div className="h-6 bg-gray-300 rounded w-3/4 mb-2"></div>
              <div className="h-4 bg-gray-200 rounded w-full mb-2"></div>
              <div className="h-3 bg-gray-200 rounded w-1/4"></div>
            </div>

            <div className="flex gap-2">
              <div className="h-8 w-12 bg-gray-300 rounded"></div>
              <div className="h-8 w-12 bg-gray-300 rounded"></div>
            </div>
          </div>
        </div>
      ))}
    </div>
  )
}
```

---

### T-035: Add Error Boundary
**Dependencies**: T-016
**Files**: `frontend/components/ErrorBoundary.tsx`

**Acceptance Criteria**:
- [ ] Catches React errors
- [ ] Shows user-friendly error message
- [ ] Provides reload button
- [ ] Logs errors to console

**Implementation**:
```typescript
"use client"

import { Component, ReactNode } from "react"

interface Props {
  children: ReactNode
}

interface State {
  hasError: boolean
  error?: Error
}

export default class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = { hasError: false }
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, errorInfo: any) {
    console.error("Error caught by boundary:", error, errorInfo)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="min-h-screen flex items-center justify-center bg-gray-100">
          <div className="max-w-md p-6 bg-white rounded-lg shadow text-center">
            <h1 className="text-2xl font-bold text-red-600 mb-4">
              Oops! Something went wrong
            </h1>
            <p className="text-gray-600 mb-4">
              We're sorry for the inconvenience. Please try reloading the page.
            </p>
            <button
              onClick={() => window.location.reload()}
              className="bg-blue-500 text-white px-6 py-2 rounded hover:bg-blue-600"
            >
              Reload Page
            </button>
          </div>
        </div>
      )
    }

    return this.props.children
  }
}
```

---

## Phase D: Integration & Deployment

### T-036: Test Authentication Flow
**Dependencies**: T-021, T-022, T-023
**Files**: `frontend/__tests__/auth.test.ts`

**Acceptance Criteria**:
- [ ] Test registration creates user and logs in
- [ ] Test login with valid credentials succeeds
- [ ] Test login with invalid credentials fails
- [ ] Test logout clears session
- [ ] Test protected route redirects when not authenticated

---

### T-037: Test CRUD Operations End-to-End
**Dependencies**: T-030
**Files**: `frontend/__tests__/tasks.test.ts`

**Acceptance Criteria**:
- [ ] Test creating task and seeing it in list
- [ ] Test updating task reflects changes
- [ ] Test deleting task removes from list
- [ ] Test toggling completion updates status
- [ ] Test filters and sorting work correctly

---

### T-038: Test Multi-User Data Isolation
**Dependencies**: T-037
**Files**: `backend/tests/test_isolation.py`

**Acceptance Criteria**:
- [ ] Create tasks for User A
- [ ] Create tasks for User B
- [ ] Verify User A cannot see User B's tasks
- [ ] Verify User A cannot modify User B's tasks
- [ ] Verify database correctly filters by user_id

**Implementation**:
```python
def test_data_isolation():
    # Create User A tasks
    token_a = create_access_token({"sub": "user_a"})
    response = client.post(
        "/tasks/",
        json={"title": "User A Task"},
        headers={"Authorization": f"Bearer {token_a}"}
    )
    assert response.status_code == 201

    # Create User B tasks
    token_b = create_access_token({"sub": "user_b"})
    response = client.post(
        "/tasks/",
        json={"title": "User B Task"},
        headers={"Authorization": f"Bearer {token_b}"}
    )
    assert response.status_code == 201

    # User A should only see their tasks
    response = client.get(
        "/tasks/",
        headers={"Authorization": f"Bearer {token_a}"}
    )
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "User A Task"
```

---

### T-039: Deploy Backend to Railway/Render
**Dependencies**: T-015
**Files**: `backend/Procfile`, `backend/runtime.txt`

**Acceptance Criteria**:
- [ ] Backend deployed and accessible
- [ ] Database migrations run successfully
- [ ] Environment variables configured
- [ ] Health check endpoint responds

**Implementation** (`backend/Procfile`):
```
web: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

**Implementation** (`backend/runtime.txt`):
```
python-3.13
```

---

### T-040: Deploy Frontend to Vercel
**Dependencies**: T-031, T-039
**Files**: `vercel.json`

**Acceptance Criteria**:
- [ ] Frontend deployed to Vercel
- [ ] Environment variables configured (API URL, JWT secret)
- [ ] Custom domain configured (optional)
- [ ] All pages accessible and working
- [ ] Backend API calls succeed

**Implementation** (`vercel.json`):
```json
{
  "buildCommand": "cd frontend && npm run build",
  "outputDirectory": "frontend/.next",
  "framework": "nextjs",
  "env": {
    "NEXT_PUBLIC_API_URL": "@api-url",
    "NEXT_PUBLIC_JWT_SECRET": "@jwt-secret"
  }
}
```

---

## Task Summary

**Total Tasks**: 40
- **Backend**: 15 tasks (T-001 to T-015)
- **Frontend**: 10 tasks (T-016 to T-025)
- **Features**: 10 tasks (T-026 to T-035)
- **Testing & Deployment**: 5 tasks (T-036 to T-040)

**Estimated Implementation Order**:
1. Complete all Phase A tasks sequentially (backend foundation)
2. Complete all Phase B tasks sequentially (frontend foundation)
3. Complete Phase C tasks (can parallelize components)
4. Complete Phase D tasks (integration testing then deployment)

---

## Dependencies Graph

```
T-001 (Backend Dir) → T-002 (Dependencies) → T-003 (Config)
                                           → T-004 (Database)
T-004 → T-005 (User Model)
     → T-006 (Auth User Model)
     → T-007 (Task Model)

T-005,T-006,T-007 → T-008 (Alembic) → T-009 (Migration)

T-003 → T-010 (JWT Utils) → T-011 (Auth Middleware)

T-007,T-011 → T-012 (Task Service) → T-013 (API Endpoints)
T-013 → T-014 (FastAPI App) → T-015 (Backend Tests)

T-016 (Next.js) → T-017 (Better Auth) → T-018 (Auth Config)
T-018 → T-019 (API Client)
T-018 → T-021 (Login Page)
      → T-022 (Register Page)
      → T-023 (Protected Route) → T-024 (Dashboard Layout)

T-020 (Types) → T-026 (TaskList)
             → T-027 (AddTaskForm)
             → T-028 (EditTaskModal)
             → T-029 (Task Service)

T-024,T-026,T-027,T-028,T-029 → T-030 (Dashboard Page)
T-030 → T-032 (Filters)
     → T-033 (Stats)
     → T-034 (Skeletons)

T-021,T-022,T-023 → T-036 (Auth Tests)
T-030 → T-037 (CRUD Tests) → T-038 (Isolation Tests)

T-015 → T-039 (Backend Deploy)
T-031,T-039 → T-040 (Frontend Deploy)
```

---

## Notes

- All tasks follow spec-driven development principles
- Each task has clear acceptance criteria
- Tasks reference specific files to create/modify
- Implementation code provided for critical components
- Testing required before deployment
- Multi-user data isolation enforced at service layer
- JWT authentication shared between Better Auth and backend
