# Phase IV: Kubernetes Deployment - Technical Plan

**Feature**: Containerization and Local Kubernetes Deployment
**Phase**: Phase IV - Docker & Kubernetes
**Status**: Draft
**Created**: 2026-01-26
**Updated**: 2026-01-26
**Spec Reference**: [spec.md](./spec.md)

---

## 1. Architecture Overview

### 1.1 System Architecture

```
                    [Minikube Cluster]
                          |
              +-----------+-----------+
              |                       |
         [Ingress/Service]       [kubectl-ai]
              |                       |
    +---------+---------+        [kagent]
    |         |         |
[Frontend] [Backend]  [MCP]
    |         |         |
    +----+----+----+----+
         |         |
    [ConfigMap] [Secret]
         |
  [External: Neon PostgreSQL]
```

### 1.2 Container Architecture

Each service runs in its own container with:
- Optimized base image (Alpine/Slim)
- Multi-stage builds for smaller images
- Non-root user for security
- Health check endpoints
- Environment-based configuration

### 1.3 Kubernetes Architecture

```
Namespace: todo-app
  |
  +-- Deployments
  |     +-- frontend (2 replicas)
  |     +-- backend (3 replicas, HPA)
  |     +-- mcp (2 replicas) [optional]
  |
  +-- Services
  |     +-- frontend (NodePort/LoadBalancer)
  |     +-- backend (ClusterIP)
  |     +-- mcp (ClusterIP) [optional]
  |
  +-- ConfigMaps
  |     +-- todo-config (API URLs, settings)
  |
  +-- Secrets
  |     +-- todo-secrets (DB, JWT, OpenAI)
  |
  +-- HPA
        +-- backend-hpa (2-10 replicas, 70% CPU)
```

---

## 2. Component Design

### 2.1 Frontend Container

**Base Image**: `node:20-alpine`

**Build Strategy**: Multi-stage
1. **Stage 1 (builder)**: Install deps, build Next.js
2. **Stage 2 (production)**: Copy built artifacts, run

**Environment Variables**:
- `NEXT_PUBLIC_API_URL` - Backend API URL

**Ports**: 3000

**Health Check**: `GET /` returns 200

### 2.2 Backend Container

**Base Image**: `python:3.13-slim`

**Build Strategy**: Single stage with UV
1. Install UV package manager
2. Copy pyproject.toml, sync dependencies
3. Copy application code
4. Run with Uvicorn

**Environment Variables**:
- `DATABASE_URL` - Neon PostgreSQL connection string
- `JWT_SECRET` - Token signing secret
- `OPENAI_API_KEY` - OpenAI API key
- `OPENAI_AGENT_MODEL` - Model name (gpt-4o)

**Ports**: 8000

**Health Check**: `GET /health` returns 200

### 2.3 MCP Container (Optional)

The MCP server can either:
1. Run as part of the backend container (recommended for simplicity)
2. Run as a separate container (for scalability)

**Decision**: Combine with backend for Phase IV. Separate in Phase V if needed.

---

## 3. Kubernetes Resources

### 3.1 Namespace

```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: todo-app
  labels:
    app.kubernetes.io/name: todo-app
    app.kubernetes.io/part-of: evolution-of-todo
```

### 3.2 Secrets

```yaml
apiVersion: v1
kind: Secret
metadata:
  name: todo-secrets
  namespace: todo-app
type: Opaque
stringData:
  database-url: <from-env>
  jwt-secret: <from-env>
  openai-api-key: <from-env>
```

### 3.3 ConfigMap

```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: todo-config
  namespace: todo-app
data:
  BACKEND_URL: "http://backend:8000"
  OPENAI_AGENT_MODEL: "gpt-4o"
```

### 3.4 Frontend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: frontend
  namespace: todo-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: frontend
  template:
    spec:
      containers:
      - name: frontend
        image: todo-frontend:latest
        ports:
        - containerPort: 3000
        env:
        - name: NEXT_PUBLIC_API_URL
          value: "http://backend:8000"
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

### 3.5 Backend Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: backend
  namespace: todo-app
spec:
  replicas: 3
  selector:
    matchLabels:
      app: backend
  template:
    spec:
      containers:
      - name: backend
        image: todo-backend:latest
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

### 3.6 Services

