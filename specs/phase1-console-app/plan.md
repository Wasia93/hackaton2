# Phase I: Todo Console App - Technical Plan

**Feature**: In-Memory Python Console Todo Application
**Phase**: Phase I - Console App
**Status**: Draft
**Created**: 2025-12-15
**Updated**: 2025-12-15

**References**:
- [Specification](./spec.md) - WHAT to build
- [Constitution](../../.specify/memory/constitution.md) - Project principles

---

## 1. Architecture Overview

### 1.1 System Architecture

```
┌─────────────────────────────────────────────────┐
│           Todo Console Application              │
│                                                 │
│  ┌──────────────┐         ┌─────────────────┐  │
│  │              │         │                 │  │
│  │   CLI Layer  │────────▶│  Business Logic │  │
│  │   (main.py)  │         │  (todo_manager) │  │
│  │              │         │                 │  │
│  └──────────────┘         └────────┬────────┘  │
│                                    │           │
│                                    ▼           │
│                           ┌─────────────────┐  │
│                           │                 │  │
│                           │   Data Layer    │  │
│                           │  (task_storage) │  │
│                           │                 │  │
│                           └─────────────────┘  │
│                                    │           │
│                                    ▼           │
│                           ┌─────────────────┐  │
│                           │                 │  │
│                           │   Task Model    │  │
│                           │   (dataclass)   │  │
│                           │                 │  │
│                           └─────────────────┘  │
└─────────────────────────────────────────────────┘
```

### 1.2 Design Principles

**Separation of Concerns**:
- **CLI Layer**: User interface, input/output, menu display
- **Business Logic**: CRUD operations, validation, business rules
- **Data Layer**: In-memory storage management
- **Data Model**: Task structure definition

**Single Responsibility**:
- Each module handles one aspect of the application
- Functions are small, focused, and testable
- Clear boundaries between layers

**Simplicity**:
- No over-engineering for Phase I
- Use Python standard library only (no external dependencies for core functionality)
- Straightforward data structures (list of Task objects)

---

## 2. Component Breakdown

### 2.1 Module Structure

```
src/
├── main.py              # Entry point, CLI interface
├── models/
│   └── task.py          # Task data model
├── services/
│   └── todo_manager.py  # Business logic (CRUD operations)
└── utils/
    └── validators.py    # Input validation functions
```

### 2.2 Component Specifications

#### Component: Task Model (`src/models/task.py`)

**Responsibility**: Define Task data structure

**Implementation**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str
    completed: bool
    created_at: datetime
