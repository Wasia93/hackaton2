# Phase I: Todo Console App - Specification

**Feature**: In-Memory Python Console Todo Application
**Phase**: Phase I - Console App
**Status**: Draft
**Created**: 2025-12-15
**Updated**: 2025-12-15

---

## 1. Overview

Build a command-line todo application that stores tasks in memory using Python 3.13+. This is the foundation for the Evolution of Todo project, implementing Basic Level functionality only.

### Purpose
- Provide a simple, functional todo list manager via command-line interface
- Establish the core data model and CRUD operations
- Foundation for future phases (web app, AI chatbot, cloud deployment)

### Constraints
- **No manual coding** - All code generated via Claude Code using this spec
- **In-memory storage only** - No database, no file persistence
- **Basic Level features only** - No priorities, tags, search, or advanced features
- **Python 3.13+** with UV package manager
- **Clean code principles** - Simple, readable, maintainable

---

## 2. User Journeys

### UJ-1: Create a New Task
**As a user**
**I want to** add a new task with a title and optional description
**So that** I can keep track of things I need to do

**Flow**:
1. User selects "Add Task" option
2. System prompts for task title
3. User enters title (required, 1-200 characters)
4. System prompts for description (optional)
5. User enters description (max 1000 characters) or skips
6. System creates task with unique ID, sets completed=False, captures timestamp
7. System displays success message with task ID

**Success Criteria**:
- Task is created with unique ID
- Title is stored correctly
- Description is stored (or empty if skipped)
- Task appears in task list
- Completion status defaults to False

---

### UJ-2: View All Tasks
**As a user**
**I want to** see a list of all my tasks
**So that** I can review what needs to be done

**Flow**:
1. User selects "View Tasks" option
2. System displays all tasks in a formatted table
3. Each task shows: ID, Title, Status (✓ or ✗), Created timestamp

**Success Criteria**:
- All tasks are displayed
- Tasks are shown with clear formatting
- Completed tasks are visually distinct (✓ vs ✗)
- If no tasks exist, friendly message shown ("No tasks yet!")

---

### UJ-3: Update a Task
**As a user**
**I want to** modify a task's title or description
**So that** I can correct or clarify task details

**Flow**:
1. User selects "Update Task" option
2. System displays list of tasks
3. User enters task ID to update
4. System validates ID exists
5. System prompts: "New title (press Enter to keep current)"
6. User enters new title or presses Enter
7. System prompts: "New description (press Enter to keep current)"
8. User enters new description or presses Enter
9. System updates task and confirms

**Success Criteria**:
- Task is updated with new values
- Unchanged fields retain original values
- Invalid task ID shows error message
- Success message displayed after update

---

### UJ-4: Delete a Task
**As a user**
**I want to** remove a task from the list
**So that** I can declutter completed or irrelevant tasks

**Flow**:
1. User selects "Delete Task" option
2. System displays list of tasks
3. User enters task ID to delete
4. System validates ID exists
5. System confirms: "Delete task '[Title]'? (y/n)"
6. User confirms (y) or cancels (n)
7. If confirmed, system removes task and confirms
8. If cancelled, returns to menu

**Success Criteria**:
- Task is permanently removed from list
- Invalid task ID shows error message
- Confirmation required before deletion
- Success message displayed after deletion

---

### UJ-5: Mark Task as Complete/Incomplete
**As a user**
**I want to** toggle a task's completion status
**So that** I can track which tasks are done

**Flow**:
1. User selects "Mark Complete/Incomplete" option
2. System displays list of tasks with current status
3. User enters task ID to toggle
4. System validates ID exists
5. System toggles completed status (False → True or True → False)
6. System displays updated status

**Success Criteria**:
- Task completion status is toggled
- Visual indicator updates (✗ → ✓ or ✓ → ✗)
- Invalid task ID shows error message
- Success message shows new status

---

## 3. Functional Requirements

### FR-1: Task Data Model
**Priority**: CRITICAL
**Dependencies**: None

**Requirements**:
- Each task MUST have:
  - `id` (integer, unique, auto-increment)
  - `title` (string, required, 1-200 characters)
  - `description` (string, optional, max 1000 characters)
  - `completed` (boolean, default False)
  - `created_at` (datetime, auto-set on creation)

**Validation Rules**:
- Title cannot be empty
- Title max 200 characters
- Description max 1000 characters (if provided)

---

### FR-2: CRUD Operations
**Priority**: CRITICAL
**Dependencies**: FR-1

**Requirements**:
- **Create**: Add new task with validation
- **Read**: List all tasks, get task by ID
- **Update**: Modify title and/or description
- **Delete**: Remove task by ID
- **Toggle**: Change completion status

**Error Handling**:
- Invalid task ID → "Task not found"
- Empty title → "Title is required"
- Title too long → "Title must be 200 characters or less"
- Description too long → "Description must be 1000 characters or less"

---

