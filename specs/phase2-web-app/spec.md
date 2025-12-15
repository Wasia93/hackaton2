# Phase II: Todo Web Application - Specification

**Feature**: Full-Stack Multi-User Todo Web Application
**Phase**: Phase II - Web Application
**Status**: Draft
**Created**: 2025-12-15
**Updated**: 2025-12-15

---

## 1. Overview

Transform the Phase I console app into a modern, multi-user web application with persistent storage, authentication, and a responsive user interface.

### Purpose
- Provide web-based access to todo functionality
- Support multiple users with isolated data
- Persist tasks to PostgreSQL database
- Professional UI/UX with Next.js and Tailwind CSS
- RESTful API backend with FastAPI

### Constraints
- **No manual coding** - All code generated via Claude Code using this spec
- **Spec-Driven Development** - Follow Specify → Plan → Tasks → Implement
- **Monorepo structure** - Frontend and backend in same repository
- **Basic Level features only** - No priorities, tags, search (added in Phase III+)
- **Deployment ready** - Frontend to Vercel, backend deployable

### Key Changes from Phase I
| Aspect | Phase I | Phase II |
|--------|---------|----------|
| Storage | In-memory | PostgreSQL (Neon) |
| Interface | CLI | Web (Next.js) |
| Users | Single | Multi-user with auth |
| Data Persistence | None | Database |
| Architecture | Monolith | Frontend + Backend |

---

## 2. User Journeys

### UJ-1: User Registration
**As a new user**
**I want to** create an account
**So that** I can access my personal todo list

**Flow**:
1. User visits application homepage
2. Clicks "Sign Up" button
3. Enters email and password
4. Submits registration form
5. System creates user account
6. User is redirected to login page
7. Success message displayed

**Acceptance Criteria**:
- ✅ Email validation (valid format, unique)
- ✅ Password validation (min 8 characters)
- ✅ Account created in database
- ✅ Passwords hashed (never stored plain text)
- ✅ Error messages for invalid input
- ✅ Success message after registration

---

### UJ-2: User Login
**As a registered user**
**I want to** log into my account
**So that** I can access my todo list

**Flow**:
1. User visits login page
2. Enters email and password
3. Submits login form
4. System validates credentials
5. JWT token generated and stored
6. User redirected to todo dashboard
7. Dashboard shows user's tasks

**Acceptance Criteria**:
- ✅ Credentials validated against database
- ✅ JWT token issued on successful login
- ✅ Token stored securely (httpOnly cookie or localStorage)
- ✅ Invalid credentials show error message
- ✅ User redirected to dashboard on success
- ✅ Session persists across page refreshes

---

### UJ-3: User Logout
**As a logged-in user**
**I want to** log out of my account
**So that** my data is secure

**Flow**:
1. User clicks "Logout" button
2. System clears JWT token
3. User redirected to login page
4. Cannot access protected routes without re-login

**Acceptance Criteria**:
- ✅ JWT token cleared from storage
- ✅ User redirected to login page
- ✅ Protected routes inaccessible after logout
- ✅ Logout button visible when authenticated

---

### UJ-4: Create Task (Web)
**As a logged-in user**
**I want to** add a new task via web interface
**So that** I can track things to do

**Flow**:
1. User on dashboard, clicks "Add Task" button
2. Modal/form appears with input fields
3. User enters task title (required)
4. User enters description (optional)
5. User clicks "Save" button
6. API POST request to `/api/{user_id}/tasks`
7. Task saved to database with user_id
8. Task appears in user's task list immediately
9. Success notification shown

**Acceptance Criteria**:
- ✅ Task created with auto-increment ID
- ✅ Task associated with authenticated user
- ✅ Title validation (required, max 200 chars)
- ✅ Description validation (max 1000 chars)
- ✅ Task appears in UI immediately
- ✅ Success notification displayed
- ✅ Form resets after successful save

---

### UJ-5: View Tasks (Web)
**As a logged-in user**
**I want to** see all my tasks in a web interface
**So that** I can review what needs to be done

**Flow**:
1. User on dashboard
2. API GET request to `/api/{user_id}/tasks`
3. Backend filters tasks by authenticated user_id
4. Tasks displayed in card/list format
5. Each task shows: Title, Description, Status, Created date

