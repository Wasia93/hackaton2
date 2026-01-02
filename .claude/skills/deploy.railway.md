# Skill: deploy.railway

## Description
Deploy backend to Railway

## Usage
```
/deploy.railway
```

## What It Does
- Deploys FastAPI backend to Railway
- Configures environment variables
- Runs database migrations
- Displays deployment URL

## Commands Executed

### Via Railway CLI
```bash
cd backend
railway up
```

### Via Git Push (Recommended)
```bash
git push railway main  # If Railway remote configured
```

## Prerequisites
- Railway account created
- Railway project initialized
- Environment variables configured
- Database (Neon) accessible

## Environment Variables (Railway Dashboard)
```
DATABASE_URL=postgresql://...@neon.tech/db
JWT_SECRET=your-secret-key
OPENAI_API_KEY=sk-... (Phase III+)
CORS_ORIGINS=https://your-frontend.vercel.app
PORT=8000
```

## Railway Configuration (railway.toml)
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

## Deployment Flow
1. Push code to GitHub
2. Railway detects changes (if connected)
3. Installs dependencies via UV
4. Runs database migrations (if configured)
5. Starts FastAPI server
6. Returns deployment URL

## Database Migrations on Deploy

### Option 1: Separate Migration Service
Create migration service in Railway:
```bash
Build Command: uv sync
Start Command: uv run alembic upgrade head
```

### Option 2: Pre-start Script
Create `scripts/start.sh`:
```bash
#!/bin/bash
uv run alembic upgrade head  # Run migrations
uv run uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

Update railway.toml:
```toml
[deploy]
startCommand = "bash scripts/start.sh"
```

## Post-Deployment Checks
- [ ] API accessible at Railway URL
- [ ] Health check endpoint responding: `/health`
- [ ] API docs accessible: `/docs`
- [ ] Database connection working
- [ ] Migrations applied successfully
- [ ] CORS configured correctly

## Testing Deployment
```bash
# Test health endpoint
curl https://your-backend.railway.app/health

# Test API endpoint (with auth)
curl -H "Authorization: Bearer TOKEN" \
     https://your-backend.railway.app/api/user-id/tasks
```

## Troubleshooting

### Build Fails
- Check Railway logs
- Verify `pyproject.toml` and `uv.lock` in repo
- Test `uv sync` locally

### App Crashes on Start
- Check Railway logs for errors
- Verify DATABASE_URL correct
- Ensure health check path exists
- Check PORT environment variable

### Database Connection Fails
- Verify DATABASE_URL includes SSL: `?sslmode=require`
- Check Neon database is running
- Test connection locally with same URL

## Related Files
- `backend/` - FastAPI application
- `railway.toml` - Railway configuration
- `.railwayignore` - Files to ignore

## Related Agents
- `.claude/agents/deployment.md`
- `.claude/agents/phase2-web.md`
- `.claude/agents/database.md`

---

**Tip**: Enable auto-deploy in Railway for seamless deployments on every push to main.