**Frontend Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: frontend
  namespace: todo-app
spec:
  type: NodePort
  selector:
    app: frontend
  ports:
  - port: 3000
    targetPort: 3000
    nodePort: 30300
```

**Backend Service**:
```yaml
apiVersion: v1
kind: Service
metadata:
  name: backend
  namespace: todo-app
spec:
  type: ClusterIP
  selector:
    app: backend
  ports:
  - port: 8000
    targetPort: 8000
```

### 3.7 Horizontal Pod Autoscaler

```yaml
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

---

## 4. Helm Chart Structure

### 4.1 Chart.yaml

```yaml
apiVersion: v2
name: todo-app
description: Evolution of Todo - Full Stack Application with AI Chatbot
version: 1.0.0
appVersion: "1.0.0"
keywords:
  - todo
  - fastapi
  - nextjs
  - kubernetes
maintainers:
  - name: Evolution of Todo Team
```

### 4.2 values.yaml

```yaml
# Namespace
namespace: todo-app

# Frontend Configuration
frontend:
  replicaCount: 2
  image:
    repository: todo-frontend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: NodePort
    port: 3000
    nodePort: 30300
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  probes:
    liveness:
      path: /
      initialDelaySeconds: 30
      periodSeconds: 10
    readiness:
      path: /
      initialDelaySeconds: 10
      periodSeconds: 5

# Backend Configuration
backend:
  replicaCount: 3
  image:
    repository: todo-backend
    tag: latest
    pullPolicy: IfNotPresent
  service:
    type: ClusterIP
    port: 8000
  resources:
    requests:
      memory: "256Mi"
      cpu: "100m"
    limits:
      memory: "512Mi"
      cpu: "500m"
  probes:
    liveness:
      path: /health
      initialDelaySeconds: 30
      periodSeconds: 10
    readiness:
      path: /health
      initialDelaySeconds: 10
      periodSeconds: 5
  autoscaling:
    enabled: true
    minReplicas: 2
    maxReplicas: 10
    targetCPUUtilizationPercentage: 70

# Configuration
config:
  backendUrl: "http://backend:8000"
  openaiModel: "gpt-4o"

# Secrets (to be provided at install time)
secrets:
  databaseUrl: ""
  jwtSecret: ""
  openaiApiKey: ""
```

### 4.3 Template Organization

```
templates/
  _helpers.tpl           # Common template helpers
  namespace.yaml         # Namespace definition
  secrets.yaml           # Secrets (from values)
  configmap.yaml         # ConfigMap (from values)
  frontend/
    deployment.yaml      # Frontend deployment
    service.yaml         # Frontend service
  backend/
    deployment.yaml      # Backend deployment
    service.yaml         # Backend service
    hpa.yaml            # Horizontal Pod Autoscaler
```

---

## 5. Docker Compose (Local Development)

```yaml
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
      - backend
    networks:
      - todo-network

  backend:
    build:
      context: ..
      dockerfile: docker/backend.Dockerfile
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=${DATABASE_URL}
      - JWT_SECRET=${JWT_SECRET}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - OPENAI_AGENT_MODEL=gpt-4o
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
```

---

## 6. Health Check Implementation

### 6.1 Backend Health Endpoint

Add to FastAPI `app/main.py`:

```python
from datetime import datetime
from sqlmodel import select

@app.get("/health")
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

### 6.2 Frontend Health

Next.js serves the root path `/` which returns 200 when healthy.

---

## 7. Development Workflow

### 7.1 Build Images

```bash
# From project root
cd hackaton2

# Build all images
docker build -f docker/frontend.Dockerfile -t todo-frontend:latest .
docker build -f docker/backend.Dockerfile -t todo-backend:latest .
```

### 7.2 Test with Docker Compose

```bash
# Create .env file with secrets
cp docker/.env.example docker/.env
# Edit docker/.env with real values

# Run locally
docker-compose -f docker/docker-compose.yml up
```

### 7.3 Deploy to Minikube

```bash
# Start Minikube
minikube start --driver=docker --cpus=4 --memory=8192

# Load images to Minikube
minikube image load todo-frontend:latest
minikube image load todo-backend:latest

# Deploy with kubectl
kubectl apply -f k8s/namespace.yaml
kubectl apply -f k8s/secrets.yaml  # Edit first!
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/frontend/
kubectl apply -f k8s/backend/

