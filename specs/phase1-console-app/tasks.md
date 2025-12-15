# Phase I: Todo Console App - Task Breakdown

**Feature**: In-Memory Python Console Todo Application
**Phase**: Phase I - Console App
**Status**: Ready for Implementation
**Created**: 2025-12-15
**Updated**: 2025-12-15

**References**:
- [Specification](./spec.md) - WHAT to build
- [Plan](./plan.md) - HOW to build

---

## Task Summary

| Task ID | Description | Status | Dependencies | Estimated Lines |
|---------|-------------|--------|--------------|-----------------|
| T-001 | Create project structure and __init__ files | ⬜ Pending | None | 10 |
| T-002 | Implement Task model (dataclass) | ⬜ Pending | T-001 | 20 |
| T-003 | Implement validators module | ⬜ Pending | None | 60 |
| T-004 | Implement TodoManager initialization | ⬜ Pending | T-002 | 15 |
| T-005 | Implement add_task method | ⬜ Pending | T-002, T-003, T-004 | 25 |
| T-006 | Implement get_all_tasks method | ⬜ Pending | T-004 | 10 |
| T-007 | Implement get_task_by_id method | ⬜ Pending | T-004 | 15 |
| T-008 | Implement update_task method | ⬜ Pending | T-003, T-007 | 30 |
| T-009 | Implement delete_task method | ⬜ Pending | T-007 | 20 |
| T-010 | Implement toggle_complete method | ⬜ Pending | T-007 | 15 |
| T-011 | Implement CLI display_menu function | ⬜ Pending | None | 20 |
| T-012 | Implement CLI display_tasks function | ⬜ Pending | T-002 | 40 |
| T-013 | Implement handle_add_task function | ⬜ Pending | T-005, T-011 | 30 |
| T-014 | Implement handle_view_tasks function | ⬜ Pending | T-006, T-012 | 15 |
| T-015 | Implement handle_update_task function | ⬜ Pending | T-008, T-012 | 45 |
| T-016 | Implement handle_delete_task function | ⬜ Pending | T-009, T-012 | 40 |
| T-017 | Implement handle_toggle_complete function | ⬜ Pending | T-010, T-012 | 30 |
| T-018 | Implement main function and program loop | ⬜ Pending | T-011, T-013-T-017 | 40 |

**Total Estimated Lines**: ~480 lines

---

## T-001: Create Project Structure and __init__ Files

**Priority**: CRITICAL
**Dependencies**: None
**Estimated Time**: 5 minutes

### Description
Create the directory structure and empty __init__.py files for proper Python package organization.

### Acceptance Criteria
- ✅ Directory `src/models/` exists
- ✅ Directory `src/services/` exists
- ✅ Directory `src/utils/` exists
- ✅ File `src/__init__.py` exists (can be empty)
- ✅ File `src/models/__init__.py` exists (can be empty)
- ✅ File `src/services/__init__.py` exists (can be empty)
- ✅ File `src/utils/__init__.py` exists (can be empty)

### Files to Create
- `src/__init__.py`
- `src/models/__init__.py`
- `src/services/__init__.py`
- `src/utils/__init__.py`

### Implementation Notes
All __init__.py files can be empty for Phase I.

---

## T-002: Implement Task Model (Dataclass)

**Priority**: CRITICAL
**Dependencies**: T-001
**Estimated Time**: 10 minutes
**File**: `src/models/task.py`

### Description
Create the Task dataclass with all required fields and type hints.

### Acceptance Criteria
- ✅ Task class is a dataclass
- ✅ Field `id: int` exists
- ✅ Field `title: str` exists
- ✅ Field `description: str` exists
- ✅ Field `completed: bool` exists with default False
- ✅ Field `created_at: datetime` exists
- ✅ All fields have proper type hints
- ✅ Import datetime from datetime module
- ✅ Import dataclass from dataclasses

### Expected Code Structure
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

### Testing
Create a sample task and verify all fields are set correctly.

