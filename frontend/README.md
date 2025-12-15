# Todo App Frontend

**Phase II - Full-Stack Web Application Frontend**

Next.js 16+ frontend with TypeScript, Tailwind CSS, and Better Auth integration.

---

## Tech Stack

- **Framework**: Next.js 16+ (App Router)
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **Authentication**: Better Auth (planned) - currently using mock auth
- **API Client**: Custom fetch wrapper with JWT support

---

## Project Structure

```
frontend/
├── app/
│   ├── page.tsx                # Home page (landing)
│   ├── login/
│   │   └── page.tsx           # Login page
│   ├── register/
│   │   └── page.tsx           # Registration page
│   └── dashboard/
│       ├── layout.tsx         # Dashboard layout with nav
│       └── page.tsx           # Dashboard with task management
├── lib/
│   └── api.ts                 # API client utility
├── services/
│   └── taskService.ts         # Task API service
├── types/
│   └── task.ts                # TypeScript type definitions
├── .env.local.example         # Environment variables template
└── README.md                  # This file
```

---

## Setup Instructions

### 1. Install Dependencies

```bash
cd frontend
npm install
```

### 2. Configure Environment Variables

```bash
cp .env.local.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_JWT_SECRET=your-super-secret-jwt-key
```

### 3. Run Development Server

```bash
npm run dev
```

Frontend will be available at: `http://localhost:3000`

---

## Pages

### Public Pages

- **`/`** - Landing page with login/register links
- **`/login`** - User login (mock auth for now)
- **`/register`** - User registration (mock auth for now)

### Protected Pages

- **`/dashboard`** - Task management dashboard
  - Add tasks
  - View all tasks
  - Toggle completion
  - Edit tasks
  - Delete tasks

---

## Features Implemented

### Core Features (Phase II - Current)

- ✅ Landing page with CTA
- ✅ Login page with form validation
- ✅ Register page with password requirements
- ✅ Dashboard layout with logout
- ✅ Task creation with title and description
- ✅ Task list display
- ✅ Task completion toggle
- ✅ Task editing (modal)
- ✅ Task deletion with confirmation
- ✅ API integration with backend
- ✅ JWT authentication (localStorage)
- ✅ TypeScript type safety
- ✅ Responsive design with Tailwind CSS

### Pending Features

- ⏳ Better Auth integration (T-017, T-018)
- ⏳ Protected route wrapper (T-023)
- ⏳ Component-based architecture (T-026, T-027, T-028)
- ⏳ Filter and sort functionality (T-032)
- ⏳ Task statistics (T-033)
- ⏳ Loading skeletons (T-034)
- ⏳ Error boundary (T-035)

---

## Authentication

**Current Implementation (Mock)**:
- Login/register forms store a mock JWT token in localStorage
- All API requests include the token in `Authorization` header
- Logout clears the token and redirects to login

**Planned (Better Auth)**:
- Real JWT token generation and validation
- Session management
- Secure cookie storage
- Password hashing
- Email verification

---

## API Integration

The frontend communicates with the FastAPI backend:

- **Base URL**: `http://localhost:8000` (configurable via `NEXT_PUBLIC_API_URL`)
- **Authentication**: JWT Bearer token
- **Endpoints**:
  - `POST /tasks/` - Create task
  - `GET /tasks/` - Get all tasks
  - `GET /tasks/{id}` - Get specific task
  - `PUT /tasks/{id}` - Update task
  - `DELETE /tasks/{id}` - Delete task
  - `PATCH /tasks/{id}/toggle` - Toggle completion

---

## Running with Backend

### 1. Start Backend (in separate terminal)

```bash
cd ../backend
source venv/bin/activate  # or venv\Scripts\activate on Windows
uvicorn app.main:app --reload
```

### 2. Start Frontend

```bash
cd frontend
npm run dev
```

### 3. Access Application

- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## Development Workflow

### Adding New Features

1. Define TypeScript types in `types/`
2. Create API service in `services/`
3. Build UI components in `components/`
4. Create pages in `app/`
5. Test integration with backend

### Code Quality

```bash
# Type checking
npm run build

# Linting
npm run lint
```

---

## Deployment

### Vercel (Recommended)

1. Push code to GitHub
2. Connect repository to Vercel
3. Set environment variables:
   - `NEXT_PUBLIC_API_URL` - Production backend URL
   - `NEXT_PUBLIC_JWT_SECRET` - Production JWT secret
4. Deploy!

### Environment Variables for Production

```env
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_JWT_SECRET=your-production-jwt-secret
```

---

## Tasks Completed

### Phase II Frontend (Current Progress)

- ✅ T-016: Next.js 16+ initialization
- ✅ T-019: API client utility
- ✅ T-020: TypeScript type definitions
- ✅ T-021: Login page
- ✅ T-022: Register page
- ✅ T-024: Dashboard layout
- ✅ T-025: Environment configuration
- ✅ T-029: Task API service
- ✅ T-030: Dashboard page with CRUD
- ✅ T-031: Landing page

### Pending Tasks

- ⏳ T-017: Install Better Auth
- ⏳ T-018: Configure Better Auth
- ⏳ T-023: Protected route wrapper
- ⏳ T-026: TaskList component
- ⏳ T-027: AddTaskForm component
- ⏳ T-028: EditTaskModal component
- ⏳ T-032: Filter/sort functionality
- ⏳ T-033: Task statistics component
- ⏳ T-034: Loading skeletons
- ⏳ T-035: Error boundary

---

## Next Steps

1. ✅ Connect to backend API (done - using mock auth)
2. ⏳ Implement Better Auth (T-017, T-018)
3. ⏳ Add protected routes (T-023)
4. ⏳ Componentize dashboard (T-026, T-027, T-028)
5. ⏳ Add filters and stats (T-032, T-033)
6. ⏳ Deploy to Vercel (T-040)

---

**Generated with Spec-Driven Development**
**Claude Code + SpecKit Plus**
**Phase II - Full-Stack Web Application**
