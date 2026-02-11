# Evolution of Todo - Hackathon II

A progressive todo application evolving from a simple console app to a cloud-native AI-powered platform, built using **Spec-Driven Development (SDD)** with Claude Code and SpecKit Plus.

## Project Summary

| Phase | Name | Stack | Status |
|-------|------|-------|--------|
| **I** | Console App | Python 3.13, UV | Complete |
| **II** | Web Application | Next.js, FastAPI, SQLModel, JWT | Complete |
| **III** | AI Chatbot | OpenAI GPT-4o-mini, MCP Server, OpenAI Agents SDK | Complete |
| **IV** | Kubernetes | Docker, Helm, K8s, HPA, RBAC | Complete |
| **V** | Cloud Deployment | GitHub Actions, Kafka, Dapr, Prometheus | Complete |
| **VI** | Cloud Deployment | Vercel, Azure AKS, ACR, Neon PostgreSQL | Complete |

---

## Phase I: Python Console App

**In-memory CRUD todo manager with interactive CLI.**

- Add, view, update, delete tasks
- Mark tasks as complete/incomplete
- Input validation (title 1-200 chars, description max 1000 chars)
- Formatted table display

```bash
cd phase1 && uv run python src/main.py
```

**Tech:** Python 3.13+ | UV | In-memory storage

---

## Phase II: Full-Stack Web Application

**Multi-user web app with authentication and persistent storage.**

### Backend (FastAPI)
- RESTful API with 6 task endpoints + auth endpoints
- JWT-based authentication (register, login)
- Data isolation between users
- Rate limiting (100 req/min general, 20 req/min auth)
- Health check endpoint (`/health`)
- Alembic database migrations

### Frontend (Next.js)
- Landing page, login, register, dashboard
- Task management (create, edit, delete, toggle completion)
- Protected routes with JWT auth
- Responsive design with Tailwind CSS

```bash
# Backend
cd phase2/backend && uvicorn app.main:app --reload

# Frontend
cd frontend && npm run dev
```

**API Endpoints:**
| Method | Path | Description |
|--------|------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login, get JWT token |
| POST | `/tasks/` | Create task |
| GET | `/tasks/` | List user's tasks |
| GET | `/tasks/{id}` | Get specific task |
| PUT | `/tasks/{id}` | Update task |
| PATCH | `/tasks/{id}/toggle` | Toggle completion |
| DELETE | `/tasks/{id}` | Delete task |
| GET | `/health` | Health check |
| GET | `/analytics` | Event analytics |

**Tech:** FastAPI | Next.js 16 | SQLModel | PostgreSQL (Neon) / SQLite | JWT | Tailwind CSS

---

## Phase III: AI Chatbot with MCP

**Natural language task management via AI-powered chatbot.**

- OpenAI GPT-4o-mini agent with system instructions for task management
- MCP (Model Context Protocol) server with 7 tools:
  - `create_task` | `list_tasks` | `get_task` | `update_task` | `complete_task` | `delete_task` | `search_tasks`
- Conversation persistence in database
- Chat UI integrated in dashboard (floating button + modal)
- Typing indicator and tool call display
- 33/33 tests passing

**Usage Examples:**
- "Add buy groceries to my list"
- "Show my tasks"
- "Mark task 1 as done"
- "Find tasks about shopping"

**Tech:** OpenAI GPT-4o-mini | OpenAI Agents SDK | MCP | Conversation persistence

---

## Phase IV: Kubernetes Deployment

**Containerized deployment on Docker Desktop Kubernetes.**

### Docker
- Backend: Python 3.12 slim with health checks
- Frontend: Node.js 20 Alpine, multi-stage build
- docker-compose.yml for local development

### Kubernetes Resources
| Resource | Details |
|----------|---------|
| Namespace | `todo-app` |
| Backend Deployment | 2 replicas, liveness/readiness probes |
| Frontend Deployment | 2 replicas, liveness/readiness probes |
| Services | ClusterIP (backend), NodePort (frontend) |
| HPA | Backend auto-scaling 2-10 pods at 70% CPU |
| ConfigMap | App config (backend URL, model, project name) |
| Secrets | DB URL, JWT secret, API keys |
| RBAC | Service accounts, roles, role bindings |
| Network Policies | Default deny + selective allow rules |

