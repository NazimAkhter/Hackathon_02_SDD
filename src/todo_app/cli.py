"""CLI interaction functions for the todo application."""
from src.todo_app.service import TodoService


def display_menu():
    """Display the main menu."""
    print("\n========== Todo App Menu ==========")
    print("1. Add Todo")
    print("2. View All Todos")
    print("3. Update Todo")
    print("4. Delete Todo")
    print("5. Mark Todo as Complete")
    print("6. Exit")
    print("===================================")


def get_user_choice() -> int:
    """
    Get and validate user menu choice.

    Returns:
        Valid menu choice (1-6)
    """
    while True:
        try:
            choice = input("\nEnter your choice (1-6): ")
            choice_int = int(choice)
            if 1 <= choice_int <= 6:
                return choice_int
            else:
                print("✗ Error: Invalid choice. Please enter a number between 1 and 6.")
        except ValueError:
            print("✗ Error: Please enter a valid number.")


def add_todo_flow(service: TodoService):
    """Handle the add todo flow."""
    print("\n--- Add New Todo ---")

    # Get title with validation
    while True:
        title = input("Enter title: ")
        if not title.strip():
            print("✗ Error: Title cannot be empty. Please try again.")
            continue

        if len(title) > 200:
            print("✗ Error: Title cannot exceed 200 characters. Please try again.")
            continue

        break

    # Get description (optional)
    while True:
        description = input("Enter description (optional, press Enter to skip): ")
        if len(description) > 1000:
            print("✗ Error: Description cannot exceed 1000 characters. Please try again.")
            continue
        break

    try:
        todo = service.add_todo(title, description)
        print(f"\n✓ Todo added successfully! (ID: {todo.id})")
    except ValueError as e:
        print(f"\n✗ Error: {e}")


def view_todos_flow(service: TodoService):
    """Display all todos in table format."""
    print("\n--- All Todos ---\n")

    todos = service.get_all_todos()

    if not todos:
        print("No todos found. Add your first todo to get started!\n")
        return

    # Print header
    print(" ID | Status | Title                          | Description")
    print("----+--------+--------------------------------+---------------------------")

    # Print each todo
    for todo in todos:
        print(str(todo))

    # Print summary
    completed = sum(1 for t in todos if t.is_complete())
    incomplete = len(todos) - completed
    print(f"\nTotal: {len(todos)} todos ({completed} completed, {incomplete} incomplete)\n")


def update_todo_flow(service: TodoService):
    """Handle the update todo flow."""
    print("\n--- Update Todo ---")

    # Get todo ID
    todo_id = _get_todo_id_input()
    if todo_id is None:
        return

    # Check if todo exists
    todo = service.get_todo_by_id(todo_id)
    if not todo:
        print(f"\n✗ Error: Todo with ID {todo_id} not found.\n")
        return

    # Display current todo
    print("\nCurrent Todo:")
    print(f"  ID: {todo.id}")
    print(f"  Title: {todo.title}")
    print(f"  Description: {todo.description}")
    print(f"  Status: {'Complete' if todo.is_complete() else 'Incomplete'}")

    # Get new title
    new_title_input = input("\nEnter new title (press Enter to keep current): ")
    new_title = new_title_input if new_title_input.strip() else None

    if new_title is not None and len(new_title) > 200:
        print("✗ Error: Title cannot exceed 200 characters.")
        return

    # Get new description
    new_desc_input = input("Enter new description (press Enter to keep current): ")
    new_desc = new_desc_input if new_desc_input != '' else None

    if new_desc is not None and len(new_desc) > 1000:
        print("✗ Error: Description cannot exceed 1000 characters.")
        return

    try:
        if service.update_todo(todo_id, title=new_title, description=new_desc):
            print("\n✓ Todo updated successfully!\n")
        else:
            print(f"\n✗ Error: Todo with ID {todo_id} not found.\n")
    except ValueError as e:
        print(f"\n✗ Error: {e}\n")


def delete_todo_flow(service: TodoService):
    """Handle the delete todo flow with confirmation."""
    print("\n--- Delete Todo ---")

    # Get todo ID
    todo_id = _get_todo_id_input()
    if todo_id is None:
        return

    # Check if todo exists
    todo = service.get_todo_by_id(todo_id)
    if not todo:
        print(f"\n✗ Error: Todo with ID {todo_id} not found.\n")
        return

    # Show todo and ask for confirmation
    print("\nAre you sure you want to delete this todo?")
    print(f"  Title: {todo.title}")
    print(f"  Description: {todo.description}")

    while True:
        confirm = input("\nConfirm deletion (y/n): ").strip().lower()
        if confirm == 'y':
            service.delete_todo(todo_id)
            print("\n✓ Todo deleted successfully!\n")
            return
        elif confirm == 'n':
            print("\nDeletion cancelled.\n")
            return
        else:
            print("✗ Error: Please enter 'y' for yes or 'n' for no.")


def mark_complete_flow(service: TodoService):
    """Handle the mark complete flow."""
    print("\n--- Mark Todo as Complete ---")

    # Get todo ID
    todo_id = _get_todo_id_input()
    if todo_id is None:
        return

    # Check if todo exists
    todo = service.get_todo_by_id(todo_id)
    if not todo:
        print(f"\n✗ Error: Todo with ID {todo_id} not found.\n")
        return

    # Check if already complete
    if todo.is_complete():
        print(f"\nℹ Info: This todo is already marked as complete.")
        print(f"  Title: {todo.title}\n")
        return

    # Mark complete
    if service.mark_complete(todo_id):
        print("\nTodo marked as complete!")
        print(f"  Title: {todo.title}")
        print(f"  Description: {todo.description}\n")
    else:
        print(f"\n✗ Error: Todo with ID {todo_id} not found.\n")


def _get_todo_id_input() -> int | None:
    """
    Helper to get and validate todo ID input.

    Returns:
        Valid todo ID or None if invalid
    """
    try:
        todo_id = int(input("Enter todo ID: "))
        return todo_id
    except ValueError:
        print("\n✗ Error: Please enter a valid number.\n")
        return None
