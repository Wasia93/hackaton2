# [Task]: T-002
# [From]: specs/phase1-console-app/spec.md §3.1, specs/phase1-console-app/plan.md §2.2

"""Task model for todo application.

This module defines the Task dataclass representing a single todo item.
"""

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Task:
    """Represents a todo task.

    Attributes:
        id: Unique task identifier (auto-incremented)
        title: Task title (required, max 200 characters)
        description: Task description (optional, max 1000 characters)
        completed: Completion status (default False)
        created_at: Creation timestamp (auto-set to current time)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
