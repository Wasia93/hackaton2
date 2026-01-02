# Phase V Cloud-Native Deployment Agent

## Purpose
Expert agent for deploying the application to cloud platforms with event-driven architecture using Kafka and Dapr (Phase V).

## Responsibilities
- Deploy to cloud Kubernetes (Azure AKS / Google GKE / Oracle OKE)
- Implement event-driven architecture with Kafka
- Integrate Dapr for distributed application runtime
- Set up CI/CD pipelines with GitHub Actions
- Configure observability and monitoring
- Implement advanced features (reminders, notifications, event sourcing)

## Technology Stack

### Cloud Platforms
- **Azure**: AKS (Azure Kubernetes Service)
- **Google Cloud**: GKE (Google Kubernetes Engine)
- **Oracle Cloud**: OKE (Oracle Container Engine for Kubernetes)

### Event Streaming
- **Kafka**: Self-hosted via Strimzi operator OR Redpanda Cloud
- **Topics**: task-events, reminders, task-updates

### Distributed Runtime
- **Dapr**: Sidecar architecture
  - Pub/Sub (Kafka)
  - State Management (PostgreSQL)
  - Bindings (Jobs API for reminders)
  - Secrets (Kubernetes secrets)
  - Service Invocation

### CI/CD
- **GitHub Actions**: Build, test, deploy pipelines
- **Container Registry**: Docker Hub, Azure ACR, Google GCR
- **GitOps**: ArgoCD (optional)

### Observability
- **Logs**: Structured JSON logs
- **Metrics**: Prometheus + Grafana
- **Tracing**: Jaeger or Zipkin (distributed tracing)
- **Alerts**: Alertmanager

## Project Structure
```
├── .github/
│   └── workflows/
│       ├── build.yml          # Build and test
│       ├── deploy-staging.yml # Deploy to staging
│       └── deploy-prod.yml    # Deploy to production
├── dapr/
│   ├── components/
│   │   ├── pubsub-kafka.yaml
│   │   ├── statestore-postgres.yaml
│   │   ├── binding-jobs.yaml
│   │   └── secretstore-k8s.yaml
│   └── config/
│       └── dapr-config.yaml
├── kafka/
│   ├── strimzi-operator.yaml
│   ├── kafka-cluster.yaml
│   └── topics/
│       ├── task-events.yaml
│       ├── reminders.yaml
│       └── task-updates.yaml
├── monitoring/
│   ├── prometheus/
│   ├── grafana/
│   └── alertmanager/
└── specs/phase5-cloud/  # Specifications (to be created)
```

## Event-Driven Architecture

### Kafka Topics

#### task-events
All CRUD operations publish events here.
```json
{
  "event_type": "created" | "updated" | "completed" | "deleted",
  "task_id": 123,
  "user_id": "user-uuid",
  "timestamp": "2025-01-02T10:00:00Z",
  "task_data": {
    "id": 123,
    "title": "Buy groceries",
    "description": "Milk, bread, eggs",
    "completed": false,
    "created_at": "2025-01-02T10:00:00Z"
  }
}
```

#### reminders
Scheduled reminder triggers.
```json
{
  "task_id": 123,
  "user_id": "user-uuid",
  "due_date": "2025-01-03T09:00:00Z",
  "reminder_type": "email" | "push",
  "sent": false
}
```

#### task-updates
Real-time updates for frontend synchronization.
```json
{
  "user_id": "user-uuid",
  "task_id": 123,
  "action": "created" | "updated" | "deleted",
  "timestamp": "2025-01-02T10:00:00Z"
}
```

## Dapr Components

### Pub/Sub (Kafka)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: pubsub
  namespace: todo-app
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-broker:9092"
  - name: authType
    value: "none"
  - name: consumerGroup
    value: "todo-group"
```

### State Store (PostgreSQL)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: statestore
  namespace: todo-app
spec:
  type: state.postgresql
  version: v1
  metadata:
  - name: connectionString
    secretKeyRef:
      name: todo-secrets
      key: database-url
```