**Acceptance Criteria**:
- ✅ Only user's own tasks are displayed
- ✅ Tasks shown in clean, responsive layout
- ✅ Completed tasks visually distinct (strikethrough, color)
- ✅ Empty state shown if no tasks ("No tasks yet!")
- ✅ Real-time updates after create/update/delete

---

### UJ-6: Update Task (Web)
**As a logged-in user**
**I want to** edit a task's title or description
**So that** I can correct or clarify details

**Flow**:
1. User clicks "Edit" button on a task
2. Editable form appears (inline or modal)
3. Current title and description pre-filled
4. User modifies title and/or description
5. User clicks "Save" button
6. API PUT request to `/api/{user_id}/tasks/{id}`
7. Backend validates user owns the task
8. Task updated in database
9. UI updates immediately
10. Success notification shown

**Acceptance Criteria**:
- ✅ User can only edit their own tasks
- ✅ Title and description editable
- ✅ Validation enforced (title required, length limits)
- ✅ Changes saved to database
- ✅ UI updates without page refresh
- ✅ Cancel button discards changes

---

### UJ-7: Delete Task (Web)
**As a logged-in user**
**I want to** remove a task
**So that** I can declutter my list

**Flow**:
1. User clicks "Delete" button on a task
2. Confirmation dialog appears ("Are you sure?")
3. User confirms deletion
4. API DELETE request to `/api/{user_id}/tasks/{id}`
5. Backend validates user owns the task
6. Task removed from database
7. Task removed from UI immediately
8. Success notification shown

**Acceptance Criteria**:
- ✅ User can only delete their own tasks
- ✅ Confirmation required before deletion
- ✅ Task removed from database
- ✅ UI updates without page refresh
- ✅ Cancel option in confirmation dialog

---

### UJ-8: Toggle Task Completion (Web)
**As a logged-in user**
**I want to** mark tasks as complete or incomplete
**So that** I can track progress

**Flow**:
1. User clicks checkbox/toggle on a task
2. API PATCH request to `/api/{user_id}/tasks/{id}/complete`
3. Backend toggles completed status
4. Task updates in database
5. UI updates immediately (visual style change)

**Acceptance Criteria**:
- ✅ User can only toggle their own tasks
- ✅ Completed status toggles (true ↔ false)
- ✅ Visual feedback (strikethrough, color change, checkmark)
- ✅ Database updated
- ✅ UI updates without page refresh

---

## 3. Functional Requirements

### FR-1: User Authentication & Authorization

**Priority**: CRITICAL
**Dependencies**: None

**Requirements**:
- Use **Better Auth** for authentication
- Email + password authentication (social login optional)
- JWT tokens for API authorization
- Password hashing with bcrypt/argon2
- Shared secret between frontend and backend for JWT verification

**Better Auth Configuration**:
```typescript
// better-auth.ts (frontend)
{
  providers: [emailPassword()],
  jwt: {
    enabled: true,
    secret: process.env.BETTER_AUTH_SECRET
  }
}
```

**Security**:
- Passwords never stored in plain text
- JWT tokens expire after 7 days
- httpOnly cookies or secure localStorage
- CORS configured for frontend domain only

---

### FR-2: Multi-User Data Isolation

**Priority**: CRITICAL
**Dependencies**: FR-1

**Requirements**:
- Each task has `user_id` foreign key
- All API queries filter by authenticated user_id
- Users cannot access other users' tasks
- API validates JWT and extracts user_id for every request

**Implementation**:
- FastAPI middleware verifies JWT
- Extract user_id from JWT payload
- All database queries include `WHERE user_id = {authenticated_user_id}`

---

### FR-3: Database Schema (Neon PostgreSQL)

**Priority**: CRITICAL
**Dependencies**: None

**Tables**:

**users** (managed by Better Auth):
```sql
CREATE TABLE users (
  id VARCHAR(255) PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  name VARCHAR(255),
  password_hash VARCHAR(255) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**tasks**:
```sql
CREATE TABLE tasks (
  id SERIAL PRIMARY KEY,
  user_id VARCHAR(255) NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  title VARCHAR(200) NOT NULL,
  description TEXT,
  completed BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

  INDEX idx_user_id (user_id),
  INDEX idx_completed (completed)
);
```

**SQLModel Classes**:
```python
class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

---

### FR-4: REST API Endpoints

**Priority**: CRITICAL
**Dependencies**: FR-1, FR-2, FR-3

