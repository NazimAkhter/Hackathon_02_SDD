"""Entry point for the todo application."""
import sys
import os

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')  # UTF-8 code page
    # Force stdout to use UTF-8
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')

from src.todo_app.service import TodoService
from src.todo_app.cli import (
    display_menu,
    get_user_choice,
    add_todo_flow,
    view_todos_flow,
    view_upcoming_todos,
    view_overdue_todos,
    update_todo_flow,
    delete_todo_flow,
    mark_complete_flow,
    search_todos_flow,
    filter_todos_flow,
    sort_todos_flow
)


def print_welcome():
    """Print welcome message."""
    print("\n========================================")
    print("       Welcome to Todo App")
    print("========================================")


def print_goodbye():
    """Print goodbye message."""
    print("\nThank you for using Todo App!")
    print("All data will be lost (in-memory only).")
    print("Goodbye!")


def main():
    """Main application loop."""
    service = TodoService()
    print_welcome()

    try:
        while True:
            display_menu()
            choice = get_user_choice()

            if choice == 1:
                add_todo_flow(service)
            elif choice == 2:
                view_todos_flow(service)
            elif choice == 3:
                view_upcoming_todos(service)
            elif choice == 4:
                view_overdue_todos(service)
            elif choice == 5:
                update_todo_flow(service)
            elif choice == 6:
                delete_todo_flow(service)
            elif choice == 7:
                mark_complete_flow(service)
            elif choice == 8:
                search_todos_flow(service)
            elif choice == 9:
                filter_todos_flow(service)
            elif choice == 10:
                sort_todos_flow(service)
            elif choice == 11:
                print_goodbye()
                break

    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)


if __name__ == "__main__":
    main()
