# Claude Agents & Skills Index

**Evolution of Todo - Hackathon II**

This index provides a complete overview of all agents and skills available for the project.

## 📁 Directory Structure

```
.claude/
├── agents/                 # Expert agents for each phase/domain
│   ├── README.md          # Agent documentation
│   ├── phase1-console.md  # Phase I: Console app expert
│   ├── phase2-web.md      # Phase II: Web app expert
│   ├── phase3-chatbot.md  # Phase III: AI chatbot expert
│   ├── phase4-kubernetes.md # Phase IV: Kubernetes expert
│   ├── phase5-cloud.md    # Phase V: Cloud deployment expert
│   ├── testing.md         # Testing expert
│   ├── deployment.md      # Deployment expert
│   └── database.md        # Database expert
├── skills/                # Quick workflow shortcuts
│   ├── README.md          # Skills documentation
│   ├── phase1.run.md      # Run Phase I console app
│   ├── phase2.dev.md      # Start Phase II dev servers
│   ├── phase3.chat.md     # Start Phase III chatbot
│   ├── test.all.md        # Run all tests
│   ├── db.migrate.md      # Database migrations
│   ├── db.seed.md         # Seed test data
│   ├── deploy.vercel.md   # Deploy frontend to Vercel
│   ├── deploy.railway.md  # Deploy backend to Railway
│   ├── k8s.deploy.md      # Deploy to Kubernetes
│   ├── dev.setup.md       # Complete dev environment setup
│   └── dev.clean.md       # Clean build artifacts
├── commands/              # SpecKit Plus commands (pre-existing)
│   ├── sp.specify.md
│   ├── sp.plan.md
│   ├── sp.tasks.md
│   ├── sp.implement.md
│   └── ... (10+ more)
└── INDEX.md               # This file
```

## 🤖 Agents (8 Total)

### Phase-Specific Agents (5)

1. **phase1-console.md** - Python Console App
   - Technology: Python 3.13+, UV
   - Features: In-memory CRUD, CLI interface
   - Use for: Phase I development

2. **phase2-web.md** - Full-Stack Web Application
   - Technology: Next.js 16+, FastAPI, PostgreSQL
   - Features: Multi-user, authentication, REST API
   - Use for: Phase II development

3. **phase3-chatbot.md** - AI-Powered Chatbot
   - Technology: OpenAI Agents SDK, MCP, ChatKit
   - Features: Natural language task management
   - Use for: Phase III development

4. **phase4-kubernetes.md** - Kubernetes Deployment
   - Technology: Docker, Minikube, Helm
   - Features: Containerization, orchestration
   - Use for: Phase IV development

5. **phase5-cloud.md** - Cloud-Native Event-Driven
   - Technology: Kafka, Dapr, AKS/GKE/OKE
   - Features: Event streaming, distributed systems
   - Use for: Phase V development

### Specialized Agents (3)

6. **testing.md** - Testing Strategies
   - Scope: All phases
   - Features: Unit, integration, E2E, MCP tests
   - Use for: Writing and running tests

7. **deployment.md** - Deployment Workflows
   - Scope: Phase II-V
   - Features: Vercel, Railway, Kubernetes deployment
   - Use for: Deploying to any environment

8. **database.md** - Database Operations
   - Scope: Phase II-V
   - Features: Schema design, migrations, optimization
   - Use for: Database work

## ⚡ Skills (12 Total)

### Phase Workflow (3)
- `/phase1.run` - Run Phase I console app
- `/phase2.dev` - Start Phase II dev servers (frontend + backend)
- `/phase3.chat` - Start Phase III chatbot with MCP server

### Testing (1)
- `/test.all` - Run all tests (frontend + backend with coverage)

### Database (2)
- `/db.migrate` - Create and apply database migrations
- `/db.seed` - Seed database with test data

### Deployment (3)
- `/deploy.vercel` - Deploy frontend to Vercel
- `/deploy.railway` - Deploy backend to Railway
- `/k8s.deploy` - Deploy to Kubernetes (Minikube or cloud)

