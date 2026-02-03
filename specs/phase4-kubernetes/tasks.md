# Phase IV: Kubernetes Deployment - Tasks

**Feature**: Containerization and Local Kubernetes Deployment
**Phase**: Phase IV - Docker & Kubernetes
**Status**: Ready for Implementation
**Created**: 2026-01-26
**Updated**: 2026-01-26
**Spec Reference**: [spec.md](./spec.md)
**Plan Reference**: [plan.md](./plan.md)

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| A | T-001 to T-006 | Docker Foundation |
| B | T-007 to T-009 | Health Endpoints |
| C | T-010 to T-017 | Kubernetes Manifests |
| D | T-018 to T-023 | Helm Chart |
| E | T-024 to T-028 | Testing & Validation |

**Total Tasks**: 28

---

## Phase A: Docker Foundation

### T-001: Create Docker Directory Structure

**Description**: Set up the docker directory with necessary files.

**Preconditions**:
- Phase III codebase exists
- Project root is hackaton2/

**Expected Output**:
```
docker/
  .dockerignore
  .env.example
```

**Artifacts to Create**:
- `docker/.dockerignore`
- `docker/.env.example`

**Acceptance Criteria**:
- [ ] docker/ directory created
- [ ] .dockerignore excludes node_modules, __pycache__, .env, .git
- [ ] .env.example has placeholder values

**From Spec**: FR-1 (Docker Containerization)
**From Plan**: Section 5 (Docker Compose)

---

### T-002: Create Frontend Dockerfile

**Description**: Create multi-stage Dockerfile for Next.js frontend.

**Preconditions**:
- T-001 complete
- frontend/ directory exists with package.json

**Expected Output**:
```dockerfile
# docker/frontend.Dockerfile
FROM node:20-alpine AS builder
WORKDIR /app
COPY frontend/package*.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build

FROM node:20-alpine
WORKDIR /app
ENV NODE_ENV=production
COPY --from=builder /app/.next/standalone ./
COPY --from=builder /app/.next/static ./.next/static
COPY --from=builder /app/public ./public
EXPOSE 3000
CMD ["node", "server.js"]
```

**Artifacts to Create**:
- `docker/frontend.Dockerfile`

**Acceptance Criteria**:
- [ ] Multi-stage build (builder + production)
- [ ] Uses node:20-alpine base
- [ ] Builds Next.js application
- [ ] Exposes port 3000
- [ ] Image builds successfully: `docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .`
- [ ] Image size < 500MB

**From Spec**: FR-1
**From Plan**: Section 2.1 (Frontend Container)

---

### T-003: Update Next.js for Standalone Output

**Description**: Configure Next.js to produce standalone output for Docker.

**Preconditions**:
- T-002 complete
- frontend/next.config.ts exists

**Expected Output**:
```typescript
// frontend/next.config.ts
const nextConfig = {
  output: 'standalone',
  // ... existing config
};
```

**Artifacts to Modify**:
- `frontend/next.config.ts`

**Acceptance Criteria**:
- [ ] output: 'standalone' added to config
- [ ] npm run build creates .next/standalone directory
- [ ] Standalone server runs correctly

**From Spec**: FR-1
**From Plan**: Section 2.1

---

### T-004: Create Backend Dockerfile

**Description**: Create Dockerfile for FastAPI backend with UV.

**Preconditions**:
- T-001 complete
- phase2/backend/ directory exists

**Expected Output**:
```dockerfile
# docker/backend.Dockerfile
FROM python:3.13-slim

WORKDIR /app

# Install UV
RUN pip install uv

# Copy requirements and install
COPY phase2/backend/requirements.txt ./
RUN pip install -r requirements.txt

# Copy application
COPY phase2/backend/app ./app
COPY phase2/backend/alembic ./alembic
COPY phase2/backend/alembic.ini ./

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Artifacts to Create**:
- `docker/backend.Dockerfile`

**Acceptance Criteria**:
- [ ] Uses python:3.13-slim base
- [ ] Installs dependencies from requirements.txt
- [ ] Runs as non-root user
- [ ] Exposes port 8000
- [ ] Image builds successfully: `docker build -f docker/backend.Dockerfile -t todo-backend:latest .`
- [ ] Image size < 500MB

**From Spec**: FR-1
**From Plan**: Section 2.2 (Backend Container)

---

### T-005: Create Docker Compose File

**Description**: Create docker-compose.yml for local multi-service deployment.

**Preconditions**:
- T-002 and T-004 complete

**Expected Output**:
```yaml
# docker/docker-compose.yml
version: '3.8'

