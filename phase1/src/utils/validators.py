# [Task]: T-003
# [From]: specs/phase1-console-app/spec.md §3.2, specs/phase1-console-app/plan.md §2.2

"""Input validation functions for todo application.

This module provides validation for task titles, descriptions, and IDs.
"""


def validate_title(title: str) -> tuple[bool, str]:
    """Validate task title.

    Args:
        title: Task title to validate

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if valid, False otherwise
        - error_message: Empty string if valid, error description otherwise
    """
    if not title or title.strip() == "":
        return (False, "Title is required")
    if len(title) > 200:
        return (False, "Title must be 200 characters or less")
    return (True, "")


def validate_description(description: str) -> tuple[bool, str]:
    """Validate task description.

    Args:
        description: Task description to validate

    Returns:
        Tuple of (is_valid, error_message)
        - is_valid: True if valid, False otherwise
        - error_message: Empty string if valid, error description otherwise
    """
    if len(description) > 1000:
        return (False, "Description must be 1000 characters or less")
    return (True, "")


def validate_task_id(task_id_str: str) -> tuple[bool, int, str]:
    """Validate and parse task ID.

    Args:
        task_id_str: Task ID as string from user input

    Returns:
        Tuple of (is_valid, task_id, error_message)
        - is_valid: True if valid, False otherwise
        - task_id: Parsed integer ID (0 if invalid)
        - error_message: Empty string if valid, error description otherwise
    """
    try:
        task_id = int(task_id_str)
        if task_id <= 0:
            return (False, 0, "Task ID must be a positive number")
        return (True, task_id, "")
    except ValueError:
        return (False, 0, "Please enter a valid number")