**Base URL**: `http://localhost:8000` (development)

**Authentication Required**: All endpoints require valid JWT token

**Endpoints**:

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/signup` | User registration | No |
| POST | `/api/auth/login` | User login | No |
| POST | `/api/auth/logout` | User logout | Yes |
| GET | `/api/{user_id}/tasks` | List all user's tasks | Yes |
| POST | `/api/{user_id}/tasks` | Create new task | Yes |
| GET | `/api/{user_id}/tasks/{id}` | Get task by ID | Yes |
| PUT | `/api/{user_id}/tasks/{id}` | Update task | Yes |
| DELETE | `/api/{user_id}/tasks/{id}` | Delete task | Yes |
| PATCH | `/api/{user_id}/tasks/{id}/complete` | Toggle completion | Yes |

**Request/Response Formats**:

POST `/api/{user_id}/tasks`:
```json
Request:
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}

Response (201):
{
  "id": 1,
  "user_id": "user123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2025-12-15T10:30:00Z",
  "updated_at": "2025-12-15T10:30:00Z"
}
```

GET `/api/{user_id}/tasks`:
```json
Response (200):
[
  {
    "id": 1,
    "user_id": "user123",
    "title": "Buy groceries",
    "description": "Milk, eggs, bread",
    "completed": false,
    "created_at": "2025-12-15T10:30:00Z",
    "updated_at": "2025-12-15T10:30:00Z"
  }
]
```

**Error Responses**:
```json
400 Bad Request:
{
  "error": "Validation error",
  "detail": "Title is required"
}

401 Unauthorized:
{
  "error": "Unauthorized",
  "detail": "Invalid or missing JWT token"
}

