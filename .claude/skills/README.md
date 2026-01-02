# Claude Skills Directory

This directory contains quick workflow shortcuts (skills) for the Evolution of Todo hackathon project. Skills are executable commands that automate common development tasks.

## Purpose

Skills provide:
- **Quick commands** for common workflows
- **Time-saving shortcuts** for repetitive tasks
- **Consistent execution** of multi-step processes
- **Best practices** baked into commands

## Available Skills

### Phase Workflow Skills

| Skill | Command | Description | Phase |
|-------|---------|-------------|-------|
| **[phase1.run](./phase1.run.md)** | `/phase1.run` | Run Phase I console app | I |
| **[phase2.dev](./phase2.dev.md)** | `/phase2.dev` | Start Phase II dev servers | II+ |
| **[phase3.chat](./phase3.chat.md)** | `/phase3.chat` | Start chatbot with MCP server | III+ |

### Testing Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **[test.all](./test.all.md)** | `/test.all` | Run all tests (frontend + backend) |

### Database Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **[db.migrate](./db.migrate.md)** | `/db.migrate` | Create and apply database migrations |
| **[db.seed](./db.seed.md)** | `/db.seed` | Seed database with test data |

### Deployment Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **[deploy.vercel](./deploy.vercel.md)** | `/deploy.vercel` | Deploy frontend to Vercel |
| **[deploy.railway](./deploy.railway.md)** | `/deploy.railway` | Deploy backend to Railway |
| **[k8s.deploy](./k8s.deploy.md)** | `/k8s.deploy` | Deploy to Kubernetes |

### Development Workflow Skills

| Skill | Command | Description |
|-------|---------|-------------|
| **[dev.setup](./dev.setup.md)** | `/dev.setup` | Complete development environment setup |
| **[dev.clean](./dev.clean.md)** | `/dev.clean` | Clean build artifacts and dependencies |

## Quick Reference

### Phase I Development
```bash
/dev.setup --phase=1    # Initial setup
/phase1.run             # Run console app
```

### Phase II Development
```bash
/dev.setup --phase=2    # Initial setup
/db.migrate upgrade     # Apply migrations
/db.seed                # Add test data
/phase2.dev             # Start dev servers
/test.all               # Run all tests
```

### Phase III Development
```bash
/dev.setup --phase=3    # Initial setup
/db.migrate upgrade     # Apply migrations (includes conversations/messages tables)
/db.seed                # Add test data
/phase3.chat            # Start chatbot + MCP server + dev servers
/test.all               # Run all tests
```

### Phase IV Development
```bash
/k8s.deploy --local     # Deploy to Minikube
/k8s.deploy --dry-run   # Preview deployment
```

### Phase V Development
```bash
/k8s.deploy --cloud=azure   # Deploy to Azure AKS
/k8s.deploy --cloud=gke     # Deploy to Google GKE
```

## Common Workflows

### First Time Setup
```bash
# 1. Clone repository
git clone <repo-url>
cd hackaton2

# 2. Run setup
/dev.setup

# 3. Configure environment variables
# Edit backend/.env and frontend/.env.local

# 4. Start development
/phase2.dev
```

### Daily Development
```bash
# Pull latest changes
git pull origin main

# Install any new dependencies
/dev.setup

# Run migrations
/db.migrate upgrade

# Start dev servers
/phase2.dev
```

### Before Committing
```bash
# Run all tests
/test.all

# Fix any failing tests

# Create PHR
/sp.phr

# Commit and push
git add .
git commit -m "Your message"
git push
```

### Deployment Workflow
```bash
# 1. Run tests
/test.all

# 2. Deploy backend
/deploy.railway

# 3. Deploy frontend
/deploy.vercel

# 4. Verify deployment
curl https://your-backend.railway.app/health
```

### Troubleshooting Workflow
```bash
# Clean environment
/dev.clean

# Reinstall dependencies
/dev.setup

# Clear and reseed database
/db.seed --clear

# Restart dev servers
/phase2.dev
```

## Skill Flags

Many skills support flags for customization:

### /test.all
```bash
/test.all           # Run all tests
/test.all --fast    # Skip slow tests
/test.all --e2e     # Include E2E tests
/test.all --unit    # Unit tests only
```

### /db.migrate
```bash
/db.migrate "Add priority field"  # Create migration
/db.migrate upgrade               # Apply migrations
/db.migrate downgrade             # Revert last migration
/db.migrate status                # Show current version
```

### /db.seed
```bash
/db.seed            # Seed database
/db.seed --clear    # Clear existing data first
/db.seed --minimal  # Minimal data set
```

### /dev.setup
```bash
/dev.setup              # Setup Phase II (default)
/dev.setup --phase=1    # Setup Phase I
/dev.setup --phase=3    # Setup Phase III
/dev.setup --skip-db    # Skip database setup
```

