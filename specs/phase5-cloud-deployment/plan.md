# Phase V: Advanced Cloud Deployment - Technical Plan

**Feature**: Production Kubernetes & Event Streaming
**Phase**: Phase V - Cloud Deployment
**Spec Reference**: [spec.md](./spec.md)
**Created**: 2026-02-03

---

## 1. Implementation Strategy

### Approach
1. Add Kafka event producer to backend
2. Create Kafka/Redpanda Kubernetes manifests
3. Update Helm chart for production
4. Create CI/CD pipelines
5. Deploy to cloud Kubernetes

### Technology Choices

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Event Streaming | Redpanda | Kafka-compatible, lighter, easier to deploy |
| Cloud Provider | Azure AKS | Best Windows/enterprise support |
| CI/CD | GitHub Actions | Native GitHub integration |
| Ingress | NGINX | Industry standard, well-documented |
| TLS | cert-manager | Automated Let's Encrypt certs |

---

## 2. Kafka Event Service

### 2.1 Dependencies

Add to `requirements.txt`:
```
aiokafka>=0.10.0
```

### 2.2 Event Service Implementation

```python
# app/services/event_service.py
import json
import os
from datetime import datetime
from uuid import uuid4
from typing import Optional
from aiokafka import AIOKafkaProducer

class EventService:
    _instance: Optional['EventService'] = None
    _producer: Optional[AIOKafkaProducer] = None

    def __init__(self):
        self.bootstrap_servers = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
        self.enabled = os.getenv('KAFKA_ENABLED', 'false').lower() == 'true'

    @classmethod
    async def get_instance(cls) -> 'EventService':
        if cls._instance is None:
            cls._instance = EventService()
            if cls._instance.enabled:
                await cls._instance._connect()
        return cls._instance

    async def _connect(self):
        self._producer = AIOKafkaProducer(
            bootstrap_servers=self.bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8')
        )
        await self._producer.start()

    async def publish_task_event(
        self,
        event_type: str,
        task_id: int,
        user_id: str,
        payload: dict
    ):
        if not self.enabled or not self._producer:
            return

        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "payload": {
                "task_id": task_id,
                **payload
            }
        }

        try:
            await self._producer.send_and_wait("task-events", event)
        except Exception as e:
            # Log error but don't fail the request
            print(f"Failed to publish event: {e}")

    async def close(self):
        if self._producer:
            await self._producer.stop()
```

### 2.3 Integration with Task Service

```python
# In task_service.py - add event publishing
from app.services.event_service import EventService

class TaskService:
    async def create_task(self, title: str, description: str = "") -> Task:
        # ... existing code ...
        task = Task(...)
        self.session.add(task)
        self.session.commit()

        # Publish event
        event_service = await EventService.get_instance()
        await event_service.publish_task_event(
            "task.created",
            task.id,
            self.user_id,
            {"title": task.title, "description": task.description}
        )

        return task
```

---

## 3. Redpanda Kubernetes Deployment

### 3.1 Redpanda Helm Values

```yaml
# kafka/redpanda-values.yaml
statefulset:
  replicas: 3

resources:
  cpu:
    cores: 1
  memory:
    container:
      max: 2Gi

storage:
  persistentVolume:
    enabled: true
    size: 10Gi

external:
  enabled: false

auth:
  sasl:
    enabled: false

tls:
  enabled: false
```

### 3.2 Topic Configuration

```yaml
# kafka/kafka-topics.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: kafka-topics-init
  namespace: todo-app
data:
  create-topics.sh: |
    #!/bin/bash
    rpk topic create task-events --partitions 3 --replicas 3
    rpk topic create task-analytics --partitions 3 --replicas 3
```

---

## 4. Production Helm Values

```yaml
# helm/todo-app/values-production.yaml
# Production overrides for cloud deployment

frontend:
  replicaCount: 3
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "1000m"

backend:
  replicaCount: 3
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70
  resources:
    requests:
      memory: "512Mi"
      cpu: "250m"
    limits:
      memory: "1Gi"
      cpu: "1000m"

kafka:
  enabled: true
  bootstrapServers: "redpanda.todo-app.svc.cluster.local:9092"

ingress:
  enabled: true
  className: nginx
  annotations:
    cert-manager.io/cluster-issuer: letsencrypt-prod
  hosts:
    - host: todo.yourdomain.com
      paths:
        - path: /
          pathType: Prefix
          service: frontend
        - path: /api
          pathType: Prefix
          service: backend
  tls:
    - secretName: todo-tls
      hosts:
        - todo.yourdomain.com
```

