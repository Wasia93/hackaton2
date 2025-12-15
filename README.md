# Evolution of Todo - Hackathon II

A progressive todo application evolving from a simple console app to a cloud-native AI chatbot, built using **Spec-Driven Development (SDD)** with Claude Code and SpecKit Plus.

## Project Overview

This project demonstrates the **Nine Pillars of AI-Driven Development** through 5 progressive phases:

- **Phase I**: In-Memory Python Console App (Basic CRUD)
- **Phase II**: Full-Stack Web Application (Next.js + FastAPI + Neon DB)
- **Phase III**: AI-Powered Todo Chatbot (OpenAI Agents SDK + MCP)
- **Phase IV**: Local Kubernetes Deployment (Minikube + Helm)
- **Phase V**: Advanced Cloud Deployment (Kafka + Dapr + Cloud)

## Current Phase: Phase I - Console App

### Features (Basic Level)

- ✅ Add Task - Create new todo items
- ✅ Delete Task - Remove tasks from the list
- ✅ Update Task - Modify existing task details
- ✅ View Task List - Display all tasks
- ✅ Mark as Complete - Toggle task completion status

### Technology Stack

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Storage**: In-memory (Python data structures)
- **Development Approach**: Spec-Driven Development with Claude Code + SpecKit Plus

## Prerequisites

- Python 3.13+
- UV package manager
- Claude Code CLI
- Git

## Installation

### 1. Clone the repository

```bash
git clone <repository-url>
cd hackaton2
```

### 2. Install dependencies with UV

```bash
uv sync
```

### 3. Run the console application

```bash
uv run python src/main.py
```

## Project Structure

```
hackaton2/
├── .claude/                 # Claude Code commands (SpecKit Plus)
│   └── commands/            # Spec commands (sp.specify, sp.plan, etc.)
├── .specify/                # SpecKit Plus configuration
│   ├── memory/
│   │   └── constitution.md  # Project constitution
│   └── templates/           # Spec templates
├── specs/                   # Feature specifications
│   └── phase1-console-app/  # Phase I specs
│       ├── spec.md          # WHAT to build
│       ├── plan.md          # HOW to build
│       └── tasks.md         # Atomic work units
├── src/                     # Python source code
│   └── main.py              # Application entry point
├── history/                 # Development history
│   ├── prompts/             # Prompt History Records (PHR)
│   └── adr/                 # Architecture Decision Records
├── AGENTS.md                # Agent instructions
├── CLAUDE.md                # Claude Code configuration
└── README.md                # This file
```

## Development Workflow

This project follows **Spec-Driven Development (SDD)**:

### 1. Specify (WHAT)
```bash
# Use Claude Code with SpecKit Plus
/sp.specify
```
Define requirements, user journeys, and acceptance criteria.

### 2. Plan (HOW)
```bash
/sp.plan
```
Create technical architecture and component design.

### 3. Tasks (BREAKDOWN)
```bash
/sp.tasks
```
Break down the plan into atomic, testable work units.

### 4. Implement (CODE)
```bash
/sp.implement
```
Generate code via Claude Code based on tasks.

### 5. Review & Iterate
Refine specs if Claude Code output needs adjustment.

## Key Principles

- **No Manual Coding**: All code generated via Claude Code using specs
- **Spec-First Mandatory**: Cannot write code without approved spec
- **Task ID References**: Every code change references a Task ID
- **Constitution Compliance**: All development follows `.specify/memory/constitution.md`

## Commands

### SpecKit Plus Commands (via Claude Code)

- `/sp.constitution` - Create/update project constitution
- `/sp.specify` - Create feature specification
- `/sp.plan` - Create technical plan
- `/sp.tasks` - Break plan into tasks
- `/sp.implement` - Execute implementation
- `/sp.checklist` - Generate test checklist
- `/sp.analyze` - Analyze code/specs
- `/sp.clarify` - Request clarification
- `/sp.adr` - Create Architecture Decision Record
- `/sp.phr` - Create Prompt History Record

## Testing

```bash
# Run tests (Phase I - manual testing via console)
uv run python src/main.py
```

## Documentation

- **AGENTS.md** - Comprehensive agent instructions
- **.specify/memory/constitution.md** - Project constitution and principles
- **specs/** - All feature specifications, plans, and tasks
- **history/prompts/** - Prompt History Records
- **history/adr/** - Architectural Decision Records

## Hackathon Information

- **Start Date**: December 1, 2025
- **Phase I Due**: December 7, 2025
- **Points**: 100 points (Phase I)
- **Submission**: https://forms.gle/KMKEKaFUD6ZX4UtY8

## Resources

- [Claude Code](https://claude.com/claude-code)
- [SpecKit Plus](https://github.com/panaversity/spec-kit-plus)
- [Hackathon Documentation](.claude/commands/documentation.md)

## License

This is a hackathon project for educational purposes.

---

**Built with Spec-Driven Development using Claude Code & SpecKit Plus**