---

## T-003: Implement Validators Module

**Priority**: CRITICAL
**Dependencies**: None
**Estimated Time**: 15 minutes
**File**: `src/utils/validators.py`

### Description
Create validation functions for title, description, and task ID.

### Acceptance Criteria
- ✅ Function `validate_title(title: str) -> tuple[bool, str]` exists
- ✅ validate_title checks for empty string
- ✅ validate_title checks for length <= 200
- ✅ Function `validate_description(description: str) -> tuple[bool, str]` exists
- ✅ validate_description checks for length <= 1000
- ✅ Function `validate_task_id(task_id_str: str) -> tuple[bool, int, str]` exists
- ✅ validate_task_id checks if input is numeric
- ✅ validate_task_id checks if input is positive integer
- ✅ All functions return appropriate error messages

### Expected Code Structure
```python
def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title.

    Returns:
        (is_valid, error_message)
    """
    if not title or title.strip() == "":
        return (False, "Title is required")
    if len(title) > 200:
        return (False, "Title must be 200 characters or less")
    return (True, "")

def validate_description(description: str) -> tuple[bool, str]:
    """Validate task description.

    Returns:
        (is_valid, error_message)
    """
    if len(description) > 1000:
        return (False, "Description must be 1000 characters or less")
    return (True, "")

def validate_task_id(task_id_str: str) -> tuple[bool, int, str]:
    """Validate and parse task ID.

    Returns:
        (is_valid, task_id, error_message)
    """
    try:
        task_id = int(task_id_str)
        if task_id <= 0:
            return (False, 0, "Task ID must be a positive number")
        return (True, task_id, "")
    except ValueError:
        return (False, 0, "Please enter a valid number")
```

### Testing
Test with various inputs: empty, too long, valid, invalid numbers.

---

## T-004: Implement TodoManager Initialization

**Priority**: CRITICAL
**Dependencies**: T-002
**Estimated Time**: 5 minutes
**File**: `src/services/todo_manager.py`

### Description
Create TodoManager class with initialization.

### Acceptance Criteria
- ✅ Class `TodoManager` exists
- ✅ `__init__` method initializes `self.tasks` as empty list
- ✅ `__init__` method initializes `self.next_id` as 1
- ✅ Proper imports from models.task

### Expected Code Structure
```python
from datetime import datetime
from typing import Optional
from src.models.task import Task

class TodoManager:
    def __init__(self):
        """Initialize the todo manager with empty task list."""
        self.tasks: list[Task] = []
        self.next_id: int = 1
```

### Testing
Create instance and verify tasks is empty list and next_id is 1.

---

## T-005: Implement add_task Method

**Priority**: CRITICAL
**Dependencies**: T-002, T-003, T-004
**Estimated Time**: 15 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to add a new task with validation.

### Acceptance Criteria
- ✅ Method `add_task(self, title: str, description: str = "") -> Task` exists
- ✅ Validates title using validators.validate_title
- ✅ Validates description using validators.validate_description
- ✅ Raises ValueError if validation fails
- ✅ Creates Task with auto-increment ID
- ✅ Sets completed to False
- ✅ Sets created_at to current datetime
- ✅ Appends task to self.tasks
- ✅ Increments self.next_id
- ✅ Returns created Task

### Expected Code Structure
```python
def add_task(self, title: str, description: str = "") -> Task:
    """Add a new task.

    Args:
        title: Task title (required, max 200 chars)
        description: Task description (optional, max 1000 chars)

    Returns:
        Created Task object

    Raises:
        ValueError: If validation fails
    """
    from src.utils.validators import validate_title, validate_description

    # Validate title
    is_valid, error_msg = validate_title(title)
    if not is_valid:
        raise ValueError(error_msg)

    # Validate description
    is_valid, error_msg = validate_description(description)
    if not is_valid:
        raise ValueError(error_msg)

    # Create task
    task = Task(
        id=self.next_id,
        title=title.strip(),
        description=description.strip(),
        completed=False,
        created_at=datetime.now()
    )

    self.tasks.append(task)
    self.next_id += 1

    return task
```

