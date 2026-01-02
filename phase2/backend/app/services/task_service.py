"""
Task service layer for business logic
Task: T-012 - Create Task Service Layer
"""

from sqlmodel import Session, select
from app.models.task import Task
from typing import Optional


class TaskService:
    """
    Service layer for task-related business logic.
    Ensures data isolation by filtering all queries by user_id.
    """

    def __init__(self, session: Session, user_id: str):
        """
        Initialize task service.

        Args:
            session: Database session
            user_id: Current user's ID (from JWT token)
        """
        self.session = session
        self.user_id = user_id

    def create_task(self, title: str, description: str = "") -> Task:
        """
        Create a new task for the current user.

        Args:
            title: Task title (required, max 200 chars)
            description: Task description (optional)

        Returns:
            Task: Created task object

        Raises:
            ValueError: If validation fails
        """
        # Validate title
        if not title or title.strip() == "":
            raise ValueError("Title is required")

        if len(title) > 200:
            raise ValueError("Title must be 200 characters or less")

        # Create task
        task = Task(
            user_id=self.user_id,
            title=title.strip(),
            description=description.strip()
        )

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Get all tasks for the current user.

        Returns:
            list[Task]: List of tasks owned by current user
        """
        statement = select(Task).where(Task.user_id == self.user_id)
        return list(self.session.exec(statement).all())

    def get_task_by_id(self, task_id: int) -> Optional[Task]:
        """
        Get a specific task by ID (only if owned by current user).

        Args:
            task_id: Task ID to retrieve

        Returns:
            Optional[Task]: Task if found and owned by user, None otherwise
        """
        statement = select(Task).where(
            Task.id == task_id,
            Task.user_id == self.user_id
        )
        return self.session.exec(statement).first()

    def update_task(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> Optional[Task]:
        """
        Update a task's title and/or description.

        Args:
            task_id: Task ID to update
            title: New title (optional)
            description: New description (optional)

        Returns:
            Optional[Task]: Updated task if found, None if not found

        Raises:
            ValueError: If validation fails
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        # Update title if provided
        if title is not None:
            if len(title) > 200:
                raise ValueError("Title must be 200 characters or less")
            task.title = title.strip()

        # Update description if provided
        if description is not None:
            task.description = description.strip()

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task

    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task by ID.

        Args:
            task_id: Task ID to delete

        Returns:
            bool: True if deleted, False if not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return False

        self.session.delete(task)
        self.session.commit()

        return True

    def toggle_completion(self, task_id: int) -> Optional[Task]:
        """
        Toggle a task's completion status.

        Args:
            task_id: Task ID to toggle

        Returns:
            Optional[Task]: Updated task if found, None if not found
        """
        task = self.get_task_by_id(task_id)
        if not task:
            return None

        task.completed = not task.completed

        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

        return task
