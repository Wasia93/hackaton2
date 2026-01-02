# Skill: dev.setup

## Description
Complete development environment setup

## Usage
```
/dev.setup
/dev.setup --phase=2
```

## What It Does
- Installs all dependencies
- Sets up environment variables
- Initializes database
- Runs migrations
- Seeds database with test data
- Verifies setup complete

## Commands Executed

### Phase I
```bash
# Install Python dependencies
uv sync

# Verify setup
uv run python --version
echo "✅ Phase I setup complete"
```

### Phase II+
```bash
# Backend setup
cd backend
uv sync
cp .env.example .env
echo "📝 Configure .env with DATABASE_URL and JWT_SECRET"

# Run migrations
uv run alembic upgrade head

# Seed database
uv run python scripts/seed.py

# Frontend setup
cd ../frontend
npm install
cp .env.example .env.local
echo "📝 Configure .env.local with NEXT_PUBLIC_API_URL"

echo "✅ Phase II setup complete"
```

## Prerequisites
- Node.js 20+ installed
- Python 3.13+ installed
- UV package manager installed
- Git installed
- Code editor (VS Code recommended)

## Environment Files Created

### Backend (.env)
```bash
DATABASE_URL=postgresql://user:pass@neon.tech/db
JWT_SECRET=your-secret-key-here
OPENAI_API_KEY=sk-... (Phase III+)
CORS_ORIGINS=http://localhost:3000
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXTAUTH_SECRET=your-secret-key-here
NEXTAUTH_URL=http://localhost:3000
```

## Setup Checklist
- [ ] UV installed: `uv --version`
- [ ] Node.js installed: `node --version`
- [ ] Dependencies installed (frontend + backend)
- [ ] Environment variables configured
- [ ] Database connection working
- [ ] Migrations applied
- [ ] Test data seeded
- [ ] Development servers start without errors

## Verification
```bash
# Test backend
cd backend
uv run uvicorn app.main:app
# Visit: http://localhost:8000/docs

# Test frontend
cd frontend
npm run dev
# Visit: http://localhost:3000
```

## Flags
- `--phase=1` - Set up Phase I only
- `--phase=2` - Set up Phase II (default)
- `--phase=3` - Set up Phase III (includes chatbot)
- `--skip-db` - Skip database setup
- `--skip-seed` - Skip database seeding

## Troubleshooting

### UV Not Found
```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### Database Connection Fails
- Verify DATABASE_URL in .env
- Check Neon database is running
- Ensure SSL mode: `?sslmode=require`

### Port Already in Use
```bash
# Kill process on port 3000
npx kill-port 3000

# Kill process on port 8000
npx kill-port 8000
```

## Next Steps After Setup
1. Run development servers: `/phase2.dev`
2. Run tests: `/test.all`
3. Start coding!

## Related Files
- `.env.example` - Environment template (backend)
- `frontend/.env.example` - Environment template (frontend)
- `scripts/seed.py` - Database seeding script

## Related Agents
- `.claude/agents/database.md`
- All phase agents

---

**Tip**: Run this skill once when first cloning the repository or switching phases.