services:
  frontend:
    build:
      context: ..
      dockerfile: docker/frontend.Dockerfile
    ports:
      - "3000:3000"
    environment:
      - NEXT_PUBLIC_API_URL=http://backend:8000
    depends_on:
      backend:
        condition: service_healthy
    networks:
      - todo-network

  backend:
    build:
      context: ..
      dockerfile: docker/backend.Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
```

**Artifacts to Create**:
- `docker/docker-compose.yml`

**Acceptance Criteria**:
- [ ] Defines frontend and backend services
- [ ] Network configuration for inter-service communication
- [ ] Environment variables from .env file
- [ ] Health check for backend
- [ ] Frontend depends on backend being healthy
- [ ] `docker-compose -f docker/docker-compose.yml up` runs successfully

**From Spec**: FR-2 (Docker Compose)
**From Plan**: Section 5

---

### T-006: Test Docker Compose Deployment

**Description**: Verify Docker Compose runs all services correctly.

**Preconditions**:
- T-005 complete
- .env file created with real values

**Steps**:
1. Create `docker/.env` from `.env.example`
2. Add real DATABASE_URL, JWT_SECRET, OPENAI_API_KEY
3. Run `docker-compose -f docker/docker-compose.yml build`
4. Run `docker-compose -f docker/docker-compose.yml up`
5. Verify frontend at http://localhost:3000
6. Verify backend at http://localhost:8000/health
7. Test login and task operations

**Acceptance Criteria**:
- [ ] Both containers start without errors
- [ ] Frontend accessible at localhost:3000
- [ ] Backend health endpoint returns 200
- [ ] Can create account and login
- [ ] Can create, list, complete, delete tasks
- [ ] Chatbot works and can manage tasks

**From Spec**: AC-1 (Docker Images)
**From Plan**: Section 7.2

---

## Phase B: Health Endpoints

### T-007: Add Health Endpoint to Backend

**Description**: Implement /health endpoint for Kubernetes probes.

**Preconditions**:
- Backend codebase exists
- Database connection configured

**Expected Output**:
```python
# phase2/backend/app/api/health.py
from datetime import datetime
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from app.core.database import get_session

router = APIRouter()

@router.get("/health")
async def health_check(session: Session = Depends(get_session)):
    """Health check endpoint for Kubernetes probes."""
    checks = {}
    status = "healthy"

    # Check database connection
    try:
        session.exec(select(1))
        checks["database"] = "ok"
    except Exception as e:
        checks["database"] = f"failed: {str(e)}"
        status = "unhealthy"

    response = {
        "status": status,
        "service": "backend",
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "checks": checks
    }

    if status == "unhealthy":
        return JSONResponse(content=response, status_code=503)
    return response
```

**Artifacts to Create/Modify**:
- `phase2/backend/app/api/health.py` (create)
- `phase2/backend/app/main.py` (add router)

**Acceptance Criteria**:
- [ ] GET /health returns 200 when healthy
- [ ] GET /health returns 503 when database unavailable
- [ ] Response includes status, service, timestamp, checks
- [ ] Response time < 100ms

**From Spec**: FR-4 (Health Check Endpoints)
**From Plan**: Section 6.1

---

### T-008: Test Health Endpoint Success

**Description**: Verify health endpoint returns correct response when healthy.

**Preconditions**:
- T-007 complete
- Backend running with database connection

**Steps**:
1. Start backend with valid DATABASE_URL
2. Call GET /health
3. Verify response structure and status

**Expected Response**:
```json
{
  "status": "healthy",
  "service": "backend",
  "timestamp": "2026-01-26T10:00:00Z",
  "checks": {
    "database": "ok"
  }
}
```

**Acceptance Criteria**:
- [ ] HTTP status code is 200
- [ ] status field is "healthy"
- [ ] database check is "ok"
- [ ] timestamp is valid ISO format

**From Spec**: FR-4
**From Plan**: Section 6.1

---

### T-009: Test Health Endpoint Failure

**Description**: Verify health endpoint returns 503 when database unavailable.

**Preconditions**:
- T-007 complete

**Steps**:
1. Start backend with invalid DATABASE_URL
2. Call GET /health
3. Verify response indicates failure

**Expected Response**:
```json
{
  "status": "unhealthy",
  "service": "backend",
  "timestamp": "2026-01-26T10:00:00Z",
  "checks": {
    "database": "failed: ..."
  }
}
```

**Acceptance Criteria**:
- [ ] HTTP status code is 503
- [ ] status field is "unhealthy"
- [ ] database check indicates failure

**From Spec**: FR-4
**From Plan**: Section 6.1

---

## Phase C: Kubernetes Manifests

### T-010: Create Kubernetes Directory Structure

**Description**: Set up k8s directory with subdirectories.

**Preconditions**:
- None

**Expected Output**:
```
k8s/
  frontend/
  backend/