### Development (2)
- `/dev.setup` - Complete development environment setup
- `/dev.clean` - Clean build artifacts and dependencies

### SpecKit Plus Commands (Pre-existing)
- `/sp.specify` - Create feature specification
- `/sp.plan` - Create technical plan
- `/sp.tasks` - Break plan into tasks
- `/sp.implement` - Execute implementation
- `/sp.phr` - Create Prompt History Record
- `/sp.adr` - Create Architecture Decision Record
- `/sp.git.commit_pr` - Git commit and PR workflow
- And more...

## 🚀 Quick Start Guide

### Phase I Development
```bash
# Read agent
cat .claude/agents/phase1-console.md

# Run app
/phase1.run
```

### Phase II Development
```bash
# Read agents
cat .claude/agents/phase2-web.md
cat .claude/agents/database.md

# Setup environment
/dev.setup --phase=2

# Start development
/db.migrate upgrade
/db.seed
/phase2.dev

# Run tests
/test.all

# Deploy
/deploy.railway
/deploy.vercel
```

### Phase III Development
```bash
# Read agent
cat .claude/agents/phase3-chatbot.md

# Setup and run
/dev.setup --phase=3
/db.migrate upgrade
/phase3.chat
```

### Phase IV Development
```bash
# Read agent
cat .claude/agents/phase4-kubernetes.md

# Deploy to Minikube
/k8s.deploy --local
```

### Phase V Development
```bash
# Read agent
cat .claude/agents/phase5-cloud.md

# Deploy to cloud
/k8s.deploy --cloud=azure
```

## 📖 Documentation Flow

### For New Features
1. **Read** relevant agent (e.g., `phase2-web.md`)
2. **Create spec**: `/sp.specify`
3. **Plan architecture**: `/sp.plan`
4. **Break into tasks**: `/sp.tasks`
5. **Implement**: `/sp.implement`
6. **Test**: `/test.all`
7. **Document**: `/sp.phr`

### For Bug Fixes
1. **Read** relevant agent for context
2. **Identify** issue in code
3. **Write test** that reproduces bug
4. **Fix** issue following agent guidelines
5. **Verify**: `/test.all`
6. **Document**: `/sp.phr`

### For Deployment
1. **Read** `deployment.md` agent
2. **Run tests**: `/test.all`
3. **Deploy backend**: `/deploy.railway`
4. **Deploy frontend**: `/deploy.vercel`
5. **Verify** deployment health
6. **Document**: `/sp.phr`

## 🎯 Phase Progression

```
Phase I (Console)
    ↓
    /dev.setup --phase=1
    /phase1.run

Phase II (Web)
    ↓
    /dev.setup --phase=2
    /db.migrate upgrade
    /db.seed
    /phase2.dev

Phase III (Chatbot)
    ↓
    /dev.setup --phase=3
    /phase3.chat

Phase IV (Kubernetes)
    ↓
    /k8s.deploy --local

Phase V (Cloud)
    ↓
    /k8s.deploy --cloud=azure
```

## 🔍 Finding Information

### By Technology
- **Python**: phase1-console.md, database.md, testing.md
- **Next.js**: phase2-web.md, deployment.md
- **FastAPI**: phase2-web.md, database.md
- **PostgreSQL**: database.md, deployment.md
- **MCP**: phase3-chatbot.md
- **OpenAI**: phase3-chatbot.md
- **Docker**: phase4-kubernetes.md, deployment.md
- **Kubernetes**: phase4-kubernetes.md, phase5-cloud.md
- **Kafka**: phase5-cloud.md
- **Dapr**: phase5-cloud.md

### By Task
- **Setup environment**: dev.setup.md
- **Database migrations**: db.migrate.md, database.md
- **Write tests**: testing.md
- **Deploy app**: deployment.md, deploy.*.md
- **Run locally**: phase*.dev.md, phase*.run.md
- **Troubleshoot**: Relevant agent's "Troubleshooting" section

### By Error
Search agents for error messages:
```bash
grep -r "CrashLoopBackOff" .claude/agents/
grep -r "Connection refused" .claude/agents/
grep -r "ImagePullBackOff" .claude/agents/
```

