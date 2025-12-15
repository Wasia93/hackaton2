# AGENTS.md

## Purpose

This project uses **Spec-Driven Development (SDD)** — a workflow where **no agent is allowed to write code until the specification is complete and approved**.

All AI agents (Claude, Copilot, Gemini, local LLMs, etc.) must follow the **Spec-Kit lifecycle**:

> **Specify → Plan → Tasks → Implement**

This prevents "vibe coding," ensures alignment across agents, and guarantees that every implementation step maps back to an explicit requirement.

---

## How Agents Must Work

Every agent in this project MUST obey these rules:

1. **Never generate code without a referenced Task ID.**
2. **Never modify architecture without updating the plan.**
3. **Never propose features without updating the specification (WHAT).**
4. **Never change approach without updating the constitution (Principles).**
5. **Every code file must contain a comment linking it to the Task and Spec sections.**

If an agent cannot find the required spec, it must **stop and request it**, not improvise.

---

## Spec-Kit Workflow (Source of Truth)

### 1. Constitution (WHY — Principles & Constraints)

**File**: `.specify/memory/constitution.md`

Defines the project's non-negotiables: architecture values, security rules, tech stack constraints, performance expectations, and patterns allowed.

Agents must check this before proposing solutions.

---

### 2. Specify (WHAT — Requirements, Journeys & Acceptance Criteria)

**File**: `specs/<feature>/spec.md`

Contains:
* User journeys
* Requirements
* Acceptance criteria
* Domain rules
* Business constraints

Agents must not infer missing requirements — they must request clarification or propose specification updates.

---

### 3. Plan (HOW — Architecture, Components, Interfaces)

**File**: `specs/<feature>/plan.md`

Includes:
* Component breakdown
* APIs & schema diagrams
* Service boundaries
* System responsibilities
* High-level sequencing

All architectural output MUST be generated from the Specify file.

---

### 4. Tasks (BREAKDOWN — Atomic, Testable Work Units)

**File**: `specs/<feature>/tasks.md`

Each Task must contain:
* Task ID
* Clear description
* Preconditions
* Expected outputs
* Artifacts to modify
* Links back to Specify + Plan sections

Agents **implement only what these tasks define**.

---

### 5. Implement (CODE — Write Only What the Tasks Authorize)

Agents now write code, but must:
* Reference Task IDs
* Follow the Plan exactly
* Not invent new features or flows
* Stop and request clarification if anything is underspecified

> The golden rule: **No task = No code.**

---

## Agent Behavior in This Project

### When generating code:

Agents must reference:

```
[Task]: T-001
[From]: specs/<feature>/spec.md §2.1, specs/<feature>/plan.md §3.4
```

### When proposing architecture:

Agents must reference:

```
Update required in specs/<feature>/plan.md → add component X
```

### When proposing new behavior or a new feature:

Agents must reference:

```
Requires update in specs/<feature>/spec.md (WHAT)
```

### When changing principles:

Agents must reference:

```
Modify .specify/memory/constitution.md → Principle #X
```

---

## Agent Failure Modes (What Agents MUST Avoid)

Agents are NOT allowed to:

* Freestyle code or architecture
* Generate missing requirements
* Create tasks on their own
* Alter stack choices without justification
* Add endpoints, fields, or flows that aren't in the spec
* Ignore acceptance criteria
* Produce "creative" implementations that violate the plan

If a conflict arises between spec files, the **Constitution > Specify > Plan > Tasks** hierarchy applies.

---

## Developer–Agent Alignment

Humans and agents collaborate, but the **spec is the single source of truth**.

Before every session, agents should re-read:

1. `.specify/memory/constitution.md`
2. Current feature's `spec.md`, `plan.md`, `tasks.md`

This ensures predictable, deterministic development.

---

## SpecKit Plus Commands (MCP Prompts)

The following commands are available as MCP prompts via `.claude/commands/`:

* `/sp.constitution` - Create/update project constitution
* `/sp.specify` - Create feature specification (WHAT)
* `/sp.plan` - Create technical plan (HOW)
* `/sp.tasks` - Break plan into actionable tasks
* `/sp.implement` - Execute implementation
* `/sp.checklist` - Generate test checklist
* `/sp.analyze` - Analyze code/specs
* `/sp.clarify` - Request clarification
* `/sp.adr` - Create Architecture Decision Record
* `/sp.phr` - Create Prompt History Record
* `/sp.git.commit_pr` - Git operations

---

## Todo App Hackathon - Phase Guidelines

This project is part of the "Evolution of Todo" hackathon with 5 progressive phases:

### Phase I: Python Console App (In-Memory)
* Basic CRUD operations
* In-memory storage
* Python 3.13+ with UV

### Phase II: Full-Stack Web App
* Next.js 16+ frontend
* FastAPI backend
* SQLModel ORM
* Neon Serverless PostgreSQL
* Better Auth authentication

### Phase III: AI Chatbot
* OpenAI ChatKit UI
* OpenAI Agents SDK
* MCP Server with Official MCP SDK
* Stateless chat with database persistence

### Phase IV: Local Kubernetes
* Docker containerization
* Minikube deployment
* Helm charts
* kubectl-ai and kagent

### Phase V: Cloud Deployment
* Event-driven with Kafka
* Dapr integration
* Azure/GCP/Oracle Cloud
* CI/CD with GitHub Actions

---

## Workflow Summary

1. **Initialize**: Project initialized with `uv specifyplus init`
2. **Instruct**: AGENTS.md defines the rules (this file)
3. **Bridge**: CLAUDE.md references AGENTS.md
4. **Empower**: MCP gives agents the tools to execute
5. **Execute**: Follow Specify → Plan → Tasks → Implement cycle

---

## Key Constraints for This Project

* **No manual coding** - All code generated via Claude Code using specs
* **Spec-first mandatory** - Cannot write code without approved spec
* **Monorepo structure** - All phases in single repository
* **Better Auth for authentication** - JWT tokens for API security
* **Stateless architecture** - All state in database (Neon PostgreSQL)
* **MCP tools for AI** - Chatbot uses MCP server for task operations

---

**Version**: 1.0.0
**Created**: 2025-12-15
**Project**: Evolution of Todo Hackathon II