```

**Artifacts to Create**:
- `k8s/` directory
- `k8s/frontend/` subdirectory
- `k8s/backend/` subdirectory

**Acceptance Criteria**:
- [ ] Directory structure created

**From Spec**: FR-3 (Kubernetes Manifests)
**From Plan**: Section 3

---

### T-011: Create Namespace Manifest

**Description**: Create Kubernetes namespace for the application.

**Preconditions**:
- T-010 complete

**Expected Output**:
```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/part-of: evolution-of-todo
```

**Artifacts to Create**:
- `k8s/namespace.yaml`

**Acceptance Criteria**:
- [ ] Namespace manifest is valid YAML
- [ ] `kubectl apply -f k8s/namespace.yaml` creates namespace
- [ ] `kubectl get ns todo-app` shows namespace

**From Spec**: FR-3
**From Plan**: Section 3.1

---

### T-012: Create Secrets Manifest

**Description**: Create Kubernetes secrets for sensitive configuration.

**Preconditions**:
- T-011 complete

**Expected Output**:
```yaml
# k8s/secrets.yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app
type: Opaque
stringData:
  database-url: "YOUR_DATABASE_URL_HERE"
  jwt-secret: "YOUR_JWT_SECRET_HERE"
  openai-api-key: "YOUR_OPENAI_API_KEY_HERE"
```

**Artifacts to Create**:
- `k8s/secrets.yaml`

**Acceptance Criteria**:
- [ ] Secret manifest is valid YAML
- [ ] Contains database-url, jwt-secret, openai-api-key
- [ ] Uses stringData for base64 encoding
- [ ] `kubectl apply -f k8s/secrets.yaml` creates secret
- [ ] Secret has .gitignore entry (template only in repo)

**From Spec**: FR-3
**From Plan**: Section 3.2

---

### T-013: Create ConfigMap Manifest

**Description**: Create Kubernetes ConfigMap for non-sensitive configuration.

**Preconditions**:
- T-011 complete

**Expected Output**:
```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: todo-app
data:
  BACKEND_URL: "http://backend:8000"
  OPENAI_AGENT_MODEL: "gpt-4o"
```

**Artifacts to Create**:
- `k8s/configmap.yaml`

**Acceptance Criteria**:
- [ ] ConfigMap manifest is valid YAML
- [ ] Contains non-sensitive configuration
- [ ] `kubectl apply -f k8s/configmap.yaml` creates configmap

**From Spec**: FR-3
**From Plan**: Section 3.3

---

### T-014: Create Frontend Deployment Manifest

**Description**: Create Kubernetes Deployment for frontend service.

**Preconditions**:
- T-011, T-013 complete

**Expected Output**:
```yaml
# k8s/frontend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
  labels:
    app: frontend
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    metadata:
      labels:
        app: frontend
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: BACKEND_URL
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /
            port: 3000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Artifacts to Create**:
- `k8s/frontend/deployment.yaml`

**Acceptance Criteria**:
- [ ] Deployment manifest is valid YAML
- [ ] 2 replicas configured
- [ ] Liveness and readiness probes configured
- [ ] Resource limits set
- [ ] Environment from ConfigMap