## 📚 Learning Path

### Beginner
1. Read `README.md` (project root)
2. Read `AGENTS.md` (project rules)
3. Read `.specify/memory/constitution.md` (principles)
4. Read `phase1-console.md` (simple start)
5. Try `/phase1.run`

### Intermediate
1. Read `phase2-web.md` (web development)
2. Read `database.md` (data persistence)
3. Try `/dev.setup` and `/phase2.dev`
4. Read `testing.md` (quality assurance)
5. Try `/test.all`

### Advanced
1. Read `phase3-chatbot.md` (AI integration)
2. Read `phase4-kubernetes.md` (containerization)
3. Read `phase5-cloud.md` (cloud-native)
4. Read `deployment.md` (production deployment)
5. Try `/k8s.deploy --cloud=azure`

## 🛠️ Tools & Prerequisites

### Required Tools
- **Git** - Version control
- **UV** - Python package manager
- **Node.js 20+** - JavaScript runtime
- **Docker** - Containerization (Phase IV+)
- **kubectl** - Kubernetes CLI (Phase IV+)
- **Helm** - Kubernetes package manager (Phase IV+)

### Optional Tools
- **Vercel CLI** - Frontend deployment
- **Railway CLI** - Backend deployment
- **Minikube** - Local Kubernetes
- **k6** - Load testing

### Cloud Accounts (Phase V)
- **Neon** - Serverless PostgreSQL
- **Vercel** - Frontend hosting
- **Railway/Render** - Backend hosting
- **Azure/Google/Oracle** - Cloud Kubernetes

## 💡 Tips & Best Practices

### Always
- ✅ Read relevant agent before starting work
- ✅ Follow Spec-Driven Development workflow
- ✅ Run `/test.all` before committing
- ✅ Create PHR after major work: `/sp.phr`
- ✅ Reference Task IDs in code and commits

### Never
- ❌ Write code without approved spec
- ❌ Skip tests
- ❌ Hardcode secrets (use .env)
- ❌ Deploy without testing
- ❌ Commit without PHR

### Productivity
- Use skills for common tasks
- Keep agent files open for reference
- Chain skills for complex workflows
- Create custom skills for repeated tasks
- Read troubleshooting sections when stuck

## 🆘 Getting Help

### In Order of Preference
1. **Check agent file** for the relevant phase/domain
2. **Read skill file** for the specific command
3. **Search INDEX.md** (this file) for keywords
4. **Use `/sp.clarify`** to ask for specification clarification
5. **Ask user** for human judgment and decisions

### Common Questions
- **"How do I...?"** → Check skills README.md
- **"What technology for...?"** → Check phase agent
- **"How to deploy...?"** → Check deployment.md
- **"Database issue?"** → Check database.md
- **"Test failing?"** → Check testing.md

## 📊 Project Stats

- **Total Agents**: 8 (5 phase-specific + 3 specialized)
- **Total Skills**: 12 (quick workflow shortcuts)
- **Total Commands**: 12+ (SpecKit Plus commands)
- **Phases Covered**: 5 (Console → Web → AI → K8s → Cloud)
- **Technologies**: 20+ (Python, Node, React, FastAPI, PostgreSQL, MCP, Docker, Kubernetes, Kafka, Dapr, etc.)

## 🎓 Success Metrics

You're doing well when:
- ✅ Using agents as reference guides
- ✅ Running skills instead of manual commands
- ✅ Following Spec-Driven Development
- ✅ All tests passing before commits
- ✅ Creating PHRs consistently
- ✅ Deployments successful
- ✅ Code references Task IDs

## 🚦 Current Status

**Project Phase**: Phase II (Web Application)
**Specs Available**: Phase I, Phase II
**Next Steps**: Complete Phase II, then create Phase III spec

---

**Last Updated**: 2026-01-02
**Hackathon**: Evolution of Todo - Hackathon II
**Built with**: Spec-Driven Development using Claude Code & SpecKit Plus

**Happy Coding! 🚀**
