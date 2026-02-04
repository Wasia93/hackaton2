# Phase V: Advanced Cloud Deployment - Specification

**Feature**: Production Kubernetes & Event Streaming
**Phase**: Phase V - Cloud Deployment
**Status**: Ready for Implementation
**Created**: 2026-02-03
**Updated**: 2026-02-03

---

## 1. Overview

Deploy the Todo application to production-grade Kubernetes on cloud providers (Azure AKS, Google GKE, or Oracle OKE) with Kafka/Redpanda event streaming for real-time task updates and analytics.

### Purpose
- Deploy to production Kubernetes cluster
- Implement event-driven architecture with Kafka
- Enable real-time task notifications
- Support horizontal scaling in cloud
- Demonstrate enterprise-grade deployment

### Deployment Flow
1. **Local Validation**: Test on Minikube (Phase 4)
2. **Cloud Setup**: Provision AKS/GKE/OKE cluster
3. **Kafka Integration**: Deploy Kafka or use Redpanda Cloud
4. **Application Deployment**: Deploy with Helm
5. **Production Validation**: End-to-end testing

---

## 2. Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                     Cloud Kubernetes (AKS/GKE/OKE)              │
├─────────────────────────────────────────────────────────────────┤
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────────┐  │
│  │   Frontend   │    │   Backend    │    │  Kafka/Redpanda  │  │
│  │   (Next.js)  │───▶│  (FastAPI)   │───▶│   Event Stream   │  │
│  │   3 replicas │    │  3-10 (HPA)  │    │   3 brokers      │  │
│  └──────────────┘    └──────────────┘    └──────────────────┘  │
│         │                   │                     │             │
│         │                   ▼                     ▼             │
│         │           ┌──────────────┐    ┌──────────────────┐   │
│         │           │    Neon      │    │   Event Consumer │   │
│         │           │  PostgreSQL  │    │   (Analytics)    │   │
│         │           └──────────────┘    └──────────────────┘   │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Ingress Controller (NGINX)                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌──────────────────┐
                    │   Load Balancer  │
                    │   (Cloud LB)     │
                    └──────────────────┘
```

---

## 3. Functional Requirements

### FR-1: Cloud Kubernetes Deployment

**Priority**: CRITICAL

**Supported Providers**:
- Azure Kubernetes Service (AKS)
- Google Kubernetes Engine (GKE)
- Oracle Container Engine (OKE)

**Requirements**:
- Production-grade cluster with 3+ nodes
- Auto-scaling node pools
- Private cluster option
- RBAC enabled
- Network policies
- Managed control plane

### FR-2: Kafka/Redpanda Event Streaming

**Priority**: HIGH

**Options**:
1. **Self-managed Kafka** in Kubernetes (Strimzi operator)
2. **Redpanda** in Kubernetes (lighter weight)
3. **Redpanda Cloud** (managed service)
4. **Confluent Cloud** (managed Kafka)

**Event Topics**:
- `task.created` - New task events
- `task.updated` - Task modification events
- `task.completed` - Task completion events
- `task.deleted` - Task deletion events

**Event Schema**:
```json
{
  "event_id": "uuid",
  "event_type": "task.created",
  "timestamp": "2026-02-03T10:00:00Z",
  "user_id": "user-uuid",
  "payload": {
    "task_id": 1,
    "title": "Buy groceries",
    "completed": false
  }
}
```

### FR-3: Event Producer (Backend)

**Priority**: HIGH

**Requirements**:
- Publish events on task CRUD operations
- Async event publishing (non-blocking)
- Retry logic for failed publishes
- Event schema validation

**Implementation**:
```python
# app/services/event_service.py
from aiokafka import AIOKafkaProducer

class EventService:
    async def publish_task_event(self, event_type: str, task: Task, user_id: str):
        event = {
            "event_id": str(uuid4()),
            "event_type": event_type,
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "user_id": user_id,
            "payload": task.dict()
        }
        await self.producer.send("task-events", json.dumps(event).encode())
