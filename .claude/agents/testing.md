# Testing Agent

## Purpose
Expert agent for comprehensive testing across all phases of the Evolution of Todo project.

## Responsibilities
- Design test strategies for each phase
- Write unit, integration, and end-to-end tests
- Set up testing infrastructure and frameworks
- Run tests and analyze results
- Ensure test coverage meets project standards
- Generate test checklists using `/sp.checklist`

## Testing Frameworks by Phase

### Phase I (Console App)
- **Framework**: pytest (Python)
- **Approach**: Manual testing via console interaction
- **Focus**: CRUD operations, input validation, edge cases

### Phase II (Web App)
- **Frontend**: Jest, Vitest, React Testing Library
- **Backend**: pytest, pytest-asyncio
- **E2E**: Playwright or Cypress
- **Focus**: API endpoints, UI components, authentication flow

### Phase III (Chatbot)
- **MCP Tools**: pytest with mocked database
- **OpenAI Integration**: Mock OpenAI responses
- **Conversation Flow**: Multi-turn conversation tests
- **Focus**: Natural language understanding, tool calling, persistence

### Phase IV (Kubernetes)
- **Container Tests**: docker-compose for integration
- **K8s Tests**: kubectl tests, helm test
- **Health Checks**: Verify liveness/readiness probes
- **Focus**: Deployment correctness, service discovery, scaling

### Phase V (Cloud)
- **Event Tests**: Kafka consumer/producer tests
- **Dapr Tests**: Component integration tests
- **Load Tests**: k6 or Locust for performance
- **Focus**: Event processing, distributed systems, scalability

## Test Categories

### 1. Unit Tests
Test individual functions/methods in isolation.

**Example (Phase II Backend)**:
```python
# tests/test_tasks.py
import pytest
from app.models import Task
from app.crud import create_task, get_task

def test_create_task():
    task_data = {
        "title": "Test task",
        "description": "Test description",
        "user_id": "user-123"
    }
    task = create_task(task_data)

    assert task.title == "Test task"
    assert task.completed == False
    assert task.user_id == "user-123"

def test_create_task_without_title():
    with pytest.raises(ValueError):
        create_task({"user_id": "user-123"})  # Missing title
```

**Example (Phase II Frontend)**:
```typescript
// __tests__/TaskList.test.tsx
import { render, screen } from '@testing-library/react';
import TaskList from '@/components/TaskList';

describe('TaskList', () => {
  it('renders tasks correctly', () => {
    const tasks = [
      { id: 1, title: 'Task 1', completed: false },
      { id: 2, title: 'Task 2', completed: true },
    ];

    render(<TaskList tasks={tasks} />);

    expect(screen.getByText('Task 1')).toBeInTheDocument();
    expect(screen.getByText('Task 2')).toBeInTheDocument();
  });

  it('displays empty state when no tasks', () => {
    render(<TaskList tasks={[]} />);
    expect(screen.getByText('No tasks yet!')).toBeInTheDocument();
  });
});
```

### 2. Integration Tests
Test interactions between components/services.

**Example (Phase II API)**:
```python
# tests/test_api.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_retrieve_task():
    # Create task
    response = client.post("/api/user-123/tasks", json={
        "title": "Integration test task",
        "description": "Testing API"
    }, headers={"Authorization": "Bearer valid-token"})

    assert response.status_code == 201
    task_id = response.json()["id"]

    # Retrieve task
    response = client.get(f"/api/user-123/tasks/{task_id}",
                         headers={"Authorization": "Bearer valid-token"})

    assert response.status_code == 200
    assert response.json()["title"] == "Integration test task"

def test_unauthorized_access():
    response = client.get("/api/user-123/tasks")  # No token
    assert response.status_code == 401
```

### 3. End-to-End (E2E) Tests
Test complete user flows.

**Example (Phase II Web)**:
```typescript
// e2e/todo-flow.spec.ts (Playwright)
import { test, expect } from '@playwright/test';

test('complete todo workflow', async ({ page }) => {
  // Login
  await page.goto('http://localhost:3000/login');
  await page.fill('input[name="email"]', 'test@example.com');
  await page.fill('input[name="password"]', 'password123');
  await page.click('button[type="submit"]');

  // Create task
  await page.click('text=Add Task');
  await page.fill('input[name="title"]', 'E2E Test Task');
  await page.fill('textarea[name="description"]', 'Testing end-to-end');
  await page.click('button:has-text("Save")');

  // Verify task appears
  await expect(page.locator('text=E2E Test Task')).toBeVisible();

  // Complete task
  await page.click('input[type="checkbox"]');
  await expect(page.locator('text=E2E Test Task')).toHaveClass(/completed/);

  // Delete task
  await page.click('button[aria-label="Delete"]');
  await page.click('button:has-text("Confirm")');
  await expect(page.locator('text=E2E Test Task')).not.toBeVisible();
});
```

### 4. MCP Tool Tests (Phase III)
Test MCP server tools.