### Helm Chart
```bash
helm install todo-app ./helm/todo-app \
  --set secrets.databaseUrl="your-db-url" \
  --set secrets.jwtSecret="your-secret" \
  --set secrets.geminiApiKey="your-key"
```

```bash
# Docker Compose
cd docker && docker-compose up --build

# Kubernetes (after building images)
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/network-policies.yaml
```

**Tech:** Docker | Kubernetes | Helm 3 | HPA | RBAC | Network Policies

---

## Phase V: Cloud Deployment with Kafka

**Production-grade cloud deployment with event streaming and CI/CD.**

### CI/CD (GitHub Actions)
- **CI pipeline** (`ci.yaml`): Backend tests, frontend build, Docker build, Helm lint
- **CD pipeline** (`deploy.yaml`): Build/push to GHCR, deploy to K8s with Helm
- Automatic deployment on push to `main` (when `KUBE_CONFIG` secret is configured)

### Kafka Event Streaming
- **Event Producer** (`event_service.py`): Publishes task CRUD events to Kafka
- **Event Consumer** (`event_consumer.py`): Processes analytics (events by type/user)
- **Topics**: `task-events`, `task-analytics`, `task-events-dlq`
- **Kafka Options**: Strimzi (in-cluster) or Redpanda (lightweight)

### Dapr Integration
- Pub/Sub component for Kafka
- Event subscription for task-events topic

### Monitoring
- Prometheus ServiceMonitor for backend
- Alert rules: BackendDown, HighErrorRate, HighLatency
- Grafana dashboard (pods, CPU, memory, HPA, health)

### Cloud Providers Supported
- Azure Kubernetes Service (AKS)
- Google Kubernetes Engine (GKE)
- Oracle Container Engine (OKE)

**Tech:** GitHub Actions | Kafka/Redpanda | Dapr | Prometheus | Grafana | GHCR

---

## Phase VI: Cloud Deployment (Live)

**Dual production deployment on Vercel (serverless) and Azure AKS (Kubernetes).**

### Deployment 1: Vercel (Serverless)

| Service | URL |
|---------|-----|
| Frontend (Landing Page) | https://hackaton2-omega.vercel.app |
| Backend API | https://backend-navy-five-43.vercel.app |
| Health Check | https://backend-navy-five-43.vercel.app/health |
| API Documentation | https://backend-navy-five-43.vercel.app/docs |

| Component | Platform | Details |
|-----------|----------|---------|
| **Frontend** | Vercel | Next.js 16 serverless, auto-deploy on push |
| **Backend** | Vercel | FastAPI serverless Python runtime |
| **Database** | Neon PostgreSQL | Serverless Postgres (East US 2) |

### Deployment 2: Azure AKS (Kubernetes)

| Service | URL |
|---------|-----|
| Frontend | http://20.42.153.18 |
| Backend API | http://20.69.114.112 |
| Health Check | http://20.69.114.112/health |

| Component | Platform | Details |
|-----------|----------|---------|
| **AKS Cluster** | Azure | `todo-aks` in West US 2, 2 nodes (Standard_B2s_v2) |
| **Container Registry** | Azure ACR | `todoacrhackathon.azurecr.io` |
| **Backend** | K8s Deployment | 2 replicas, liveness/readiness probes, HPA |
| **Frontend** | K8s Deployment | 2 replicas, LoadBalancer service |
| **Infrastructure** | K8s | RBAC, Network Policies, Secrets, ConfigMaps |

### Features (Both Deployments)
- User registration and login (JWT authentication)
- Task CRUD operations via REST API
- AI chatbot (OpenAI GPT-4o-mini) with MCP tool calling
- Conversation persistence in database

**Tech:** Vercel | Azure AKS | ACR | Neon PostgreSQL | FastAPI | Next.js

---

## Project Structure

