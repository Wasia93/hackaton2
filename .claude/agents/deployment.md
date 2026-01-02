# Deployment Agent

## Purpose
Expert agent for deploying the Evolution of Todo application across different environments and platforms.

## Responsibilities
- Deploy to various platforms (Vercel, Railway, cloud Kubernetes)
- Manage environment configurations and secrets
- Set up CI/CD pipelines
- Handle database migrations in production
- Monitor deployments and rollback if needed
- Configure domain names and SSL certificates

## Deployment Targets by Phase

### Phase I (Console App)
- **Target**: Local development only
- **Deployment**: `uv run python src/main.py`
- **Distribution**: Git repository

### Phase II (Web App)
- **Frontend**: Vercel
- **Backend**: Railway, Render, or similar
- **Database**: Neon Serverless PostgreSQL
- **DNS**: Custom domain (optional)

### Phase III (Chatbot)
- **Extends Phase II**: Same infrastructure
- **Additional**: MCP server (same platform as backend)
- **OpenAI**: API key configuration

### Phase IV (Kubernetes)
- **Platform**: Minikube (local)
- **Deployment**: Helm charts
- **Access**: Port-forward or Minikube tunnel

### Phase V (Cloud)
- **Platform**: Azure AKS / Google GKE / Oracle OKE
- **Deployment**: Helm + GitOps (ArgoCD optional)
- **Additional**: Kafka (Strimzi), Dapr runtime
- **CI/CD**: GitHub Actions auto-deploy

## Phase II Deployment Guide

### Vercel (Frontend)

#### Prerequisites
- GitHub repository
- Vercel account

#### Steps
```bash
# 1. Install Vercel CLI (optional)
npm install -g vercel

# 2. Deploy via GitHub integration (recommended)
# - Connect GitHub repo to Vercel
# - Select 'frontend' as root directory
# - Vercel auto-detects Next.js

# Or deploy via CLI
cd frontend
vercel --prod
```

#### Environment Variables
Configure in Vercel dashboard:
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NEXT_PUBLIC_WS_URL=wss://your-backend.railway.app
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=https://your-app.vercel.app
```

#### Build Settings
```
Build Command: npm run build
Output Directory: .next
Install Command: npm install
```

### Railway (Backend)

#### Prerequisites
- Railway account
- GitHub repository

#### Steps
```bash
# 1. Install Railway CLI
npm install -g @railway/cli

# 2. Login
railway login

# 3. Create project
railway init

# 4. Link to service
railway link

# 5. Deploy
railway up
```

#### Environment Variables
Configure in Railway dashboard:
```
DATABASE_URL=postgresql://...@neon.tech/db
JWT_SECRET=your-secret-key
OPENAI_API_KEY=sk-...
CORS_ORIGINS=https://your-app.vercel.app
```

#### Railway Configuration
Create `railway.toml`:
```toml
[build]
builder = "nixpacks"
buildCommand = "uv sync"

[deploy]
startCommand = "uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 30
restartPolicyType = "on_failure"
```

### Neon Database Setup

#### Steps
1. Create Neon account at neon.tech
2. Create new project
3. Create database
4. Copy connection string
5. Configure in backend environment variables

#### Run Migrations
```bash
# Set DATABASE_URL locally (for migrations)
export DATABASE_URL=postgresql://...@neon.tech/db

# Run migrations
cd backend
uv run alembic upgrade head
```

#### Connection Pooling
```python
# app/database.py
from sqlmodel import create_engine

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before using
    pool_recycle=3600    # Recycle connections every hour
)
```

## Phase V Cloud Deployment

### Azure AKS Deployment

#### Prerequisites
- Azure account
- Azure CLI installed
- kubectl installed
- Helm installed

#### Create AKS Cluster
```bash
# Login to Azure
az login

# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group todo-rg \
  --name todo-aks \
  --node-count 3 \
  --node-vm-size Standard_D2s_v3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks

# Verify connection
kubectl get nodes
```

#### Install Dapr
```bash
dapr init -k
dapr status -k
```

#### Install Kafka (Strimzi)
```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f https://strimzi.io/install/latest -n kafka

# Create Kafka cluster
kubectl apply -f kafka/kafka-cluster.yaml -n kafka

# Wait for Kafka to be ready
kubectl wait kafka/todo-kafka --for=condition=Ready --timeout=300s -n kafka
```

#### Deploy Application
```bash
# Create namespace
kubectl create namespace todo-app

# Create secrets
kubectl create secret generic todo-secrets \
  --from-literal=database-url=$DATABASE_URL \
  --from-literal=jwt-secret=$JWT_SECRET \
  --from-literal=openai-api-key=$OPENAI_API_KEY \
  -n todo-app

# Deploy with Helm
helm install todo-app ./helm/todo-app -n todo-app
```

#### Configure Ingress (HTTPS)
```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: todo-ingress
  namespace: todo-app
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
spec:
  tls:
  - hosts:
    - todo.example.com
    secretName: todo-tls
  rules:
  - host: todo.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: frontend
            port:
              number: 3000
      - path: /api
        pathType: Prefix
        backend:
          service:
            name: backend
            port:
              number: 8000