```

**Key Points**:
- Use Python dataclass for clean, immutable-ish structure
- Type hints for all fields
- Automatic __init__, __repr__, __eq__ methods

---

#### Component: Todo Manager (`src/services/todo_manager.py`)

**Responsibility**: Manage task storage and CRUD operations

**Key Functions**:

1. **`__init__()`**
   - Initialize empty task list
   - Set next_id counter to 1

2. **`add_task(title: str, description: str = "") -> Task`**
   - Validate title (length, not empty)
   - Validate description (length if provided)
   - Create Task with auto-increment ID
   - Store in task list
   - Return created Task

3. **`get_all_tasks() -> list[Task]`**
   - Return all tasks
   - Return empty list if no tasks

4. **`get_task_by_id(task_id: int) -> Task | None`**
   - Search for task by ID
   - Return Task if found, None otherwise

5. **`update_task(task_id: int, title: str | None = None, description: str | None = None) -> Task | None`**
   - Find task by ID
   - Update title if provided (with validation)
   - Update description if provided (with validation)
   - Return updated Task or None if not found

6. **`delete_task(task_id: int) -> bool`**
   - Find and remove task by ID
   - Return True if deleted, False if not found

7. **`toggle_complete(task_id: int) -> Task | None`**
   - Find task by ID
   - Toggle completed status (True ↔ False)
   - Return updated Task or None if not found

**Data Storage**:
- Use Python list: `self.tasks: list[Task] = []`
- Use integer counter: `self.next_id: int = 1`
- No persistence mechanism (in-memory only)

---

#### Component: Validators (`src/utils/validators.py`)

**Responsibility**: Input validation logic

**Key Functions**:

1. **`validate_title(title: str) -> tuple[bool, str]`**
   - Check not empty
   - Check length <= 200
   - Return (is_valid, error_message)

2. **`validate_description(description: str) -> tuple[bool, str]`**
   - Check length <= 1000
   - Return (is_valid, error_message)

3. **`validate_task_id(task_id_str: str) -> tuple[bool, int, str]`**
   - Check is numeric
   - Check is positive integer
   - Return (is_valid, task_id, error_message)

**Design Pattern**:
- Return tuple: (success_bool, value/error_message)
- Caller decides how to handle validation failure
- Pure functions (no side effects)

---

#### Component: CLI Interface (`src/main.py`)

**Responsibility**: User interaction, menu display, input/output

**Key Functions**:

1. **`display_menu()`**
   - Print menu options (1-6)
   - Clear, formatted output

2. **`display_tasks(tasks: list[Task])`**
   - Print tasks in table format
   - Show: ID | Title | Status | Created
   - Use ✓ for completed, ✗ for incomplete
   - Handle empty list with friendly message

3. **`handle_add_task(manager: TodoManager)`**
   - Prompt for title
   - Prompt for description
   - Validate inputs
   - Call manager.add_task()
   - Display success/error message

4. **`handle_view_tasks(manager: TodoManager)`**
   - Get all tasks from manager
   - Call display_tasks()

5. **`handle_update_task(manager: TodoManager)`**
   - Display current tasks
   - Prompt for task ID
   - Validate ID
   - Prompt for new title (Enter to skip)
   - Prompt for new description (Enter to skip)
   - Call manager.update_task()
   - Display success/error message

6. **`handle_delete_task(manager: TodoManager)`**
   - Display current tasks
   - Prompt for task ID
   - Validate ID
   - Ask for confirmation (y/n)
   - Call manager.delete_task()
   - Display success/error message

7. **`handle_toggle_complete(manager: TodoManager)`**
   - Display current tasks
   - Prompt for task ID
   - Validate ID
   - Call manager.toggle_complete()
   - Display success/error message

8. **`main()`**
   - Initialize TodoManager
   - Loop: display menu, get choice, route to handler
   - Exit on option 6

**Design Patterns**:
- Use handler functions for each menu option
- Single responsibility per function
- Clear separation between UI and business logic

---

## 3. Data Flow

### 3.1 Add Task Flow

```
User Input (Title, Description)
    │
    ▼
Validate in CLI (handle_add_task)
    │
    ▼
Validate in Validators (validate_title, validate_description)
    │
    ▼
TodoManager.add_task(title, description)
    │
    ├─ Create Task object with auto-increment ID
    ├─ Set completed = False
    ├─ Set created_at = now
    ├─ Append to self.tasks list
    └─ Increment self.next_id
    │
    ▼
Return Task object
    │
    ▼
Display success message in CLI
```

### 3.2 View Tasks Flow

```
User selects "View Tasks"
    │
    ▼
TodoManager.get_all_tasks()
    │
    └─ Return self.tasks (list)
    │
    ▼
CLI displays in table format
    │
    ├─ Loop through tasks
    ├─ Format each: ID | Title | Status | Created
    └─ Print to console
```

### 3.3 Update Task Flow

```
User Input (Task ID, New Title, New Description)
    │
    ▼
Validate Task ID in CLI
    │
    ▼
TodoManager.update_task(task_id, title, description)
    │
    ├─ Find task by ID
    ├─ If not found: return None
    ├─ If found:
    │   ├─ Validate new title (if provided)
    │   ├─ Validate new description (if provided)
    │   ├─ Update task fields
    │   └─ Return updated Task
    │
    ▼
Display success/error message in CLI
```

### 3.4 Delete Task Flow

```
User Input (Task ID) + Confirmation
    │
    ▼
Validate Task ID in CLI
    │
    ▼
Prompt for confirmation (y/n)
    │
    ▼
If confirmed:
    TodoManager.delete_task(task_id)
        │
        ├─ Find task by ID
        ├─ If found: remove from list, return True
        └─ If not found: return False
        │
        ▼
    Display success/error message
```

### 3.5 Toggle Complete Flow

```
User Input (Task ID)
    │
    ▼
Validate Task ID in CLI
    │
    ▼
TodoManager.toggle_complete(task_id)
    │
    ├─ Find task by ID
    ├─ If not found: return None
    ├─ If found:
    │   ├─ Toggle task.completed (True ↔ False)
    │   └─ Return updated Task
    │
    ▼
