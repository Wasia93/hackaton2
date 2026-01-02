# Skill: db.migrate

## Description
Create and apply database migrations

## Usage
```
/db.migrate [message]
/db.migrate upgrade
/db.migrate downgrade
```

## What It Does
- Creates new Alembic migration (if message provided)
- Applies pending migrations (`upgrade`)
- Reverts last migration (`downgrade`)
- Shows migration status

## Commands Executed

### Create Migration
```bash
cd backend
uv run alembic revision --autogenerate -m "Your migration message"
```

### Apply Migrations
```bash
cd backend
uv run alembic upgrade head
```

### Revert Migration
```bash
cd backend
uv run alembic downgrade -1
```

### Show Status
```bash
cd backend
uv run alembic current
uv run alembic history --verbose
```

## Prerequisites
- Alembic initialized in backend
- DATABASE_URL environment variable set
- SQLModel models defined
- Database connection working

## Migration Workflow
1. Modify SQLModel models
2. Run `/db.migrate "description"` to generate migration
3. Review generated file in `backend/alembic/versions/`
4. Run `/db.migrate upgrade` to apply
5. Verify changes in database

## Environment Variables
```bash
DATABASE_URL=postgresql://...@neon.tech/db
```

## Common Operations

### Check Current Version
```
/db.migrate status
```

### Create New Migration
```
/db.migrate "Add priority field to tasks"
```

### Apply All Pending
```
/db.migrate upgrade
```

### Rollback Last Migration
```
/db.migrate downgrade
```

## Safety Checks
- Always review auto-generated migrations
- Test migrations on development database first
- Backup production database before applying
- Use `/db.migrate downgrade` if issues occur

## Related Files
- `backend/alembic/` - Migration files
- `backend/app/models.py` - SQLModel definitions
- `backend/alembic/env.py` - Alembic configuration

## Related Agents
- `.claude/agents/database.md`
- `.claude/agents/deployment.md`

---

**Tip**: Run `/db.migrate upgrade` after pulling code to sync database schema.