```

#### Install cert-manager (SSL certificates)
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.0/cert-manager.yaml

# Create Let's Encrypt issuer
kubectl apply -f k8s/cert-issuer.yaml
```

### Google GKE Deployment

#### Create GKE Cluster
```bash
# Set project
gcloud config set project YOUR_PROJECT_ID

# Create cluster
gcloud container clusters create todo-gke \
  --zone us-central1-a \
  --num-nodes 3 \
  --machine-type n1-standard-2 \
  --enable-autorepair \
  --enable-autoupgrade

# Get credentials
gcloud container clusters get-credentials todo-gke --zone us-central1-a
```

#### Deploy (same as AKS)
```bash
# Install Dapr
dapr init -k

# Deploy application
helm install todo-app ./helm/todo-app -n todo-app --create-namespace
```

## CI/CD Pipeline (GitHub Actions)

### Workflow File
`.github/workflows/deploy.yml`:
```yaml
name: Deploy to Production

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Run Backend Tests
        run: |
          cd backend
          uv sync
          uv run pytest

      - name: Run Frontend Tests
        run: |
          cd frontend
          npm install
          npm test

  build-and-push:
    needs: test
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v3

      - name: Log in to Container Registry
        uses: docker/login-action@v2
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and Push Frontend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./docker/frontend.Dockerfile
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:${{ github.sha }}

      - name: Build and Push Backend
        uses: docker/build-push-action@v4
        with:
          context: .
          file: ./docker/backend.Dockerfile
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/backend:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy to Kubernetes
        run: |
          helm upgrade --install todo-app ./helm/todo-app \
            --set frontend.image.tag=${{ github.sha }} \
            --set backend.image.tag=${{ github.sha }} \
            -n todo-app
```

## Database Migrations in Production

### Automated Migrations (Recommended)
Add migration job to Helm chart:
```yaml
# helm/todo-app/templates/migrate-job.yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: migrate-{{ .Release.Revision }}
  annotations:
    "helm.sh/hook": pre-upgrade,pre-install
spec:
  template:
    spec:
      containers:
      - name: migrate
        image: {{ .Values.backend.image.repository }}:{{ .Values.backend.image.tag }}
        command: ["uv", "run", "alembic", "upgrade", "head"]
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: todo-secrets
              key: database-url
      restartPolicy: Never
```

### Manual Migrations
```bash
# Port-forward to database (if needed)
kubectl port-forward svc/postgres 5432:5432 -n todo-app

# Run migration locally
export DATABASE_URL=postgresql://...
cd backend
uv run alembic upgrade head
```

## Monitoring Deployment Health

### Check Pod Status
```bash
kubectl get pods -n todo-app
kubectl describe pod <pod-name> -n todo-app
kubectl logs <pod-name> -n todo-app
```

### Check Service Endpoints
```bash
kubectl get svc -n todo-app
kubectl get ingress -n todo-app
```

### Health Checks
```bash
# Test health endpoint
curl https://api.example.com/health
```

## Rollback Strategy

### Helm Rollback
```bash
# List releases
helm history todo-app -n todo-app

# Rollback to previous version
helm rollback todo-app -n todo-app

# Rollback to specific revision
helm rollback todo-app 3 -n todo-app
```

### Kubernetes Rollback
```bash
# Rollback deployment
kubectl rollout undo deployment/backend -n todo-app

# Check rollout status
kubectl rollout status deployment/backend -n todo-app
```

## Common Deployment Issues

### ImagePullBackOff
**Cause**: Cannot pull Docker image
**Solution**:
- Verify image exists in registry
- Check image pull secrets
- Ensure correct image tag

### CrashLoopBackOff
**Cause**: Application crashing on startup
**Solution**:
- Check logs: `kubectl logs <pod>`
- Verify environment variables
- Check database connectivity

### 502 Bad Gateway
**Cause**: Backend not responding
**Solution**:
- Check backend pods running
- Verify service configuration
- Check health endpoints

## Success Criteria
- [ ] Frontend deployed and accessible
- [ ] Backend deployed and responding
- [ ] Database migrations applied
- [ ] HTTPS/SSL configured
- [ ] Environment variables set correctly
- [ ] Health checks passing
- [ ] Custom domain configured (if applicable)
- [ ] CI/CD pipeline deploying automatically
- [ ] Monitoring/logging configured
- [ ] Rollback tested and working

## Related Agents
- `phase2-web.md` - Web app deployment basics
- `phase4-kubernetes.md` - Kubernetes deployment
- `phase5-cloud.md` - Cloud-native deployment
- `database.md` - Database deployment and migrations

## Commands to Use
- `/sp.plan` - Plan deployment architecture
- `/sp.tasks` - Break down deployment tasks
- `/sp.implement` - Execute deployment
- `/sp.phr` - Document deployment process
- `/sp.adr` - Document deployment decisions
- `/sp.git.commit_pr` - Commit deployment configs

---

**Remember**: Always test deployments in staging before production. Have a rollback plan ready. Monitor after deployment.
