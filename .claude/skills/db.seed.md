# Skill: db.seed

## Description
Seed database with development/test data

## Usage
```
/db.seed
/db.seed --clear  # Clear existing data first
```

## What It Does
- Creates sample users (if needed)
- Creates sample tasks for testing
- Creates sample conversations (Phase III+)
- Optionally clears existing data

## Commands Executed
```bash
cd backend
uv run python scripts/seed.py
```

## Prerequisites
- Database migrations applied
- Seed script exists (`scripts/seed.py`)
- DATABASE_URL configured
- Database connection working

## Sample Data Created
- **Users**: 2-3 test users
- **Tasks**: 10-15 sample tasks per user
  - Mix of completed/incomplete
  - Various titles and descriptions
  - Different priorities (Phase II+)
- **Conversations**: 2-3 conversations per user (Phase III+)
- **Messages**: Sample chat history (Phase III+)

## Test Users Created
```
User 1:
  ID: test-user-123
  Email: test@example.com
  Password: password123

User 2:
  ID: test-user-456
  Email: alice@example.com
  Password: password123
```

## Flags
- `--clear` - Drop all existing data before seeding
- `--users` - Seed users only
- `--tasks` - Seed tasks only
- `--minimal` - Create minimal data set (3 tasks)

## Safety Warning
**Do NOT run on production database!**
This is for development/testing only.

## Use Cases
- Fresh development environment setup
- Testing multi-user scenarios
- Populating demo environment
- Testing pagination/filtering
- E2E test data setup

## Related Files
- `backend/scripts/seed.py` - Seed script
- `backend/app/models.py` - Data models

## Related Agents
- `.claude/agents/database.md`
- `.claude/agents/testing.md`

---

**Tip**: Run `/db.seed` after database setup for quick testing data.