### FR-3: In-Memory Storage
**Priority**: CRITICAL
**Dependencies**: FR-1

**Requirements**:
- Use Python list or dictionary to store tasks
- Data persists only during program execution
- No file I/O or database connections
- Auto-increment task IDs starting from 1

**Implementation Notes**:
- Use a global list or class-based storage
- Task IDs should be sequential (1, 2, 3, ...)
- After deletion, IDs are not reused

---

### FR-4: Command-Line Interface
**Priority**: CRITICAL
**Dependencies**: FR-2

**Requirements**:
- Interactive menu-driven interface
- Clear menu options (numbered 1-6)
- Input prompts with clear instructions
- Success/error messages for all operations
- Option to exit the application

**Menu Options**:
1. Add Task
2. View All Tasks
3. Update Task
4. Delete Task
5. Mark Complete/Incomplete
6. Exit

**UI Principles**:
- Clear, concise prompts
- Visual feedback for all actions
- Error messages in red or with "ERROR:" prefix
- Success messages with confirmation
- Table format for task lists

---

## 4. Non-Functional Requirements

### NFR-1: Performance
- Application starts in < 1 second
- All operations complete instantly (< 100ms)
- No lag or delays in user interaction

### NFR-2: Usability
- Menu is intuitive and self-explanatory
- Error messages guide users to correct actions
- No need for documentation to use basic features

### NFR-3: Code Quality
- Follow PEP 8 Python style guide
- Use type hints where applicable
- Functions are single-purpose and testable
- Maximum function length: 50 lines
- Clear variable and function names

### NFR-4: Maintainability
- Modular code structure (separate concerns)
- Comments for complex logic
- Each CRUD operation in separate function
- Easy to extend for future phases

---

## 5. Acceptance Criteria

### AC-1: Add Task
- ✅ User can create task with title only
- ✅ User can create task with title and description
- ✅ Empty title is rejected with error message
- ✅ Title > 200 chars is rejected
- ✅ Task is assigned unique ID
- ✅ Task appears in task list immediately

### AC-2: View Tasks
- ✅ All tasks are displayed in table format
- ✅ Table shows: ID, Title, Status, Created timestamp
- ✅ Completed tasks show ✓, incomplete show ✗
- ✅ Empty list shows "No tasks yet!" message

### AC-3: Update Task
- ✅ User can update title only
- ✅ User can update description only
- ✅ User can update both title and description
- ✅ User can keep current values by pressing Enter
- ✅ Invalid task ID shows error
- ✅ Success message confirms update

### AC-4: Delete Task
- ✅ User can delete task by ID
- ✅ Confirmation required before deletion
- ✅ Task is removed from list
- ✅ Invalid task ID shows error
- ✅ Cancel option returns to menu without deleting

### AC-5: Mark Complete/Incomplete
- ✅ User can toggle task completion by ID
- ✅ Status changes from incomplete to complete
- ✅ Status changes from complete to incomplete
- ✅ Visual indicator updates immediately
- ✅ Invalid task ID shows error

### AC-6: Exit
- ✅ User can exit application cleanly
- ✅ Exit option returns control to terminal

---

## 6. Out of Scope (Not in Phase I)

The following features are explicitly **excluded** from Phase I:

- ❌ File persistence or database storage
- ❌ User authentication or multi-user support
- ❌ Task priorities (high/medium/low)
- ❌ Tags or categories
- ❌ Search or filter functionality
- ❌ Sort tasks by different criteria
- ❌ Due dates or reminders
- ❌ Recurring tasks
- ❌ Web interface or API
- ❌ Data import/export

These features will be added in later phases.

---

## 7. Dependencies

### External Dependencies
- Python 3.13+
- UV package manager

### Internal Dependencies
- None (standalone console application)

### Development Dependencies
- pytest (for future testing)
- Black (for code formatting)
- mypy (for type checking)

---

## 8. Risks and Assumptions

### Risks
- **R-1**: User enters invalid input (mitigated by input validation)
- **R-2**: Large number of tasks may clutter display (acceptable for Phase I)

### Assumptions
- **A-1**: Users understand command-line interfaces
- **A-2**: Tasks don't need to persist after program exit (in-memory is sufficient)
- **A-3**: Single-user usage (no concurrent access)
- **A-4**: English language only

---

## 9. Success Metrics

Phase I is successful when:
- ✅ All 5 Basic Level features work correctly
- ✅ All acceptance criteria pass
- ✅ Code follows constitution principles
- ✅ Application runs without crashes
- ✅ Code is generated by Claude Code (no manual coding)

---

## 10. References

- [Constitution](./.specify/memory/constitution.md) - Project principles
- [AGENTS.md](./AGENTS.md) - Agent workflow instructions
- [Documentation](./.claude/commands/documentation.md) - Hackathon requirements

---

**Spec Version**: 1.0.0
**Approved By**: [Pending approval]
**Approval Date**: [Pending]