Display success message with new status
```

---

## 4. Error Handling Strategy

### 4.1 Input Validation Errors

**Strategy**: Validate early, fail fast, provide helpful messages

**Examples**:
- Empty title → "ERROR: Title is required"
- Title too long → "ERROR: Title must be 200 characters or less"
- Description too long → "ERROR: Description must be 1000 characters or less"
- Invalid task ID → "ERROR: Task not found with ID {id}"
- Non-numeric input → "ERROR: Please enter a valid number"

### 4.2 Operation Errors

**Task Not Found**:
```python
if task is None:
    print(f"ERROR: Task not found with ID {task_id}")
    return
```

**Empty Task List**:
```python
if not tasks:
    print("No tasks yet! Add your first task to get started.")
    return
```

### 4.3 User Input Errors

**Handle keyboard interrupts gracefully**:
```python
try:
    # user input code
except KeyboardInterrupt:
    print("\nOperation cancelled")
    return
```

---

## 5. Interface Design

### 5.1 Menu Display

```
========================================
        TODO LIST MANAGER
========================================

1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

Enter your choice (1-6): _
```

### 5.2 Task List Display

```
========================================
           YOUR TASKS
========================================

ID  | Title                  | Status | Created
----|------------------------|--------|------------------
1   | Buy groceries          | ✗      | 2025-12-15 10:30
2   | Call dentist           | ✓      | 2025-12-15 11:15
3   | Finish hackathon       | ✗      | 2025-12-15 14:22