**From Spec**: FR-3
**From Plan**: Section 3.4

---

### T-015: Create Frontend Service Manifest

**Description**: Create Kubernetes Service for frontend.

**Preconditions**:
- T-014 complete

**Expected Output**:
```yaml
# k8s/frontend/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: todo-app
  labels:
    app: frontend
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30300
    protocol: TCP
```

**Artifacts to Create**:
- `k8s/frontend/service.yaml`

**Acceptance Criteria**:
- [ ] Service manifest is valid YAML
- [ ] NodePort type for Minikube access
- [ ] Selector matches deployment labels
- [ ] Port 3000 exposed

**From Spec**: FR-3
**From Plan**: Section 3.6

---

### T-016: Create Backend Deployment Manifest

**Description**: Create Kubernetes Deployment for backend service.

**Preconditions**:
- T-011, T-012, T-013 complete

**Expected Output**:
```yaml
# k8s/backend/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
  labels:
    app: backend
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    metadata:
      labels:
        app: backend
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
        - name: JWT_SECRET
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: jwt-secret
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: openai-api-key
        - name: OPENAI_AGENT_MODEL
          valueFrom:
            configMapKeyRef:
              name: todo-config
              key: OPENAI_AGENT_MODEL
        resources:
          requests:
            memory: "256Mi"
            cpu: "100m"
          limits:
            memory: "512Mi"
            cpu: "500m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
```

**Artifacts to Create**:
- `k8s/backend/deployment.yaml`

**Acceptance Criteria**:
- [ ] Deployment manifest is valid YAML
- [ ] 3 replicas configured
- [ ] Liveness and readiness probes use /health
- [ ] Secrets injected as environment variables
- [ ] ConfigMap values injected
- [ ] Resource limits set

**From Spec**: FR-3
**From Plan**: Section 3.5

---

### T-017: Create Backend Service and HPA Manifests

**Description**: Create Kubernetes Service and HPA for backend.

**Preconditions**:
- T-016 complete

**Expected Output**:
```yaml
# k8s/backend/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: todo-app
  labels:
    app: backend
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
    protocol: TCP
---
# k8s/backend/hpa.yaml
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: backend-hpa
  namespace: todo-app
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: backend
  minReplicas: 2
  maxReplicas: 10
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
```

**Artifacts to Create**:
- `k8s/backend/service.yaml`
- `k8s/backend/hpa.yaml`

**Acceptance Criteria**:
- [ ] Service manifest is valid YAML
- [ ] ClusterIP type for internal access
- [ ] HPA configured with min/max replicas
- [ ] HPA targets 70% CPU utilization

**From Spec**: FR-3, FR-6
**From Plan**: Section 3.6, 3.7

---

## Phase D: Helm Chart

### T-018: Create Helm Chart Structure

**Description**: Set up Helm chart directory and Chart.yaml.

**Preconditions**:
- Phase C complete

**Expected Output**:
```
helm/todo-app/
  Chart.yaml
  templates/
    _helpers.tpl
```

**Artifacts to Create**:
- `helm/todo-app/Chart.yaml`
- `helm/todo-app/templates/_helpers.tpl`

**Acceptance Criteria**:
- [ ] Chart.yaml has name, version, appVersion
- [ ] _helpers.tpl has common label definitions
- [ ] `helm lint ./helm/todo-app` passes

**From Spec**: FR-5 (Helm Chart)
**From Plan**: Section 4.1

---

### T-019: Create Helm values.yaml

**Description**: Create parameterized values file.

**Preconditions**:
- T-018 complete

**Expected Output**: See plan.md Section 4.2 for full values.yaml

**Artifacts to Create**:
- `helm/todo-app/values.yaml`

**Acceptance Criteria**:
- [ ] Frontend configuration (replica, image, resources)
- [ ] Backend configuration (replica, image, resources, autoscaling)
- [ ] Config section for non-sensitive values
- [ ] Secrets section (empty defaults)

**From Spec**: FR-5
**From Plan**: Section 4.2

---

### T-020: Create Helm Templates for Base Resources

**Description**: Create templated namespace, secrets, and configmap.

**Preconditions**:
- T-019 complete