---

## 5. CI/CD Pipelines

### 5.1 CI Pipeline

```yaml
# .github/workflows/ci.yaml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  backend-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        run: |
          cd phase2/backend
          pip install -r requirements.txt
          pip install pytest pytest-asyncio

      - name: Run tests
        run: |
          cd phase2/backend
          python -m pytest tests/ -v

  frontend-build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: frontend/package-lock.json

      - name: Install dependencies
        run: |
          cd frontend
          npm ci

      - name: Build
        run: |
          cd frontend
          npm run build

  docker-build:
    runs-on: ubuntu-latest
    needs: [backend-test, frontend-build]
    steps:
      - uses: actions/checkout@v4

      - name: Build backend image
        run: docker build -f docker/backend.Dockerfile -t todo-backend:${{ github.sha }} .

      - name: Build frontend image
        run: docker build -f docker/frontend.Dockerfile -t todo-frontend:${{ github.sha }} .
```

### 5.2 CD Pipeline

```yaml
# .github/workflows/deploy.yaml
name: Deploy

on:
  push:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}

jobs:
  build-and-push:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Log in to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push backend
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/backend.Dockerfile
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/backend:${{ github.sha }}

      - name: Build and push frontend
        uses: docker/build-push-action@v5
        with:
          context: .
          file: docker/frontend.Dockerfile
          push: true
          tags: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}/frontend:${{ github.sha }}

  deploy:
    needs: build-and-push
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up kubectl
        uses: azure/setup-kubectl@v3

      - name: Set up Helm
        uses: azure/setup-helm@v3

      - name: Configure kubectl
        run: |
          echo "${{ secrets.KUBE_CONFIG }}" | base64 -d > kubeconfig
          export KUBECONFIG=kubeconfig

      - name: Deploy with Helm
        run: |
          helm upgrade --install todo-app ./helm/todo-app \
            --namespace todo-app \
            --create-namespace \
            -f helm/todo-app/values-production.yaml \
            --set backend.image.tag=${{ github.sha }} \
            --set frontend.image.tag=${{ github.sha }} \
            --set secrets.databaseUrl=${{ secrets.DATABASE_URL }} \
            --set secrets.jwtSecret=${{ secrets.JWT_SECRET }} \
            --set secrets.geminiApiKey=${{ secrets.GEMINI_API_KEY }}
```

---

## 6. Deployment Steps

### Step 1: Local Validation (Minikube)
```bash
# Test everything works locally first
minikube start
helm install todo-app ./helm/todo-app -n todo-app --create-namespace
```

### Step 2: Create Cloud Cluster
```bash
# Azure AKS example
az aks create --resource-group todo-rg --name todo-aks --node-count 3
az aks get-credentials --resource-group todo-rg --name todo-aks
```

### Step 3: Deploy Redpanda
```bash
helm repo add redpanda https://charts.redpanda.com
helm install redpanda redpanda/redpanda -n todo-app -f kafka/redpanda-values.yaml
```

### Step 4: Deploy Application
```bash
helm upgrade --install todo-app ./helm/todo-app \
  -n todo-app \
  -f helm/todo-app/values-production.yaml
```

### Step 5: Configure DNS and TLS
```bash
# Install cert-manager
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.yaml

# Create ClusterIssuer for Let's Encrypt
kubectl apply -f k8s/cluster-issuer.yaml
```

---

## 7. Monitoring

### Health Checks
- Backend: `/health` endpoint
- Frontend: `/` endpoint
- Kafka: Redpanda admin API

### Logs
```bash
# View backend logs
kubectl logs -l app=backend -n todo-app -f

# View Kafka logs
kubectl logs -l app.kubernetes.io/name=redpanda -n todo-app
```

---

**Plan Version**: 1.0.0
**Next Step**: Create tasks.md
