# Claude Agents Directory

This directory contains specialized AI agents for the Evolution of Todo hackathon project. Each agent is an expert in a specific phase or domain of the project.

## Purpose

Agents provide:
- **Phase-specific expertise** for each evolution stage
- **Domain knowledge** for specialized tasks (testing, deployment, database)
- **Best practices** and patterns for each technology stack
- **Troubleshooting guides** for common issues
- **Quick reference** for commands and workflows

## Available Agents

### Phase-Specific Agents

| Agent | Purpose | Technology Stack |
|-------|---------|------------------|
| **[phase1-console.md](./phase1-console.md)** | Python console app development | Python 3.13+, UV |
| **[phase2-web.md](./phase2-web.md)** | Full-stack web application | Next.js 16+, FastAPI, PostgreSQL |
| **[phase3-chatbot.md](./phase3-chatbot.md)** | AI chatbot with MCP server | OpenAI Agents SDK, MCP |
| **[phase4-kubernetes.md](./phase4-kubernetes.md)** | Kubernetes deployment | Docker, Minikube, Helm |
| **[phase5-cloud.md](./phase5-cloud.md)** | Cloud-native event-driven | Kafka, Dapr, AKS/GKE/OKE |

### Specialized Agents

| Agent | Purpose | Scope |
|-------|---------|-------|
| **[testing.md](./testing.md)** | Testing strategies and frameworks | All phases |
| **[deployment.md](./deployment.md)** | Deployment workflows | Vercel, Railway, K8s |
| **[database.md](./database.md)** | Database operations and migrations | Phase II-V |

## When to Use Which Agent

### Working on Phase I?
→ Read **phase1-console.md**
- Console app implementation
- In-memory CRUD operations
- Python best practices

### Working on Phase II?
→ Read **phase2-web.md** + **database.md**
- Next.js frontend development
- FastAPI backend APIs
- PostgreSQL schema design
- Better Auth integration

### Working on Phase III?
→ Read **phase3-chatbot.md** + **phase2-web.md**
- MCP server implementation
- OpenAI Agents SDK integration
- ChatKit UI setup
- Natural language processing

### Working on Phase IV?
→ Read **phase4-kubernetes.md** + **deployment.md**
- Docker containerization
- Kubernetes manifests
- Helm charts
- Local cluster setup

### Working on Phase V?
→ Read **phase5-cloud.md** + **deployment.md**
- Event-driven architecture
- Kafka event streaming
- Dapr components
- Cloud deployment (AKS/GKE/OKE)

### Writing Tests?
→ Read **testing.md**
- Unit tests (pytest, Jest)
- Integration tests
- E2E tests (Playwright)
- MCP tool tests
- Event-driven tests

### Deploying?
→ Read **deployment.md**
- Vercel deployment (frontend)
- Railway deployment (backend)
- Kubernetes deployment
- CI/CD pipelines

### Database Work?
→ Read **database.md**
- Schema design
- Alembic migrations
- Query optimization
- Data seeding

## How to Use Agents

### 1. Read Before Implementing
Before starting work on any phase or feature:
```bash
# Open the relevant agent file
cat .claude/agents/phase2-web.md
```

### 2. Follow Spec-Driven Development
All agents enforce the SDD workflow:
```
Specify → Plan → Tasks → Implement
```

### 3. Reference During Development
Keep agent files open for:
- Technology stack details
- Common operations
- Code examples
- Troubleshooting tips

### 4. Use Related Commands
Each agent lists relevant commands:
- `/sp.specify` - Create specification
- `/sp.plan` - Create technical plan
- `/sp.tasks` - Break into tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record

## Agent Structure

Each agent file contains:
1. **Purpose** - What this agent does
2. **Responsibilities** - Key tasks handled
3. **Technology Stack** - Tools and frameworks
4. **Key Directories/Files** - Important paths
5. **Mandatory Workflow** - SDD process
6. **Core Features** - What to build
7. **Common Operations** - Code examples
8. **Success Criteria** - Definition of done
9. **Related Agents** - Cross-references
10. **Commands to Use** - Relevant skills/commands

## Project Constitution

All agents MUST follow: `.specify/memory/constitution.md`

### Core Principles
- **Spec-Driven Development** - No code without approved spec
- **Stateless Architecture** - All state in database
- **User Isolation** - Data filtered by user_id
- **Security-First** - JWT auth, input validation
- **Progressive Evolution** - Each phase builds on previous

## File References

Agents use code references in this format:
```
filename.py:line_number
```

Example: `src/main.py:42` refers to line 42 in src/main.py

## Related Resources

### Specifications
- `specs/phase1-console-app/` - Phase I specs
- `specs/phase2-web-app/` - Phase II specs
- `specs/phase3-chatbot/` - Phase III specs (to be created)
- `specs/phase4-kubernetes/` - Phase IV specs (to be created)
- `specs/phase5-cloud/` - Phase V specs (to be created)

### Commands
- `.claude/commands/` - SpecKit Plus commands
- `.claude/skills/` - Quick workflow shortcuts

### Documentation
- `README.md` - Project overview
- `AGENTS.md` - Agent instructions and rules
- `CLAUDE.md` - Claude Code configuration

## Tips

### Multi-Phase Work
If working across multiple phases, read agents in order:
1. **phase1-console.md** - Foundation
2. **phase2-web.md** - Web layer
3. **phase3-chatbot.md** - AI layer
4. **phase4-kubernetes.md** - Container layer
5. **phase5-cloud.md** - Cloud layer

### Cross-Cutting Concerns
For features spanning multiple domains:
- **Authentication** → phase2-web.md + database.md
- **API Testing** → testing.md + phase2-web.md
- **Production Deploy** → deployment.md + phase5-cloud.md
- **Database Changes** → database.md + deployment.md

### Quick Navigation
```bash
# List all agents
ls .claude/agents/

# Search for specific content
grep -r "MCP server" .claude/agents/

# View agent in terminal
cat .claude/agents/phase3-chatbot.md
```

## Contributing

When creating new agents:
1. Follow existing agent structure
2. Include all required sections
3. Provide code examples
4. Link to related agents
5. Update this README

## Questions?

- Check **AGENTS.md** for overall agent rules
- Check **constitution.md** for project principles
- Use `/sp.clarify` if spec is unclear
- Ask for human clarification when uncertain

---

**Remember**: Agents are your co-pilots. They guide you through each phase with expertise and best practices. Read them, follow them, succeed! 🚀