**Artifacts to Create**:
- `helm/todo-app/templates/namespace.yaml`
- `helm/todo-app/templates/secrets.yaml`
- `helm/todo-app/templates/configmap.yaml`

**Acceptance Criteria**:
- [ ] Templates use Helm values
- [ ] Templates use _helpers.tpl functions
- [ ] `helm template ./helm/todo-app` renders correctly

**From Spec**: FR-5
**From Plan**: Section 4.3

---

### T-021: Create Helm Templates for Frontend

**Description**: Create templated frontend deployment and service.

**Preconditions**:
- T-020 complete

**Artifacts to Create**:
- `helm/todo-app/templates/frontend/deployment.yaml`
- `helm/todo-app/templates/frontend/service.yaml`

**Acceptance Criteria**:
- [ ] Uses values for replica count
- [ ] Uses values for image repository/tag
- [ ] Uses values for resources
- [ ] Uses values for probes
- [ ] Renders correctly with `helm template`

**From Spec**: FR-5
**From Plan**: Section 4.3

---

### T-022: Create Helm Templates for Backend

**Description**: Create templated backend deployment, service, and HPA.

**Preconditions**:
- T-021 complete

**Artifacts to Create**:
- `helm/todo-app/templates/backend/deployment.yaml`
- `helm/todo-app/templates/backend/service.yaml`
- `helm/todo-app/templates/backend/hpa.yaml`

**Acceptance Criteria**:
- [ ] Uses values for replica count
- [ ] Uses values for image repository/tag
- [ ] Uses values for resources
- [ ] HPA conditionally rendered (if autoscaling.enabled)
- [ ] Renders correctly with `helm template`

**From Spec**: FR-5
**From Plan**: Section 4.3

---

### T-023: Test Helm Chart Installation

**Description**: Verify Helm chart installs, upgrades, and uninstalls correctly.

**Preconditions**:
- T-022 complete
- Minikube running with images loaded

**Steps**:
1. `helm install todo-app ./helm/todo-app -n todo-app --create-namespace --set secrets.databaseUrl=... --set secrets.jwtSecret=... --set secrets.openaiApiKey=...`
2. Verify all pods running
3. `helm upgrade todo-app ./helm/todo-app -n todo-app --set backend.replicaCount=4`
4. Verify backend scaled to 4
5. `helm uninstall todo-app -n todo-app`
6. Verify all resources removed

**Acceptance Criteria**:
- [ ] Helm install succeeds
- [ ] All pods reach Running state
- [ ] Helm upgrade changes values
- [ ] Helm uninstall removes all resources

**From Spec**: AC-5 (Helm Chart)
**From Plan**: Section 7.3

---

## Phase E: Testing & Validation

### T-024: Test Kubernetes Deployment with kubectl

**Description**: Deploy application using raw kubectl manifests.

**Preconditions**:
- Minikube running
- Docker images built and loaded to Minikube
- k8s/secrets.yaml edited with real values

**Steps**:
1. `minikube start --driver=docker --cpus=4 --memory=8192`
2. `minikube image load todo-frontend:latest`
3. `minikube image load todo-backend:latest`
4. `kubectl apply -f k8s/namespace.yaml`
5. `kubectl apply -f k8s/secrets.yaml`
6. `kubectl apply -f k8s/configmap.yaml`
7. `kubectl apply -f k8s/frontend/`
8. `kubectl apply -f k8s/backend/`
9. `kubectl get pods -n todo-app` (wait for Running)
10. `kubectl port-forward svc/frontend 3000:3000 -n todo-app`
11. Access http://localhost:3000

**Acceptance Criteria**:
- [ ] All manifests apply without errors
- [ ] All pods reach Running state
- [ ] No CrashLoopBackOff errors
- [ ] Frontend accessible via port-forward
- [ ] Backend health endpoint responds

**From Spec**: AC-2 (Kubernetes Deployment)
**From Plan**: Section 7.3

---

### T-025: Test Health Probes

**Description**: Verify liveness and readiness probes work correctly.

**Preconditions**:
- T-024 complete

**Steps**:
1. `kubectl describe pod -l app=backend -n todo-app`
2. Verify liveness and readiness probes configured
3. Observe probe results in events
4. Simulate failure (optional): delete database connection
5. Watch pod restart

