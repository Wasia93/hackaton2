# Phase V: Advanced Cloud Deployment - Tasks

**Feature**: Production Kubernetes & Event Streaming
**Phase**: Phase V - Cloud Deployment
**Status**: Ready for Implementation
**Created**: 2026-02-03

---

## Task Summary

| Phase | Tasks | Description |
|-------|-------|-------------|
| A | T-001 to T-003 | Kafka Event Service |
| B | T-004 to T-006 | Kafka/Redpanda Manifests |
| C | T-007 to T-009 | CI/CD Pipelines |
| D | T-010 to T-012 | Production Helm Config |
| E | T-013 to T-015 | Cloud Deployment |

**Total Tasks**: 15

---

## Phase A: Kafka Event Service

### T-001: Add Kafka Dependencies
- Add `aiokafka>=0.10.0` to requirements.txt
- [ ] DONE

### T-002: Create Event Service
- File: `phase2/backend/app/services/event_service.py`
- Kafka producer with async publishing
- [ ] DONE

### T-003: Integrate with Task Service
- Publish events on create, update, delete, complete
- [ ] DONE

---

## Phase B: Kafka/Redpanda Manifests

### T-004: Create Kafka Directory
- Directory: `kafka/`
- [ ] DONE

### T-005: Create Redpanda Values
- File: `kafka/redpanda-values.yaml`
- [ ] DONE

### T-006: Create Topic Init Script
- File: `kafka/kafka-topics.yaml`
- [ ] DONE

---

## Phase C: CI/CD Pipelines

### T-007: Create CI Workflow
- File: `.github/workflows/ci.yaml`
- Backend tests, frontend build, Docker build
- [ ] DONE

### T-008: Create Deploy Workflow
- File: `.github/workflows/deploy.yaml`
- Build, push to registry, deploy with Helm
- [ ] DONE

### T-009: Create Dependabot Config
- File: `.github/dependabot.yml`
- Auto-update dependencies
- [ ] DONE

---

## Phase D: Production Helm Config

### T-010: Create Production Values
- File: `helm/todo-app/values-production.yaml`
- [ ] DONE

### T-011: Add Ingress Template
- File: `helm/todo-app/templates/ingress.yaml`
- [ ] DONE

### T-012: Update Backend Deployment for Kafka
- Add Kafka env vars to Helm template
- [ ] DONE

---

## Phase E: Cloud Deployment

### T-013: Document Cloud Setup
- File: `CLOUD_DEPLOYMENT.md`
- [ ] DONE

### T-014: Create Cluster Issuer for TLS
- File: `k8s/cluster-issuer.yaml`
- [ ] DONE

### T-015: Test Local Deployment
- Verify everything works on Minikube
- [ ] DONE

---

## Implementation Status

| Task | Status |
|------|--------|
| T-001 | Pending |
| T-002 | Pending |
| T-003 | Pending |
| T-004 | Pending |
| T-005 | Pending |
| T-006 | Pending |
| T-007 | Pending |
| T-008 | Pending |
| T-009 | Pending |
| T-010 | Pending |
| T-011 | Pending |
| T-012 | Pending |
| T-013 | Pending |
| T-014 | Pending |
| T-015 | Pending |

---

**Tasks Version**: 1.0.0