# OR deploy with Helm
helm install todo-app ./helm/todo-app \
  --namespace todo-app \
  --create-namespace \
  --set secrets.databaseUrl=$DATABASE_URL \
  --set secrets.jwtSecret=$JWT_SECRET \
  --set secrets.openaiApiKey=$OPENAI_API_KEY
```

### 7.4 Access Application

```bash
# Port forward
kubectl port-forward svc/frontend 3000:3000 -n todo-app

# OR use Minikube service
minikube service frontend -n todo-app

# OR use Minikube tunnel
minikube tunnel
```

---

## 8. Implementation Phases

### Phase A: Docker Foundation
1. Create docker directory structure
2. Create .dockerignore files
3. Create frontend.Dockerfile
4. Create backend.Dockerfile
5. Create docker-compose.yml
6. Test local Docker deployment

### Phase B: Health Endpoints
7. Add /health endpoint to backend
8. Test health endpoint returns correct JSON
9. Test health endpoint with database failure

### Phase C: Kubernetes Manifests
10. Create namespace.yaml
11. Create secrets.yaml (template)
12. Create configmap.yaml
13. Create frontend deployment and service
14. Create backend deployment and service
15. Create HPA for backend

### Phase D: Helm Chart
16. Create Chart.yaml
17. Create values.yaml
18. Create _helpers.tpl
19. Create templated manifests
20. Test Helm install/upgrade/uninstall

### Phase E: Testing & Validation
21. Test Docker Compose deployment
22. Test Kubernetes deployment
23. Test health probes
24. Test HPA scaling
25. Validate all Phase III features work

---

## 9. Verification Checklist

- [ ] Docker images build successfully
- [ ] Docker Compose runs all services
- [ ] Frontend accessible at localhost:3000
- [ ] Backend accessible at localhost:8000
- [ ] Health endpoint returns correct JSON
- [ ] Kubernetes manifests apply without errors
- [ ] All pods reach Running state
- [ ] Liveness probes passing
- [ ] Readiness probes passing
- [ ] Helm chart installs successfully
- [ ] Helm values override works
- [ ] HPA scales pods on load
- [ ] kubectl-ai responds to commands
- [ ] All Phase III features functional

---

## 10. Architectural Decisions

### AD-1: Combined Backend and MCP

**Decision**: Run MCP server as part of backend container (not separate).

**Rationale**:
- Simpler architecture for Phase IV
- MCP tools directly call backend services
- Fewer containers to manage
- Can be separated in Phase V if needed

### AD-2: External Database

**Decision**: Continue using external Neon PostgreSQL (no in-cluster database).

**Rationale**:
- Stateless services are easier to scale
- No PersistentVolumeClaims needed
- Database already set up from Phase II
- Production-like architecture

### AD-3: NodePort for Frontend

**Decision**: Use NodePort service for frontend (not LoadBalancer).

**Rationale**:
- Works with Minikube without cloud provider
- Simple to access with `minikube service`
- LoadBalancer requires tunnel or cloud

### AD-4: Helm for Deployment

**Decision**: Create Helm chart in addition to raw manifests.

**Rationale**:
- Industry standard for Kubernetes packages
- Easy to parameterize for different environments
- Required for Phase V cloud deployment
- Better than managing multiple YAML files

---

## 11. Security Considerations

1. **No secrets in images**: All secrets via Kubernetes Secrets
2. **Non-root containers**: Run as non-root user
3. **Resource limits**: Prevent container from consuming all resources
4. **Network isolation**: Services only exposed as needed
5. **Image scanning**: Consider adding in Phase V

---

## 12. References

- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [Kubernetes Deployments](https://kubernetes.io/docs/concepts/workloads/controllers/deployment/)
- [Kubernetes Probes](https://kubernetes.io/docs/tasks/configure-pod-container/configure-liveness-readiness-startup-probes/)
- [Helm Charts](https://helm.sh/docs/topics/charts/)
- [Minikube Tutorial](https://minikube.sigs.k8s.io/docs/start/)

---

**Plan Version**: 1.0.0
**Created By**: Claude Code
**Next Step**: Create tasks.md (BREAKDOWN into atomic tasks)