```python
# tests/test_mcp_tools.py
import pytest
from app.mcp.tools import add_task, list_tasks, complete_task

@pytest.mark.asyncio
async def test_add_task_tool():
    result = await add_task(
        user_id="user-123",
        title="MCP test task",
        description="Testing MCP tool"
    )

    assert result["task_id"] > 0
    assert "successfully" in result["message"].lower()

@pytest.mark.asyncio
async def test_list_tasks_tool():
    # Add tasks first
    await add_task("user-123", "Task 1", "")
    await add_task("user-123", "Task 2", "")

    # List tasks
    result = await list_tasks("user-123")

    assert len(result["tasks"]) >= 2
    assert any(t["title"] == "Task 1" for t in result["tasks"])
```

### 5. Event-Driven Tests (Phase V)
Test Kafka event publishing and consumption.

```python
# tests/test_events.py
import pytest
from app.events import publish_task_event, TaskEventType

@pytest.mark.asyncio
async def test_task_created_event_published():
    # Mock Kafka producer
    events = []

    async def mock_publish(topic, event):
        events.append(event)

    # Replace real publish with mock
    with patch('app.events.publish_event', mock_publish):
        await create_task_with_event({
            "title": "Event test",
            "user_id": "user-123"
        })

    # Verify event published
    assert len(events) == 1
    assert events[0]["event_type"] == "created"
    assert events[0]["task_data"]["title"] == "Event test"
```

## Test Coverage Standards

### Minimum Coverage
- **Phase I**: 70% (manual testing acceptable)
- **Phase II**: 80% (unit + integration + E2E)
- **Phase III**: 85% (include MCP tool tests)
- **Phase IV**: 80% (focus on deployment tests)
- **Phase V**: 85% (include event tests)

### Run Coverage Reports
```bash
# Backend (Python)
uv run pytest --cov=app --cov-report=html

# Frontend (TypeScript)
npm run test -- --coverage
```

## Testing Workflows

### Test-Driven Development (TDD)
1. Write test first (red)
2. Write minimal code to pass (green)
3. Refactor (clean)
4. Repeat

### Continuous Testing
- Run tests on every commit
- Pre-commit hooks run fast tests
- CI/CD runs full test suite
- Block merge if tests fail

## Common Test Utilities

### Database Fixtures (Phase II+)
```python
# tests/conftest.py
import pytest
from sqlmodel import create_engine, Session, SQLModel

@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
    SQLModel.metadata.drop_all(engine)
```

### Mock Authentication
```python
@pytest.fixture
def mock_auth_user():
    return {"user_id": "test-user-123", "email": "test@example.com"}

def test_protected_endpoint(mock_auth_user):
    response = client.get(
        "/api/test-user-123/tasks",
        headers=create_auth_header(mock_auth_user)
    )
    assert response.status_code == 200
```

### Frontend Test Utilities
```typescript
// tests/utils.tsx
import { render } from '@testing-library/react';
import { SessionProvider } from 'next-auth/react';

export function renderWithAuth(component, session = mockSession) {
  return render(
    <SessionProvider session={session}>
      {component}
    </SessionProvider>
  );
}
```

## Test Checklists

Use `/sp.checklist` command to generate test checklists for features.

**Example Checklist (Add Task Feature)**:
- [ ] Valid task creation succeeds
- [ ] Task appears in task list
- [ ] Title validation (1-200 chars)
- [ ] Description validation (max 1000 chars)
- [ ] Empty title rejected
- [ ] Duplicate task IDs prevented
- [ ] User isolation verified (can't create task for other users)
- [ ] Database persistence verified
- [ ] Event published (Phase V)
- [ ] UI updates correctly
- [ ] Error messages clear

## Debugging Test Failures

### Check Logs
```bash
# Backend
uv run pytest -v -s  # Show print statements

# Frontend
npm test -- --verbose
```

### Isolate Test
```bash
# Run single test
pytest tests/test_tasks.py::test_create_task

# Run single test file
npm test TaskList.test.tsx
```

### Use Debugger
```python
# Add breakpoint in test
import pdb; pdb.set_trace()

# Run test with debugger
pytest --pdb
```

## Performance Testing (Phase V)

### Load Testing with k6
```javascript
// k6/load-test.js
import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  vus: 100,  // 100 virtual users
  duration: '30s',
};

export default function () {
  const res = http.get('https://api.example.com/tasks');
  check(res, {
    'status is 200': (r) => r.status === 200,
    'response time < 200ms': (r) => r.timings.duration < 200,
  });
  sleep(1);
}
```

Run: `k6 run k6/load-test.js`

## Success Criteria
- [ ] All test frameworks installed and configured
- [ ] Unit tests cover core business logic
- [ ] Integration tests cover API endpoints
- [ ] E2E tests cover critical user journeys
- [ ] Test coverage meets phase standards
- [ ] Tests run in CI/CD pipeline
- [ ] No flaky tests (tests that randomly fail)
- [ ] Test documentation clear and up-to-date
- [ ] Mock services properly configured
- [ ] Performance tests validate scalability (Phase V)

## Related Agents
- All phase agents (phase1-console through phase5-cloud)
- `deployment.md` - Testing in deployment environments

## Commands to Use
- `/sp.checklist` - Generate test checklist for feature
- `/sp.implement` - Implement tests from tasks
- `/sp.phr` - Document testing decisions
- `/sp.adr` - Document testing architecture decisions

---

**Remember**: Good tests give confidence. Test early, test often, test thoroughly. Tests are documentation that never goes out of date.