```
hackaton2/
├── phase1/                        # Phase I: Console App
│   └── src/                       # Python CLI application
├── phase2/backend/                # Phase II-III: FastAPI Backend
│   └── app/
│       ├── api/                   # REST endpoints (auth, tasks, chat)
│       ├── core/                  # Config, database, auth, rate limiting
│       ├── models/                # SQLModel models
│       ├── services/              # Business logic, AI agent, events
│       └── mcp_tools/             # MCP tool implementations
├── frontend/                      # Phase II-III: Next.js Frontend
│   ├── app/                       # Pages (login, register, dashboard)
│   ├── components/                # UI components (TaskList, Chatbot)
│   └── services/                  # API clients
├── docker/                        # Phase IV: Containerization
│   ├── backend.Dockerfile
│   ├── frontend.Dockerfile
│   └── docker-compose.yml
├── k8s/                           # Phase IV: Kubernetes Manifests
│   ├── backend/                   # Deployment, Service, HPA
│   ├── frontend/                  # Deployment, Service
│   ├── event-consumer/            # Kafka consumer deployment
│   ├── dapr/                      # Dapr pub/sub config
│   ├── monitoring/                # Prometheus + Grafana
│   ├── rbac.yaml                  # RBAC configuration
│   ├── network-policies.yaml      # Network policies
│   ├── configmap.yaml             # ConfigMap
│   └── secrets.yaml               # Secrets
├── helm/todo-app/                 # Phase IV: Helm Chart
│   ├── Chart.yaml
│   ├── values.yaml                # Default values
│   ├── values-production.yaml     # Production values
│   └── templates/                 # K8s resource templates
├── kafka/                         # Phase V: Event Streaming
│   ├── kafka-cluster.yaml         # Strimzi Kafka cluster
│   ├── kafka-topics.yaml          # Topic initialization
│   └── redpanda-values.yaml       # Redpanda Helm values
├── .github/workflows/             # Phase V: CI/CD
│   ├── ci.yaml                    # CI pipeline
│   └── deploy.yaml                # CD pipeline
├── specs/                         # SDD Specifications
│   ├── phase1-console-app/
│   ├── phase2-web-app/
│   ├── phase3-ai-chatbot/
│   ├── phase4-kubernetes/
│   └── phase5-cloud-deployment/
└── history/                       # Development history (PHR, ADR)
```

## Quick Start

### Option 1: Docker Compose (Easiest)
```bash
cd docker
docker-compose up --build
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
```

### Option 2: Kubernetes
```bash
# Build images
docker build -f docker/backend.Dockerfile -t docker-backend:latest .
docker build -f docker/frontend.Dockerfile -t docker-frontend:latest .

# Deploy
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/secrets.yaml
kubectl apply -f k8s/backend/
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/rbac.yaml
kubectl apply -f k8s/network-policies.yaml

# Access
kubectl port-forward -n todo-app svc/backend 8000:8000
kubectl port-forward -n todo-app svc/frontend 3000:3000
```

### Option 3: Local Development
```bash
# Backend
cd phase2/backend
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend (separate terminal)
cd frontend
npm install && npm run dev
```

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | Database connection string | Yes |
| `JWT_SECRET` | JWT signing secret (min 32 chars) | Yes |
| `OPENAI_API_KEY` | OpenAI API key (GPT-4o-mini) | For Phase III |
| `GEMINI_API_KEY` | Google Gemini API key (fallback) | Optional |
| `KAFKA_ENABLED` | Enable Kafka events (`true`/`false`) | For Phase V |
| `KAFKA_BOOTSTRAP_SERVERS` | Kafka broker address | For Phase V |

## Development Methodology

Built using **Spec-Driven Development (SDD)** with the workflow:

1. **Specify** (WHAT) - Define requirements and acceptance criteria
2. **Plan** (HOW) - Create technical architecture
3. **Tasks** (BREAKDOWN) - Atomic, testable work units
4. **Implement** (CODE) - Generate code via Claude Code
5. **Review** - Refine and iterate

All specifications are in `specs/` with `spec.md`, `plan.md`, and `tasks.md` for each phase.

## Repository

- **GitHub**: https://github.com/Wasia93/hackaton2
- **CI/CD**: GitHub Actions (CI + Deploy pipelines)
- **Vercel Frontend**: https://hackaton2-omega.vercel.app
- **Vercel Backend**: https://backend-navy-five-43.vercel.app
- **Azure Frontend**: http://20.42.153.18
- **Azure Backend**: http://20.69.114.112
- **Database**: Neon PostgreSQL (serverless)

---

**Built with Spec-Driven Development using Claude Code & SpecKit Plus**