### Testing
- Add task with valid title only
- Add task with title and description
- Try to add task with empty title (should raise ValueError)
- Try to add task with title > 200 chars (should raise ValueError)

---

## T-006: Implement get_all_tasks Method

**Priority**: CRITICAL
**Dependencies**: T-004
**Estimated Time**: 5 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to retrieve all tasks.

### Acceptance Criteria
- ✅ Method `get_all_tasks(self) -> list[Task]` exists
- ✅ Returns list of all tasks
- ✅ Returns empty list if no tasks

### Expected Code Structure
```python
def get_all_tasks(self) -> list[Task]:
    """Get all tasks.

    Returns:
        List of all Task objects
    """
    return self.tasks
```

### Testing
- Get tasks when empty (should return [])
- Add tasks and get all (should return all tasks)

---

## T-007: Implement get_task_by_id Method

**Priority**: CRITICAL
**Dependencies**: T-004
**Estimated Time**: 10 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to find a task by ID.

### Acceptance Criteria
- ✅ Method `get_task_by_id(self, task_id: int) -> Optional[Task]` exists
- ✅ Returns Task if found
- ✅ Returns None if not found
- ✅ Searches by task.id

### Expected Code Structure
```python
def get_task_by_id(self, task_id: int) -> Optional[Task]:
    """Find a task by ID.

    Args:
        task_id: Task ID to search for

    Returns:
        Task if found, None otherwise
    """
    for task in self.tasks:
        if task.id == task_id:
            return task
    return None
```

### Testing
- Get existing task by ID (should return task)
- Get non-existent task (should return None)

---

## T-008: Implement update_task Method

**Priority**: CRITICAL
**Dependencies**: T-003, T-007
**Estimated Time**: 20 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to update a task's title and/or description.

### Acceptance Criteria
- ✅ Method `update_task(self, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Optional[Task]` exists
- ✅ Finds task by ID
- ✅ Returns None if task not found
- ✅ Updates title if provided (with validation)
- ✅ Updates description if provided (with validation)
- ✅ Does not update if parameter is None
- ✅ Raises ValueError if validation fails
- ✅ Returns updated Task

### Expected Code Structure
```python
def update_task(
    self,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Optional[Task]:
    """Update a task's title and/or description.

    Args:
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Updated Task if found, None otherwise

    Raises:
        ValueError: If validation fails
    """
    from src.utils.validators import validate_title, validate_description

    task = self.get_task_by_id(task_id)
    if task is None:
        return None

    # Update title if provided
    if title is not None:
        is_valid, error_msg = validate_title(title)
        if not is_valid:
            raise ValueError(error_msg)
        task.title = title.strip()

    # Update description if provided
    if description is not None:
        is_valid, error_msg = validate_description(description)
        if not is_valid:
            raise ValueError(error_msg)
        task.description = description.strip()

    return task
```

### Testing
- Update title only
- Update description only
- Update both
- Update non-existent task (should return None)
- Update with invalid title (should raise ValueError)

---

## T-009: Implement delete_task Method

**Priority**: CRITICAL
**Dependencies**: T-007
**Estimated Time**: 10 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to delete a task by ID.

### Acceptance Criteria
- ✅ Method `delete_task(self, task_id: int) -> bool` exists
- ✅ Finds task by ID
- ✅ Removes task from list if found
- ✅ Returns True if deleted
- ✅ Returns False if not found

### Expected Code Structure
```python
def delete_task(self, task_id: int) -> bool:
    """Delete a task by ID.

    Args:
        task_id: Task ID to delete

    Returns:
        True if deleted, False if not found
    """
    task = self.get_task_by_id(task_id)
    if task is None:
        return False

    self.tasks.remove(task)
    return True
```

### Testing
- Delete existing task (should return True, task removed)
- Delete non-existent task (should return False)