```

### FR-4: Event Consumer (Analytics)

**Priority**: MEDIUM

**Requirements**:
- Consume events from Kafka topics
- Process task analytics (completion rates, trends)
- Store aggregated metrics
- Optional: Real-time dashboard updates

### FR-5: Ingress and TLS

**Priority**: HIGH

**Requirements**:
- NGINX Ingress Controller
- TLS termination with cert-manager
- Let's Encrypt certificates
- Custom domain support

### FR-6: CI/CD Integration

**Priority**: HIGH

**Requirements**:
- GitHub Actions for deployment
- Automated image builds
- Helm upgrade on merge to main
- Environment-specific configurations

---

## 4. Cloud Provider Setup

### Option A: Azure AKS

```bash
# Create resource group
az group create --name todo-rg --location eastus

# Create AKS cluster
az aks create \
  --resource-group todo-rg \
  --name todo-aks \
  --node-count 3 \
  --enable-managed-identity \
  --generate-ssh-keys

# Get credentials
az aks get-credentials --resource-group todo-rg --name todo-aks
```

### Option B: Google GKE

```bash
# Create GKE cluster
gcloud container clusters create todo-gke \
  --zone us-central1-a \
  --num-nodes 3 \
  --enable-autoscaling \
  --min-nodes 2 \
  --max-nodes 10

# Get credentials
gcloud container clusters get-credentials todo-gke --zone us-central1-a
```

### Option C: Oracle OKE

```bash
# Use OCI CLI or Console to create cluster
oci ce cluster create \
  --compartment-id <compartment-ocid> \
  --name todo-oke \
  --kubernetes-version v1.28.0
```

---

## 5. Kafka Deployment Options

### Option 1: Strimzi (Kafka in Kubernetes)

```bash
# Install Strimzi operator
kubectl create namespace kafka
kubectl apply -f 'https://strimzi.io/install/latest?namespace=kafka'

# Create Kafka cluster
kubectl apply -f kafka/kafka-cluster.yaml
```

### Option 2: Redpanda (Lightweight)

```bash
# Install Redpanda operator
helm repo add redpanda https://charts.redpanda.com
helm install redpanda redpanda/redpanda \
  --namespace redpanda \
  --create-namespace
```

### Option 3: Redpanda Cloud (Managed)

1. Create account at https://cloud.redpanda.com
2. Create cluster
3. Get bootstrap servers and credentials
4. Configure in Kubernetes secrets

---

## 6. Acceptance Criteria

### AC-1: Cloud Cluster
- [ ] Kubernetes cluster running in cloud
- [ ] Nodes auto-scaling functional
- [ ] kubectl access working

### AC-2: Application Deployment
- [ ] All pods Running in cloud
- [ ] Services accessible via Ingress
- [ ] TLS certificates valid

### AC-3: Kafka Integration
- [ ] Kafka/Redpanda cluster running
- [ ] Events published on task changes
- [ ] Events consumed successfully

### AC-4: Production Readiness
- [ ] Horizontal Pod Autoscaler working
- [ ] Health checks passing
- [ ] Logs accessible
- [ ] Monitoring enabled

---

## 7. Files to Create

```
hackaton2/
├── kafka/
│   ├── kafka-cluster.yaml      # Strimzi Kafka cluster
│   ├── kafka-topics.yaml       # Topic definitions
│   └── redpanda-values.yaml    # Redpanda Helm values
├── phase2/backend/
│   └── app/
│       └── services/
│           └── event_service.py  # Kafka producer
├── helm/todo-app/
│   └── values-production.yaml    # Production overrides
├── .github/workflows/
│   ├── ci.yaml                  # CI pipeline
│   └── deploy.yaml              # CD pipeline
└── specs/phase5-cloud-deployment/
    ├── spec.md                  # This file
    ├── plan.md                  # Architecture plan
    └── tasks.md                 # Task breakdown
```

---

## 8. Out of Scope

- Multi-region deployment
- Service mesh (Istio)
- Advanced monitoring (Prometheus/Grafana)
- Database migration from Neon
- Blue-green deployments

---

## 9. Success Criteria

Phase V is successful when:
- Application running in cloud Kubernetes
- Kafka events flowing on task operations
- Auto-scaling working under load
- TLS enabled with valid certificates
- CI/CD pipeline deploying automatically

---

**Spec Version**: 1.0.0
**Next Step**: Create plan.md
