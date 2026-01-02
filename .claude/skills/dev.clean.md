# Skill: dev.clean

## Description
Clean development environment (dependencies, cache, build artifacts)

## Usage
```
/dev.clean
/dev.clean --deep
```

## What It Does
- Removes node_modules
- Clears Python cache
- Deletes build artifacts
- Removes temporary files
- Optionally clears database (with --deep)

## Commands Executed
```bash
# Frontend cleanup
cd frontend
rm -rf node_modules
rm -rf .next
rm -rf coverage
npm cache clean --force

# Backend cleanup
cd backend
find . -type d -name "__pycache__" -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
rm -rf .pytest_cache
rm -rf htmlcov
rm -rf .coverage

# UV cache
uv cache clean

echo "✅ Development environment cleaned"
```

## What Gets Removed
- `frontend/node_modules/` - Node dependencies
- `frontend/.next/` - Next.js build output
- `frontend/coverage/` - Test coverage reports
- `backend/__pycache__/` - Python bytecode cache
- `backend/.pytest_cache/` - Pytest cache
- `backend/htmlcov/` - Coverage HTML reports
- `.uv/cache/` - UV package cache

## Flags
- `--deep` - Also clear database and env files
- `--db` - Clear database only
- `--cache` - Clear cache only
- `--build` - Clear build artifacts only

## Deep Clean (--deep)
Additionally removes:
- `.env` files (backend and frontend)
- Database data (if local SQLite)
- Log files
- Temporary files

**Warning**: Deep clean requires re-setup with `/dev.setup`

## When to Use
- **Normal Clean**: Before reinstalling dependencies
- **Deep Clean**: When switching branches/phases
- **Cache Clean**: When experiencing build issues
- **Build Clean**: Before production build

## After Cleaning
```bash
# Reinstall dependencies
/dev.setup

# Or manually:
cd frontend && npm install
cd backend && uv sync
```

## Disk Space Saved
Typical savings:
- Frontend: 300-500 MB (node_modules + .next)
- Backend: 50-100 MB (cache + coverage)
- Total: 400-600 MB

## Related Skills
- `/dev.setup` - Reinstall after cleaning

## Related Agents
- `.claude/agents/phase2-web.md`

---

**Tip**: Run `/dev.clean` if experiencing weird build issues or before switching phases.