---

## T-010: Implement toggle_complete Method

**Priority**: CRITICAL
**Dependencies**: T-007
**Estimated Time**: 10 minutes
**File**: `src/services/todo_manager.py`

### Description
Implement method to toggle a task's completion status.

### Acceptance Criteria
- ✅ Method `toggle_complete(self, task_id: int) -> Optional[Task]` exists
- ✅ Finds task by ID
- ✅ Returns None if task not found
- ✅ Toggles completed (False → True or True → False)
- ✅ Returns updated Task

### Expected Code Structure
```python
def toggle_complete(self, task_id: int) -> Optional[Task]:
    """Toggle a task's completion status.

    Args:
        task_id: Task ID to toggle

    Returns:
        Updated Task if found, None otherwise
    """
    task = self.get_task_by_id(task_id)
    if task is None:
        return None

    task.completed = not task.completed
    return task
```

### Testing
- Toggle incomplete → complete
- Toggle complete → incomplete
- Toggle non-existent task (should return None)

---

## T-011: Implement CLI display_menu Function

**Priority**: CRITICAL
**Dependencies**: None
**Estimated Time**: 10 minutes
**File**: `src/main.py`

### Description
Create function to display the main menu.

### Acceptance Criteria
- ✅ Function `display_menu()` exists
- ✅ Displays header with separators
- ✅ Displays 6 menu options (numbered 1-6)
- ✅ Menu includes: Add, View, Update, Delete, Toggle, Exit
- ✅ Uses clear formatting

### Expected Output
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

---

## T-012: Implement CLI display_tasks Function

**Priority**: CRITICAL
**Dependencies**: T-002
**Estimated Time**: 20 minutes
**File**: `src/main.py`

### Description
Create function to display tasks in a formatted table.

### Acceptance Criteria
- ✅ Function `display_tasks(tasks: list[Task])` exists
- ✅ Displays header "YOUR TASKS"
- ✅ Shows table with: ID, Title, Status, Created
- ✅ Completed tasks show ✓, incomplete show ✗
- ✅ Handles empty list with "No tasks yet!" message
- ✅ Shows total count and completion stats

### Expected Output
```
========================================
           YOUR TASKS
========================================

ID  | Title                  | Status | Created
----|------------------------|--------|------------------
1   | Buy groceries          | ✗      | 2025-12-15 10:30
2   | Call dentist           | ✓      | 2025-12-15 11:15

Total: 2 tasks (1 completed, 1 pending)
```

---

## T-013: Implement handle_add_task Function

**Priority**: CRITICAL
**Dependencies**: T-005, T-011
**Estimated Time**: 15 minutes
**File**: `src/main.py`

### Description
Create handler function for adding tasks.

### Acceptance Criteria
- ✅ Function `handle_add_task(manager: TodoManager)` exists
- ✅ Prompts for title
- ✅ Prompts for description (optional)
- ✅ Calls manager.add_task()
- ✅ Displays success message with task ID
- ✅ Catches ValueError and displays error message
- ✅ Handles KeyboardInterrupt gracefully

---

## T-014: Implement handle_view_tasks Function

**Priority**: CRITICAL
**Dependencies**: T-006, T-012
**Estimated Time**: 10 minutes
**File**: `src/main.py`

### Description
Create handler function for viewing all tasks.

### Acceptance Criteria
- ✅ Function `handle_view_tasks(manager: TodoManager)` exists
- ✅ Gets all tasks from manager
- ✅ Calls display_tasks() to show them

---

## T-015: Implement handle_update_task Function

**Priority**: CRITICAL
**Dependencies**: T-008, T-012
**Estimated Time**: 25 minutes
**File**: `src/main.py`

### Description
Create handler function for updating tasks.

### Acceptance Criteria
- ✅ Function `handle_update_task(manager: TodoManager)` exists
- ✅ Displays current tasks
- ✅ Prompts for task ID
- ✅ Validates ID
- ✅ Prompts for new title (Enter to keep current)
- ✅ Prompts for new description (Enter to keep current)
- ✅ Calls manager.update_task()
- ✅ Displays success/error message
- ✅ Handles KeyboardInterrupt

