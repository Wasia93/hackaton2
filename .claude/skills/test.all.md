# Skill: test.all

## Description
Run all tests across frontend and backend

## Usage
```
/test.all
```

## What It Does
- Runs backend tests with pytest
- Runs frontend tests with Jest/Vitest
- Generates coverage reports
- Displays test results summary

## Commands Executed
```bash
# Backend tests
cd backend && uv run pytest --cov=app --cov-report=term-missing

# Frontend tests
cd frontend && npm test -- --coverage

# Display summary
echo "✅ All tests complete"
```

## Prerequisites
- Testing frameworks installed
- Test files written
- Test database configured (for integration tests)
- Environment variables set

## Test Coverage Targets
- Backend: 80%+
- Frontend: 80%+
- Critical paths: 100%

## Output
- Terminal: Test results and coverage percentages
- Coverage reports:
  - Backend: `backend/htmlcov/index.html`
  - Frontend: `frontend/coverage/index.html`

## Test Types Run
- **Unit Tests**: Individual function/component tests
- **Integration Tests**: API endpoint tests
- **Component Tests**: React component tests
- **E2E Tests**: (if `--e2e` flag passed)

## Flags
```
/test.all --fast     # Skip slow tests
/test.all --e2e      # Include E2E tests
/test.all --unit     # Unit tests only
```

## Related Files
- `backend/tests/` - Backend test files
- `frontend/__tests__/` - Frontend test files

## Related Agents
- `.claude/agents/testing.md`

---

**Tip**: Run this before committing to ensure all tests pass.
