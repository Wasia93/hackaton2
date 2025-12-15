# [Task]: T-011, T-012, T-013, T-014, T-015, T-016, T-017, T-018
# [From]: specs/phase1-console-app/spec.md §2-4, specs/phase1-console-app/plan.md §2.2

"""Todo Console Application - Main Entry Point.

This module provides the command-line interface for the todo application.
"""

from src.models.task import Task
from src.services.todo_manager import TodoManager
from src.utils.validators import validate_task_id


def display_menu():
    """Display the main menu."""
    print("\n" + "=" * 40)
    print("        TODO LIST MANAGER")
    print("=" * 40)
    print("\n1. Add Task")
    print("2. View All Tasks")
    print("3. Update Task")
    print("4. Delete Task")
    print("5. Mark Complete/Incomplete")
    print("6. Exit")
    print()


def display_tasks(tasks: list[Task]):
    """Display tasks in a formatted table.

    Args:
        tasks: List of Task objects to display
    """
    print("\n" + "=" * 80)
    print("           YOUR TASKS".center(80))
    print("=" * 80)

    if not tasks:
        print("\nNo tasks yet! Add your first task to get started.\n")
        return

    # Header
    print(f"\n{'ID':<4} | {'Title':<40} | {'Status':<6} | {'Created':<18}")
    print("-" * 4 + "-+-" + "-" * 40 + "-+-" + "-" * 6 + "-+-" + "-" * 18)

    # Task rows
    for task in tasks:
        status_icon = "✓" if task.completed else "✗"
        title_display = task.title[:40] if len(task.title) <= 40 else task.title[:37] + "..."
        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")

        print(f"{task.id:<4} | {title_display:<40} | {status_icon:<6} | {created_str:<18}")

    # Summary
    completed_count = sum(1 for task in tasks if task.completed)
    pending_count = len(tasks) - completed_count
    print(f"\nTotal: {len(tasks)} tasks ({completed_count} completed, {pending_count} pending)\n")


def handle_add_task(manager: TodoManager):
    """Handle adding a new task.

    Args:
        manager: TodoManager instance
    """
    try:
        print("\n--- Add New Task ---")
        title = input("Enter task title: ").strip()
        description = input("Enter description (optional, press Enter to skip): ").strip()

        task = manager.add_task(title, description)
        print(f"\n✓ Task added successfully! (ID: {task.id})")

    except ValueError as e:
        print(f"\n✗ ERROR: {e}")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled")


def handle_view_tasks(manager: TodoManager):
    """Handle viewing all tasks.

    Args:
        manager: TodoManager instance
    """
    tasks = manager.get_all_tasks()
    display_tasks(tasks)


def handle_update_task(manager: TodoManager):
    """Handle updating a task.

    Args:
        manager: TodoManager instance
    """
    try:
        # Show current tasks
        tasks = manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks to update!")
            return

        display_tasks(tasks)

        # Get task ID
        print("\n--- Update Task ---")
        task_id_str = input("Enter task ID to update: ").strip()

        is_valid, task_id, error_msg = validate_task_id(task_id_str)
        if not is_valid:
            print(f"\n✗ ERROR: {error_msg}")
            return

        # Check if task exists
        task = manager.get_task_by_id(task_id)
        if task is None:
            print(f"\n✗ ERROR: Task not found with ID {task_id}")
            return

        # Get new values
        print(f"\nCurrent title: {task.title}")
        new_title = input("New title (press Enter to keep current): ").strip()

        print(f"Current description: {task.description if task.description else '(none)'}")
        new_description = input("New description (press Enter to keep current): ").strip()

        # Update task
        updated_task = manager.update_task(
            task_id,
            title=new_title if new_title else None,
            description=new_description if new_description else None
        )

        if updated_task:
            print("\n✓ Task updated successfully!")
        else:
            print(f"\n✗ ERROR: Task not found with ID {task_id}")

    except ValueError as e:
        print(f"\n✗ ERROR: {e}")
    except KeyboardInterrupt:
        print("\n\nOperation cancelled")


def handle_delete_task(manager: TodoManager):
    """Handle deleting a task.

    Args:
        manager: TodoManager instance
    """
    try:
        # Show current tasks
        tasks = manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks to delete!")
            return

        display_tasks(tasks)

        # Get task ID
        print("\n--- Delete Task ---")
        task_id_str = input("Enter task ID to delete: ").strip()

        is_valid, task_id, error_msg = validate_task_id(task_id_str)
        if not is_valid:
            print(f"\n✗ ERROR: {error_msg}")
            return

        # Check if task exists
        task = manager.get_task_by_id(task_id)
        if task is None:
            print(f"\n✗ ERROR: Task not found with ID {task_id}")
            return

        # Confirm deletion
        confirm = input(f"Delete task '{task.title}'? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\nDeletion cancelled")
            return

        # Delete task
        if manager.delete_task(task_id):
            print("\n✓ Task deleted successfully!")
        else:
            print(f"\n✗ ERROR: Task not found with ID {task_id}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled")


def handle_toggle_complete(manager: TodoManager):
    """Handle toggling task completion status.

    Args:
        manager: TodoManager instance
    """
    try:
        # Show current tasks
        tasks = manager.get_all_tasks()
        if not tasks:
            print("\nNo tasks to toggle!")
            return

        display_tasks(tasks)

        # Get task ID
        print("\n--- Mark Complete/Incomplete ---")
        task_id_str = input("Enter task ID to toggle: ").strip()

        is_valid, task_id, error_msg = validate_task_id(task_id_str)
        if not is_valid:
            print(f"\n✗ ERROR: {error_msg}")
            return

        # Toggle completion
        updated_task = manager.toggle_complete(task_id)

        if updated_task:
            status = "complete" if updated_task.completed else "incomplete"
            print(f"\n✓ Task marked as {status}!")
        else:
            print(f"\n✗ ERROR: Task not found with ID {task_id}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled")


def main():
    """Main program loop."""
    manager = TodoManager()

    print("\nWelcome to Todo List Manager!")
    print("Note: Tasks are stored in memory and will not persist after exit.\n")

    while True:
        try:
            display_menu()
            choice = input("Enter your choice (1-6): ").strip()

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
                print("\n" + "=" * 40)
                print("Thank you for using Todo List Manager!")
                print("Your tasks will not be saved.")
                print("=" * 40 + "\n")
                break
            else:
                print("\n✗ ERROR: Invalid choice. Please enter 1-6.")

            input("\nPress Enter to continue...")

        except KeyboardInterrupt:
            print("\n\n" + "=" * 40)
            print("Application interrupted by user.")
            print("=" * 40 + "\n")
            break


if __name__ == "__main__":
    main()