### Bindings (Dapr Jobs API)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: reminders-job
  namespace: todo-app
spec:
  type: bindings.cron
  version: v1
  metadata:
  - name: schedule
    value: "@every 1m"  # Check for due reminders every minute
```

### Secrets (Kubernetes)
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: secretstore
  namespace: todo-app
spec:
  type: secretstores.kubernetes
  version: v1
  metadata:
  - name: vaultName
    value: "todo-secrets"
```

## Backend Changes for Event-Driven

### Publish Events on CRUD Operations
```python
from dapr.clients import DaprClient

async def create_task(task: TaskCreate, user_id: str):
    # 1. Save to database
    task = db.create_task(task, user_id)

    # 2. Publish event to Kafka via Dapr
    with DaprClient() as client:
        client.publish_event(
            pubsub_name='pubsub',
            topic_name='task-events',
            data={
                'event_type': 'created',
                'task_id': task.id,
                'user_id': user_id,
                'timestamp': datetime.now().isoformat(),
                'task_data': task.dict()
            }
        )

    return task
```

### Subscribe to Events
```python
from dapr.ext.fastapi import DaprApp

app = FastAPI()
dapr_app = DaprApp(app)

@dapr_app.subscribe(pubsub='pubsub', topic='task-events')
async def task_event_handler(event_data: dict):
    # Process event (e.g., send notifications, update analytics)
    logger.info(f"Task event: {event_data['event_type']} for task {event_data['task_id']}")

    # Example: Send notification if task completed
    if event_data['event_type'] == 'completed':
        await send_notification(event_data['user_id'], f"Task {event_data['task_id']} completed!")
```

### Reminder Service
```python
@dapr_app.subscribe(pubsub='pubsub', topic='reminders')
async def reminder_handler(reminder: dict):
    task_id = reminder['task_id']
    user_id = reminder['user_id']

    # Send reminder notification
    await send_reminder_notification(user_id, task_id)

    # Mark reminder as sent
    with DaprClient() as client:
        client.save_state(
            store_name='statestore',
            key=f"reminder-{task_id}",
            value={'sent': True, 'sent_at': datetime.now().isoformat()}
        )
```

## CI/CD Pipeline

### GitHub Actions Workflow
```yaml
name: Build and Deploy

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build Frontend
        run: |
          cd frontend
          npm install
          npm run build

      - name: Build Backend
        run: |
          cd backend
          uv sync
          uv run pytest

      - name: Build Docker Images
        run: |
          docker build -f docker/frontend.Dockerfile -t ${{ secrets.REGISTRY }}/frontend:${{ github.sha }} .
          docker build -f docker/backend.Dockerfile -t ${{ secrets.REGISTRY }}/backend:${{ github.sha }} .

      - name: Push to Registry
        run: |
          echo ${{ secrets.REGISTRY_PASSWORD }} | docker login -u ${{ secrets.REGISTRY_USERNAME }} --password-stdin
          docker push ${{ secrets.REGISTRY }}/frontend:${{ github.sha }}
          docker push ${{ secrets.REGISTRY }}/backend:${{ github.sha }}

  deploy:
    needs: build
    runs-on: ubuntu-latest
    steps:
      - name: Deploy to Kubernetes
        run: |
          kubectl set image deployment/frontend frontend=${{ secrets.REGISTRY }}/frontend:${{ github.sha }} -n todo-app
          kubectl set image deployment/backend backend=${{ secrets.REGISTRY }}/backend:${{ github.sha }} -n todo-app
```

## Cloud Deployment Steps

### Azure AKS
```bash
# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create --resource-group todo-rg --name todo-aks --node-count 3 --enable-managed-identity

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks

# Install Dapr on AKS
dapr init -k

# Install Strimzi (Kafka operator)
kubectl create namespace kafka
kubectl apply -f kafka/strimzi-operator.yaml -n kafka
kubectl apply -f kafka/kafka-cluster.yaml -n kafka

# Deploy application
helm upgrade --install todo-app ./helm/todo-app -n todo-app --create-namespace
```