Total: 3 tasks (1 completed, 2 pending)
```

### 5.3 Success Messages

```
✓ Task added successfully! (ID: 3)
✓ Task updated successfully!
✓ Task deleted successfully!
✓ Task marked as complete!
✓ Task marked as incomplete!
```

### 5.4 Error Messages

```
✗ ERROR: Title is required
✗ ERROR: Task not found with ID 5
✗ ERROR: Title must be 200 characters or less
```

---

## 6. Implementation Strategy

### 6.1 Development Order

**Step 1**: Create Task model (`src/models/task.py`)
- Define dataclass
- Add type hints
- Test with sample creation

**Step 2**: Create Validators (`src/utils/validators.py`)
- Implement validation functions
- Test with various inputs

**Step 3**: Create TodoManager (`src/services/todo_manager.py`)
- Implement __init__
- Implement add_task (with validation)
- Implement get_all_tasks
- Implement get_task_by_id
- Implement update_task
- Implement delete_task
- Implement toggle_complete

**Step 4**: Create CLI Interface (`src/main.py`)
- Implement display_menu
- Implement display_tasks
- Implement handle_add_task
- Implement handle_view_tasks
- Implement handle_update_task
- Implement handle_delete_task
- Implement handle_toggle_complete
- Implement main loop

**Step 5**: Integration & Testing
- Run application
- Test each CRUD operation
- Verify validation works
- Check edge cases

### 6.2 Testing Approach

**Manual Testing** (Phase I - no automated tests required):
1. Add multiple tasks
2. View tasks (verify display)
3. Update task (title, description, both)
4. Delete task (with confirmation)
5. Toggle completion status
6. Test validation (empty title, too long, invalid ID)
7. Test edge cases (no tasks, delete all tasks)

**Test Cases**:
- TC-1: Add task with title only
- TC-2: Add task with title and description
- TC-3: Add task with empty title (should fail)
- TC-4: Add task with title > 200 chars (should fail)
- TC-5: View tasks when empty
- TC-6: View tasks with multiple tasks
- TC-7: Update task title
- TC-8: Update task description
- TC-9: Update task with invalid ID (should fail)
- TC-10: Delete task with confirmation
- TC-11: Delete task cancelled
- TC-12: Delete task with invalid ID (should fail)
- TC-13: Toggle task to complete
- TC-14: Toggle task to incomplete
- TC-15: Exit application

---

## 7. Technology Stack

### 7.1 Core Technologies

- **Language**: Python 3.13+
- **Package Manager**: UV
- **Data Structure**: Python list and dataclass
- **Type System**: Python type hints

### 7.2 Standard Library Modules

- `dataclasses` - Task model
- `datetime` - Timestamps
- `typing` - Type hints (list, Optional, Union)

### 7.3 Development Tools

- **Formatter**: Black (code formatting)
- **Linter**: Ruff (code linting)
- **Type Checker**: mypy (optional, for strict typing)

---

## 8. File Structure

```
hackaton2/
├── src/
│   ├── __init__.py
│   ├── main.py                    # CLI entry point
│   ├── models/
│   │   ├── __init__.py
│   │   └── task.py                # Task dataclass
│   ├── services/
│   │   ├── __init__.py
│   │   └── todo_manager.py        # CRUD operations
│   └── utils/
│       ├── __init__.py
│       └── validators.py          # Input validation
├── specs/
│   └── phase1-console-app/
│       ├── spec.md                # This document's companion
│       ├── plan.md                # This document
│       └── tasks.md               # Atomic tasks (next step)
├── pyproject.toml                 # UV configuration
├── README.md                      # Setup instructions
└── .gitignore                     # Git ignore rules
```

---

## 9. Performance Considerations

### 9.1 Memory Usage

- **Expected**: < 1 MB for typical usage (< 1000 tasks)
- **Implementation**: Simple list storage
- **Optimization**: Not needed for Phase I

### 9.2 Response Time

- **Target**: All operations < 100ms
- **Implementation**: In-memory operations are instant
- **Bottleneck**: None (no I/O, no network calls)

---

## 10. Security Considerations

### 10.1 Input Validation

- **Threat**: Malformed input crashing application
- **Mitigation**: Validate all user inputs before processing
- **Implementation**: validators.py module

### 10.2 Data Integrity

- **Threat**: Task ID collision
- **Mitigation**: Auto-increment ID, never reuse deleted IDs
- **Implementation**: TodoManager.next_id counter

---

## 11. Future Phase Compatibility

### 11.1 Phase II Preparation

**Database Migration**:
- Task model already matches future database schema
- CRUD operations can be adapted to SQLModel ORM
- Validation logic reusable

**API Endpoints**:
- TodoManager methods map directly to REST API endpoints
- Business logic separates from CLI (easy to add FastAPI layer)

### 11.2 Design Decisions for Future

- Use dataclass (compatible with SQLModel)
- Separate business logic from UI (reusable in API)
- Validation functions (reusable in API layer)
- Return objects instead of printing (composable)

---

## 12. Open Questions

**Q1**: Should we add logging?
**A1**: Not for Phase I (keep it simple), add in Phase II

**Q2**: Should tasks be sorted by creation date?
**A2**: Display in creation order (list order), add sorting in Phase II

**Q3**: Should we handle very long titles in display?
**A3**: Truncate in display if > 50 chars, show full in details

---

## 13. Architectural Decision Records

**ADR-001**: Use Dataclass for Task Model
- **Decision**: Use Python dataclass instead of regular class
- **Rationale**: Cleaner code, automatic methods, future SQLModel compatibility
- **Alternatives**: Regular class, dict, NamedTuple
- **Impact**: Easier maintenance, better type safety

**ADR-002**: In-Memory List Storage
- **Decision**: Use Python list for task storage
- **Rationale**: Simple, sufficient for Phase I, no external dependencies
- **Alternatives**: File storage, SQLite database
- **Impact**: Data lost on exit (acceptable for Phase I)

**ADR-003**: Separation of Concerns (3-Layer Architecture)
- **Decision**: Separate CLI, Business Logic, and Data Model
- **Rationale**: Maintainability, testability, future extensibility
- **Alternatives**: Single-file monolith
- **Impact**: More files, but cleaner codebase

---

## 14. Success Criteria

This plan is successful when:
- ✅ All components defined clearly
- ✅ Implementation order specified
- ✅ Error handling strategy documented
- ✅ Interface mockups provided
- ✅ Future compatibility considered
- ✅ Code can be generated by Claude Code following this plan

---

## 15. Next Steps

1. **Create Tasks** (`tasks.md`) - Break this plan into atomic work units
2. **Implement** - Generate code following task breakdown
3. **Test** - Verify all acceptance criteria from spec.md
4. **Push to GitHub** - Version control and backup

---

**Plan Version**: 1.0.0
**Created**: 2025-12-15
**Last Updated**: 2025-12-15
**Status**: Ready for Task Breakdown
