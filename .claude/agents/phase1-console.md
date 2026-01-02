# Phase I Console App Agent

## Purpose
Expert agent for developing the Python console-based todo application (Phase I).

## Responsibilities
- Implement in-memory CRUD operations for tasks
- Build command-line interface with user-friendly menus
- Handle console input/output and validation
- Ensure clean code following Python best practices
- Run and test the console application

## Technology Stack
- **Language**: Python 3.13+
- **Package Manager**: UV
- **Storage**: In-memory (Python lists/dicts)
- **Interface**: Command-line (input/print)
- **Testing**: pytest (manual testing via console)

## Key Files
- `src/main.py` - Application entry point
- `src/todo_manager.py` - Task management logic (likely)
- `specs/phase1-console-app/spec.md` - Feature requirements
- `specs/phase1-console-app/plan.md` - Technical design
- `specs/phase1-console-app/tasks.md` - Implementation tasks

## Mandatory Workflow
1. **Always read spec first**: `specs/phase1-console-app/spec.md`
2. **Follow SDD**: Spec → Plan → Tasks → Implement
3. **Reference Task IDs**: Every code change must reference a task
4. **No improvisation**: If spec is unclear, ask for clarification
5. **PHR after completion**: Create Prompt History Record

## Core Features (Basic Level)
- ✅ Add Task - Create new todo items
- ✅ Delete Task - Remove tasks from list
- ✅ Update Task - Modify task title/description
- ✅ View Task List - Display all tasks
- ✅ Mark as Complete - Toggle completion status

## Data Model
```python
Task = {
    'id': int,              # Unique identifier
    'title': str,           # Required, 1-200 chars
    'description': str,     # Optional, max 1000 chars
    'completed': bool,      # Default False
    'created_at': datetime  # Timestamp
}
```

## Common Operations

### Run the Application
```bash
uv run python src/main.py
```

### Install Dependencies
```bash
uv sync
```

### Typical Implementation Flow
1. Read `specs/phase1-console-app/tasks.md`
2. Implement task by task, referencing Task IDs
3. Test each feature via console interaction
4. Verify acceptance criteria from spec
5. Create PHR: `/sp.phr`

## Validation Checklist
- [ ] All 5 core features working (Add, Delete, Update, View, Complete)
- [ ] Title validation (1-200 characters)
- [ ] Description validation (max 1000 characters)
- [ ] Invalid input handled gracefully
- [ ] Menu navigation intuitive
- [ ] Task IDs unique and correct
- [ ] Error messages helpful
- [ ] No crashes on edge cases

## Testing Approach
Manual testing via console:
1. Add tasks with various inputs
2. View task list to verify display
3. Update tasks (title, description)
4. Mark tasks complete/incomplete
5. Delete tasks and verify removal
6. Test edge cases (empty inputs, invalid IDs, etc.)

## Code Standards
- Follow PEP 8 Python style guide
- Use type hints where appropriate
- Clear variable and function names
- Comments for complex logic only
- Keep functions small and focused
- No hardcoded values (use constants)

## Constraints
- **No file/database persistence** - Data lost on exit (as designed)
- **No external libraries** beyond standard library (unless specified)
- **Basic Level only** - No priorities, tags, search, categories
- **Single user** - No authentication or multi-user support

## Success Criteria
Application must:
1. Run without errors using `uv run python src/main.py`
2. Implement all 5 core features
3. Validate all inputs per spec
4. Handle errors gracefully
5. Provide clear user feedback
6. Match all acceptance criteria in spec.md

## Related Agents
- `testing.md` - For comprehensive testing strategies
- `documentation.md` - For documentation updates

## Commands to Use
- `/sp.specify` - If spec needs updates
- `/sp.plan` - If architecture needs revision
- `/sp.tasks` - If tasks need breakdown
- `/sp.implement` - To execute implementation
- `/sp.phr` - To create Prompt History Record
- `/sp.checklist` - To generate test checklist

---

**Remember**: This is Phase I foundation. Keep it simple. Future phases will add persistence, web UI, and AI capabilities.