---

## T-016: Implement handle_delete_task Function

**Priority**: CRITICAL
**Dependencies**: T-009, T-012
**Estimated Time**: 20 minutes
**File**: `src/main.py`

### Description
Create handler function for deleting tasks.

### Acceptance Criteria
- ✅ Function `handle_delete_task(manager: TodoManager)` exists
- ✅ Displays current tasks
- ✅ Prompts for task ID
- ✅ Validates ID
- ✅ Shows confirmation prompt (y/n)
- ✅ Deletes if confirmed
- ✅ Displays success/error message
- ✅ Handles KeyboardInterrupt

---

## T-017: Implement handle_toggle_complete Function

**Priority**: CRITICAL
**Dependencies**: T-010, T-012
**Estimated Time**: 15 minutes
**File**: `src/main.py`

### Description
Create handler function for toggling task completion.

### Acceptance Criteria
- ✅ Function `handle_toggle_complete(manager: TodoManager)` exists
- ✅ Displays current tasks
- ✅ Prompts for task ID
- ✅ Validates ID
- ✅ Calls manager.toggle_complete()
- ✅ Displays success message with new status
- ✅ Displays error if task not found
- ✅ Handles KeyboardInterrupt

---

## T-018: Implement main Function and Program Loop

**Priority**: CRITICAL
**Dependencies**: T-011, T-013, T-014, T-015, T-016, T-017
**Estimated Time**: 20 minutes
**File**: `src/main.py`

### Description
Create main function with menu loop and choice routing.

### Acceptance Criteria
- ✅ Function `main()` exists
- ✅ Creates TodoManager instance
- ✅ Runs infinite loop until exit
- ✅ Displays menu each iteration
- ✅ Gets user choice
- ✅ Routes to correct handler function
- ✅ Handles invalid menu choices
- ✅ Exits cleanly on option 6
- ✅ `if __name__ == "__main__":` block calls main()

### Expected Code Structure
```python
def main():
    """Main program loop."""
    manager = TodoManager()

    while True:
        display_menu()
        choice = input().strip()

        if choice == "1":
            handle_add_task(manager)
        elif choice == "2":
            handle_view_tasks(manager)
        elif choice == "3":
            handle_update_task(manager)
        elif choice == "4":
            handle_delete_task(manager)
        elif choice == "5":
            handle_toggle_complete(manager)
        elif choice == "6":
            print("\nGoodbye! Your tasks will not be saved.")
            break
        else:
            print("\n✗ ERROR: Invalid choice. Please enter 1-6.")

        input("\nPress Enter to continue...")

if __name__ == "__main__":
    main()
```

---

## Implementation Order

Execute tasks in this order:

1. **Foundation** (T-001, T-002, T-003, T-004)
2. **Business Logic** (T-005, T-006, T-007, T-008, T-009, T-010)
3. **User Interface** (T-011, T-012, T-013, T-014, T-015, T-016, T-017)
4. **Integration** (T-018)

---

## Testing Checklist

After implementation, verify:

- [ ] Can add task with title only
- [ ] Can add task with title and description
- [ ] Empty title is rejected
- [ ] Title > 200 chars is rejected
- [ ] Can view all tasks (formatted correctly)
- [ ] Empty list shows friendly message
- [ ] Can update task title
- [ ] Can update task description
- [ ] Can update both
- [ ] Invalid task ID shows error
- [ ] Can delete task with confirmation
- [ ] Can cancel deletion
- [ ] Can toggle task to complete
- [ ] Can toggle task to incomplete
- [ ] Can exit application
- [ ] Invalid menu choice shows error

---

**Task Breakdown Version**: 1.0.0
**Status**: Ready for Implementation
**Total Tasks**: 18
**Estimated Total Time**: ~4 hours
