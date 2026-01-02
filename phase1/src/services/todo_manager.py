# [Task]: T-004, T-005, T-006, T-007, T-008, T-009, T-010
# [From]: specs/phase1-console-app/spec.md §3, specs/phase1-console-app/plan.md §2.2

"""Todo Manager service for CRUD operations.

This module provides the business logic for managing todo tasks.
"""

from datetime import datetime
from typing import Optional

from src.models.task import Task
from src.utils.validators import validate_title, validate_description


class TodoManager:
    """Manages todo tasks with in-memory storage.

    Provides CRUD operations: Create, Read, Update, Delete tasks.
    Also supports toggling task completion status.
    """

    def __init__(self):
        """Initialize the todo manager with empty task list."""
        self.tasks: list[Task] = []
        self.next_id: int = 1

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

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks.

        Returns:
            List of all Task objects
        """
        return self.tasks

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