### /dev.clean
```bash
/dev.clean          # Clean build artifacts
/dev.clean --deep   # Also remove .env and database
/dev.clean --cache  # Clean cache only
```

### /k8s.deploy
```bash
/k8s.deploy                 # Deploy to Minikube
/k8s.deploy --cloud=azure   # Deploy to Azure AKS
/k8s.deploy --cloud=gke     # Deploy to Google GKE
/k8s.deploy --dry-run       # Preview without applying
```

## How Skills Work

### Skill Structure
Each skill file contains:
1. **Description** - What the skill does
2. **Usage** - Command syntax
3. **What It Does** - Step-by-step actions
4. **Commands Executed** - Actual bash commands
5. **Prerequisites** - Required setup
6. **Flags** - Optional parameters
7. **Related Files** - Relevant file paths
8. **Related Agents** - Link to expert agents

### Skill Invocation
Skills are invoked using slash commands:
```bash
/skill-name [flags]
```

Example:
```bash
/db.migrate "Add due_date column"
```

### Skill Chaining
Skills can be chained for complex workflows:
```bash
/dev.clean && /dev.setup && /db.migrate upgrade && /phase2.dev
```

## Creating Custom Skills

### Skill Template
```markdown
# Skill: skill-name

## Description
Brief description of what this skill does

## Usage
\`\`\`
/skill-name [flags]
\`\`\`

## What It Does
- Step 1
- Step 2
- Step 3

## Commands Executed
\`\`\`bash
command1
command2
\`\`\`

## Prerequisites
- Requirement 1
- Requirement 2

## Flags
- \`--flag1\` - Description

## Related Files
- \`path/to/file\`

## Related Agents
- \`.claude/agents/agent-name.md\`
```

### Adding New Skills
1. Create file in `.claude/skills/`
2. Follow skill template structure
3. Test the skill commands
4. Update this README
5. Link to related agents

## Environment Variables

Skills may require environment variables:

### Backend (.env)
```bash
DATABASE_URL=postgresql://...
JWT_SECRET=your-secret-key
OPENAI_API_KEY=sk-...
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key
NEXTAUTH_URL=http://localhost:3000
```

## Troubleshooting Skills

### Skill Not Working?

1. **Check prerequisites**
   - Read skill file for required setup
   - Verify all dependencies installed

2. **Check environment variables**
   - Ensure .env files configured
   - Verify values are correct

3. **Check logs**
   - Skills output detailed error messages
   - Follow error suggestions

4. **Run manual commands**
   - Skills show exact commands executed
   - Try running commands manually to debug

### Common Issues

#### "Command not found"
- Install missing tool (UV, npm, kubectl, etc.)
- Check PATH environment variable

#### "Connection refused"
- Verify service is running
- Check port not already in use
- Verify URL in environment variables

#### "Permission denied"
- Run with appropriate permissions
- Check file ownership
- Verify write access to directories

## Related Resources

### Agents
- `.claude/agents/` - Expert agents for each phase/domain
- `.claude/agents/README.md` - Agent documentation

### Commands
- `.claude/commands/` - SpecKit Plus commands
  - `/sp.specify` - Create specification
  - `/sp.plan` - Create plan
  - `/sp.tasks` - Create tasks
  - `/sp.implement` - Execute implementation
  - `/sp.phr` - Create Prompt History Record

### Documentation
- `README.md` - Project overview
- `AGENTS.md` - Agent rules and workflow
- `CLAUDE.md` - Claude Code configuration
- `.specify/memory/constitution.md` - Project principles

## Tips

### Speed Up Development
- Use skills instead of manual commands
- Chain skills for complex workflows
- Create custom skills for repeated tasks

### Consistent Execution
- Skills follow best practices
- Reduce human error
- Ensure all team members use same workflow

### Learn by Doing
- Read skill files to learn commands
- Modify skills for your needs
- Share custom skills with team

## Phase-Specific Workflows

### Phase I
```bash
/dev.setup --phase=1
/phase1.run
```

### Phase II
```bash
/dev.setup --phase=2
/db.migrate upgrade
/db.seed
/phase2.dev
/test.all
/deploy.vercel
/deploy.railway
```

### Phase III
```bash
/dev.setup --phase=3
/db.migrate upgrade
/db.seed
/phase3.chat
/test.all
```

### Phase IV
```bash
/dev.setup --phase=2
/k8s.deploy --local
kubectl get pods -n todo-app
```

### Phase V
```bash
/dev.setup --phase=2
/k8s.deploy --cloud=azure
kubectl get pods -n todo-app
```

## Next Steps

1. **Explore skills** - Read each skill file
2. **Run setup** - `/dev.setup`
3. **Start development** - `/phase2.dev`
4. **Run tests** - `/test.all`
5. **Deploy** - `/deploy.vercel` + `/deploy.railway`

---

**Remember**: Skills save time and reduce errors. Use them frequently! ⚡