### Google GKE
```bash
# Create cluster
gcloud container clusters create todo-gke --num-nodes=3 --zone=us-central1-a

# Get credentials
gcloud container clusters get-credentials todo-gke --zone=us-central1-a

# Install Dapr
dapr init -k

# Deploy
helm upgrade --install todo-app ./helm/todo-app -n todo-app --create-namespace
```

### Oracle OKE
```bash
# Create cluster via Oracle Cloud Console or CLI
oci ce cluster create --name todo-oke ...

# Get kubeconfig
oci ce cluster create-kubeconfig --cluster-id <cluster-id>

# Install Dapr
dapr init -k

# Deploy
helm upgrade --install todo-app ./helm/todo-app -n todo-app --create-namespace
```

## Monitoring and Observability

### Prometheus Metrics
```python
from prometheus_client import Counter, Histogram

task_created = Counter('tasks_created_total', 'Total tasks created')
task_completed = Counter('tasks_completed_total', 'Total tasks completed')
api_latency = Histogram('api_request_duration_seconds', 'API request latency')

@api_latency.time()
async def create_task(...):
    task = await create_task_logic(...)
    task_created.inc()
    return task
```

### Structured Logging
```python
import structlog

logger = structlog.get_logger()

logger.info("task_created", task_id=task.id, user_id=user_id, title=task.title)
```

### Distributed Tracing
```python
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

tracer = trace.get_tracer(__name__)

FastAPIInstrumentor.instrument_app(app)

@app.get("/tasks")
async def list_tasks():
    with tracer.start_as_current_span("list_tasks"):
        tasks = await fetch_tasks()
        return tasks
```

## Advanced Features (Phase V Only)

### Task Reminders
- Due date field added to tasks
- Cron job checks for upcoming due dates
- Publishes to `reminders` topic
- Notification service sends email/push

### Real-Time Updates
- WebSocket connection for live task updates
- Subscribe to `task-updates` topic
- Push updates to connected clients

### Event Sourcing (Optional)
- Store all task events in event store
- Rebuild task state from events
- Audit trail of all changes

## Success Criteria
- [ ] Deployed to cloud Kubernetes (AKS/GKE/OKE)
- [ ] Kafka cluster running (Strimzi or Redpanda)
- [ ] Dapr installed and configured
- [ ] All Dapr components working (Pub/Sub, State, Secrets)
- [ ] Events published on all CRUD operations
- [ ] Event subscribers processing events
- [ ] CI/CD pipeline deploying automatically
- [ ] Monitoring dashboards showing metrics
- [ ] Distributed tracing enabled
- [ ] Reminder service functional
- [ ] Auto-scaling configured
- [ ] Production-ready (HTTPS, secrets management)

## Performance & Scalability
- API response: < 200ms p95
- Event processing: < 1 second
- Kafka throughput: > 1000 events/sec
- Auto-scale: 3-20 pods based on CPU/memory
- Database connection pooling
- Caching for frequently accessed data (optional)

## Security Hardening
- TLS/SSL for all communication
- Kubernetes Network Policies
- Pod Security Policies
- Secrets in Kubernetes secrets (not ConfigMaps)
- Image scanning (Trivy, Snyk)
- RBAC for Kubernetes access

## Related Agents
- `phase4-kubernetes.md` - Kubernetes foundation
- `deployment.md` - Deployment strategies
- `testing.md` - Testing event-driven systems

## Commands to Use
- `/sp.specify` - Create Phase V spec
- `/sp.plan` - Design event-driven architecture
- `/sp.tasks` - Break down cloud deployment tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record
- `/sp.adr` - Document cloud architecture decisions

---

**Remember**: Phase V is the final evolution - cloud-native, event-driven, production-ready. This completes the "Evolution of Todo" journey!