**Acceptance Criteria**:
- [ ] Liveness probes configured correctly
- [ ] Readiness probes configured correctly
- [ ] Probes show in pod description
- [ ] Unhealthy pods are restarted

**From Spec**: AC-3 (Health Checks)
**From Plan**: Section 6

---

### T-026: Test Full Application Functionality

**Description**: Verify all Phase III features work in Kubernetes.

**Preconditions**:
- T-024 complete
- Application accessible

**Steps**:
1. Access frontend via `minikube service frontend -n todo-app` or port-forward
2. Create new account
3. Login
4. Create task via UI
5. List tasks
6. Complete task
7. Delete task
8. Open chatbot
9. Create task via chat: "Add buy milk to my list"
10. List tasks via chat: "Show my tasks"
11. Complete task via chat: "Mark buy milk as done"

**Acceptance Criteria**:
- [ ] Account creation works
- [ ] Login works
- [ ] Task CRUD via UI works
- [ ] Chatbot opens
- [ ] Task CRUD via chatbot works
- [ ] Conversation persists across refreshes

**From Spec**: AC-1, AC-6
**From Plan**: Section 9

---

### T-027: Test HPA Scaling (Optional)

**Description**: Verify Horizontal Pod Autoscaler scales pods.

**Preconditions**:
- T-024 complete
- HPA applied

**Steps**:
1. `kubectl get hpa -n todo-app`
2. Generate load on backend (use hey or ab)
3. Watch pod count increase
4. Remove load
5. Watch pod count decrease (takes ~5 minutes)

**Acceptance Criteria**:
- [ ] HPA shows in kubectl output
- [ ] Pods scale up under load
- [ ] Pods scale down when idle
- [ ] Service remains available during scaling

**From Spec**: AC-7 (Scaling)
**From Plan**: Section 3.7

---

### T-028: Document Deployment Instructions

**Description**: Create deployment documentation in README.

**Preconditions**:
- All testing complete

**Artifacts to Create/Modify**:
- `docker/README.md` (create)

**Content**:
- Prerequisites (Docker, Minikube, Helm)
- Build instructions
- Docker Compose instructions
- Kubernetes deployment instructions
- Helm deployment instructions
- Troubleshooting section

**Acceptance Criteria**:
- [ ] Clear step-by-step instructions
- [ ] Commands copy-paste ready
- [ ] Troubleshooting for common issues
- [ ] Links to official docs

**From Spec**: UJ-1
**From Plan**: Section 7

---

## Task Status Tracking

| Task ID | Description | Status |
|---------|-------------|--------|
| T-001 | Docker Directory Structure | [ ] |
| T-002 | Frontend Dockerfile | [ ] |
| T-003 | Next.js Standalone Config | [ ] |
| T-004 | Backend Dockerfile | [ ] |
| T-005 | Docker Compose File | [ ] |
| T-006 | Test Docker Compose | [ ] |
| T-007 | Health Endpoint | [ ] |
| T-008 | Test Health Success | [ ] |
| T-009 | Test Health Failure | [ ] |
| T-010 | K8s Directory Structure | [ ] |
| T-011 | Namespace Manifest | [ ] |
| T-012 | Secrets Manifest | [ ] |
| T-013 | ConfigMap Manifest | [ ] |
| T-014 | Frontend Deployment | [ ] |
| T-015 | Frontend Service | [ ] |
| T-016 | Backend Deployment | [ ] |
| T-017 | Backend Service & HPA | [ ] |
| T-018 | Helm Chart Structure | [ ] |
| T-019 | Helm values.yaml | [ ] |
| T-020 | Helm Base Templates | [ ] |
| T-021 | Helm Frontend Templates | [ ] |
| T-022 | Helm Backend Templates | [ ] |
| T-023 | Test Helm Installation | [ ] |
| T-024 | Test K8s Deployment | [ ] |
| T-025 | Test Health Probes | [ ] |
| T-026 | Test Full Functionality | [ ] |
| T-027 | Test HPA Scaling | [ ] |
| T-028 | Document Deployment | [ ] |

---

**Tasks Version**: 1.0.0
**Created By**: Claude Code
**Next Step**: Begin implementation with T-001