404 Not Found:
{
  "error": "Not found",
  "detail": "Task not found with ID 5"
}
```

---

### FR-5: Frontend UI/UX

**Priority**: CRITICAL
**Dependencies**: FR-4

**Technology Stack**:
- Next.js 16+ (App Router)
- TypeScript
- Tailwind CSS
- React Server Components (default)
- Client Components for interactivity

**Pages**:

1. **Landing Page** (`/`)
   - Marketing page with app description
   - "Sign Up" and "Login" buttons
   - Responsive design

2. **Sign Up Page** (`/auth/signup`)
   - Email input
   - Password input (with show/hide toggle)
   - Confirm password
   - "Create Account" button
   - Link to login page

3. **Login Page** (`/auth/login`)
   - Email input
   - Password input
   - "Login" button
   - Link to signup page
   - Error messages displayed

4. **Dashboard** (`/dashboard`)
   - Protected route (requires authentication)
   - Header with user name and logout button
   - "Add Task" button
   - Task list (cards or table)
   - Empty state if no tasks

**Components**:
- `TaskCard` - Display single task with edit/delete/toggle
- `TaskForm` - Create/edit task form (modal or inline)
- `AuthForm` - Reusable form for login/signup
- `Header` - App header with navigation
- `ProtectedRoute` - HOC for authentication check

**Responsive Design**:
- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px)
- Stack vertically on mobile
- Grid layout on desktop

---

## 4. Non-Functional Requirements

### NFR-1: Performance
- Page load time < 2 seconds
- API response time < 500ms for CRUD operations
- Database queries optimized with indexes
- Frontend optimized (code splitting, lazy loading)

### NFR-2: Security
- HTTPS required in production
- JWT tokens expire and refresh
- CORS configured properly
- SQL injection prevented (SQLModel parameterized queries)
- XSS prevented (React escaping)
- CSRF protection

### NFR-3: Scalability
- Horizontal scaling ready (stateless backend)
- Database connection pooling
- Neon Serverless auto-scales

### NFR-4: Usability
- Intuitive UI (no training required)
- Clear error messages
- Loading states during API calls
- Success notifications
- Responsive on mobile and desktop

### NFR-5: Maintainability
- Type safety (TypeScript + Python type hints)
- Clear folder structure
- Component reusability
- API client abstraction
- Environment-based configuration

---

## 5. Acceptance Criteria

### AC-1: User Registration
- ✅ User can create account with email and password
- ✅ Email validation enforced
- ✅ Password min 8 characters
- ✅ Duplicate email shows error
- ✅ Success message after registration
- ✅ Redirect to login page

### AC-2: User Login
- ✅ User can login with correct credentials
- ✅ Invalid credentials show error
- ✅ JWT token issued and stored
- ✅ Redirect to dashboard on success
- ✅ Session persists across refreshes

### AC-3: User Logout
- ✅ Logout button works
- ✅ JWT token cleared
- ✅ Redirect to login page
- ✅ Dashboard inaccessible after logout

### AC-4: Create Task
- ✅ User can add task with title and description
- ✅ Title validation enforced
- ✅ Task saved to database with user_id
- ✅ Task appears in UI immediately
- ✅ Success notification shown

### AC-5: View Tasks
- ✅ User sees only their own tasks
- ✅ Tasks displayed in clean layout
- ✅ Completed tasks visually distinct
- ✅ Empty state for no tasks

### AC-6: Update Task
- ✅ User can edit title and description
- ✅ Changes saved to database
- ✅ UI updates without refresh
- ✅ Validation enforced

### AC-7: Delete Task
- ✅ User can delete task with confirmation
- ✅ Task removed from database
- ✅ UI updates without refresh

### AC-8: Toggle Completion
- ✅ User can toggle task completion
- ✅ Visual feedback immediate
- ✅ Database updated

### AC-9: Data Isolation
- ✅ User A cannot see User B's tasks
- ✅ User A cannot modify User B's tasks
- ✅ API enforces authorization

### AC-10: Deployment
- ✅ Frontend deployed to Vercel
- ✅ Backend deployable (Railway, Render, etc.)
- ✅ Environment variables configured
- ✅ Database connected

---

## 6. Out of Scope (Phase II)

The following features are explicitly **excluded** from Phase II:

- ❌ AI Chatbot interface (Phase III)
- ❌ MCP server (Phase III)
- ❌ Priorities and tags (Phase III+)
- ❌ Search and filter (Phase III+)
- ❌ Due dates and reminders (Phase V)
- ❌ Recurring tasks (Phase V)
- ❌ Kubernetes deployment (Phase IV)
- ❌ Kafka/Dapr (Phase V)
- ❌ Social login (optional, may add later)
- ❌ Password reset flow (nice-to-have)
- ❌ Email verification (nice-to-have)

---

## 7. Dependencies

### External Services
- **Neon PostgreSQL** - Free tier (https://neon.tech)
- **Vercel** - Frontend hosting (free tier)
- **Backend Hosting** - Railway, Render, or similar (free tier)

### Frontend Dependencies
- Next.js 16+
- React 19+
- TypeScript
- Tailwind CSS
- Better Auth
- Axios or Fetch API

### Backend Dependencies
- Python 3.13+
- FastAPI
- SQLModel
- Psycopg2-binary
- Python-Jose (JWT)
- Passlib (password hashing)
- Python-dotenv

---

## 8. Risks and Assumptions

### Risks
- **R-1**: Neon database connection issues (mitigated by connection pooling)
- **R-2**: JWT token security (mitigated by short expiration, secure storage)
- **R-3**: CORS configuration (mitigated by proper setup)
- **R-4**: Better Auth integration complexity (mitigated by documentation)

### Assumptions
- **A-1**: Neon free tier sufficient for development
- **A-2**: Vercel free tier sufficient for frontend
- **A-3**: Users have modern browsers (Chrome, Firefox, Safari)
- **A-4**: Internet connection available (no offline mode)
- **A-5**: English language only (no i18n in Phase II)

---

## 9. Success Metrics

Phase II is successful when:
- ✅ Users can register, login, and logout
- ✅ All 5 Basic Level features work in web interface
- ✅ Multi-user data isolation enforced
- ✅ Tasks persist to PostgreSQL database
- ✅ Frontend deployed to Vercel
- ✅ Backend deployable and functional
- ✅ All acceptance criteria pass
- ✅ Code generated via Claude Code (no manual coding)
- ✅ Follows constitution principles

---

## 10. References

- [Phase I Spec](../phase1-console-app/spec.md) - Console app requirements
- [Constitution](../../.specify/memory/constitution.md) - Project principles
- [AGENTS.md](../../AGENTS.md) - Agent workflow instructions
- [Documentation](../../.claude/commands/documentation.md) - Hackathon requirements

---

**Spec Version**: 1.0.0
**Approved By**: [Pending approval]
**Approval Date**: [Pending]
**Next Step**: Create plan.md (HOW to build)
