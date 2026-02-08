"""CLI interaction functions for the todo application."""
from src.todo_app.service import TodoService
from src.todo_app.models import Priority, Recurrence


def display_menu():
    """Display the main menu."""
    print("\n========== Todo App Menu ==========")
    print("1. Add Todo")
    print("2. View All Todos")
    print("3. View Upcoming Todos")
    print("4. View Overdue Todos")
    print("5. Update Todo")
    print("6. Delete Todo")
    print("7. Mark Todo as Complete")
    print("8. Search Todos")
    print("9. Filter Todos")
    print("10. Sort Todos")
    print("11. Exit")
    print("===================================")


def get_user_choice() -> int:
    """
    Get and validate user menu choice.

    Returns:
        Valid menu choice (1-11)
    """
    while True:
        try:
            choice = input("\nEnter your choice (1-11): ")
            choice_int = int(choice)
            if 1 <= choice_int <= 11:
                return choice_int
            else:
                print("✗ Error: Invalid choice. Please enter a number between 1 and 11.")
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

    # Get priority (optional, default to MEDIUM)
    priority = _get_priority_input(default=Priority.MEDIUM)

    # Get tags (optional)
    tags_input = input("Enter tags (comma-separated, press Enter to skip): ").strip()
    tags = service._normalize_tags(tags_input) if tags_input else []

    # Get due date (optional)
    due_date = None
    while True:
        due_date_input = input("Enter due date (YYYY-MM-DD HH:MM, press Enter to skip): ").strip()
        if not due_date_input:
            break
        try:
            due_date = service._parse_due_date(due_date_input)
            break
        except ValueError as e:
            print(f"✗ Error: {e}")
            continue

    # Get recurrence (optional)
    recurrence = Recurrence.NONE
    while True:
        recurrence_input = input("Enter recurrence (none/daily/weekly/monthly, press Enter for none): ").strip().lower()
        if not recurrence_input or recurrence_input == "none":
            recurrence = Recurrence.NONE
            break
        elif recurrence_input == "daily":
            recurrence = Recurrence.DAILY
            break
        elif recurrence_input == "weekly":
            recurrence = Recurrence.WEEKLY
            break
        elif recurrence_input == "monthly":
            recurrence = Recurrence.MONTHLY
            break
        else:
            print("✗ Error: Invalid recurrence type. Please enter 'none', 'daily', 'weekly', or 'monthly'.")
            continue

    # Validate that recurring todos require a due date
    if recurrence != Recurrence.NONE and due_date is None:
        print("✗ Error: Recurring todos require a due date. Please enter a due date or set recurrence to 'none'.")
        return

    try:
        todo = service.add_todo(title, description, priority=priority, tags=tags, due_date=due_date, recurrence=recurrence)
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
    print(" ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence")
    print("----+--------+----------+--------------------------+----------------------+-----------------------+-------------")

    # Print each todo
    for todo in todos:
        print(str(todo))

    # Print summary
    completed = sum(1 for t in todos if t.is_complete())
    incomplete = len(todos) - completed
    print(f"\nTotal: {len(todos)} todos ({completed} completed, {incomplete} incomplete)\n")


def view_upcoming_todos(service: TodoService):
    """Display todos due within the next 7 days."""
    print("\n--- View Upcoming Todos ---\n")

    todos = service.get_upcoming_todos()

    if not todos:
        print("No upcoming todos due within the next 7 days.\n")
        return

    # Print header
    print(" ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence")
    print("----+--------+----------+--------------------------+----------------------+-----------------------+-------------")

    # Print each todo
    for todo in todos:
        print(str(todo))

    print(f"\nFound {len(todos)} upcoming todo(s) due within the next 7 days.\n")


def view_overdue_todos(service: TodoService):
    """Display overdue todos (past due date, not complete)."""
    print("\n--- View Overdue Todos ---\n")

    todos = service.get_overdue_todos()

    if not todos:
        print("No overdue todos. Great job staying on track!\n")
        return

    # Print header
    print(" ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence")
    print("----+--------+----------+--------------------------+----------------------+-----------------------+-------------")

    # Print each todo
    for todo in todos:
        print(str(todo))

    print(f"\nFound {len(todos)} overdue todo(s).\n")


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
    print(f"  Priority: {todo.priority.name}")
    print(f"  Tags: {', '.join(todo.tags) if todo.tags else '(none)'}")
    due_date_display = todo.due_date.strftime("%Y-%m-%d %H:%M") if todo.due_date else "(none)"
    print(f"  Due Date: {due_date_display}")
    print(f"  Recurrence: {todo.recurrence.value}")

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

    # Get new priority
    print(f"\nCurrent priority: {todo.priority.name.lower()}")
    priority_input = input("Enter new priority (high/medium/low, press Enter to keep current): ").strip().lower()
    new_priority = None
    if priority_input:
        if priority_input == "high":
            new_priority = Priority.HIGH
        elif priority_input == "medium":
            new_priority = Priority.MEDIUM
        elif priority_input == "low":
            new_priority = Priority.LOW
        else:
            print("✗ Error: Invalid priority. Update cancelled.")
            return

    # Get new tags
    print(f"\nCurrent tags: {', '.join(todo.tags) if todo.tags else '(none)'}")
    tags_input = input("Enter new tags (comma-separated, press Enter to keep current): ").strip()
    new_tags = None
    if tags_input:
        new_tags = service._normalize_tags(tags_input)

    # Get new due date
    print(f"\nCurrent due date: {due_date_display}")
    new_due_date = None
    while True:
        due_date_input = input("Enter new due date (YYYY-MM-DD HH:MM, press Enter to keep current): ").strip()
        if not due_date_input:
            break
        try:
            new_due_date = service._parse_due_date(due_date_input)
            break
        except ValueError as e:
            print(f"✗ Error: {e}")
            continue

    # Get new recurrence
    print(f"\nCurrent recurrence: {todo.recurrence.value}")
    new_recurrence = None
    while True:
        recurrence_input = input("Enter new recurrence (none/daily/weekly/monthly, press Enter to keep current): ").strip().lower()
        if not recurrence_input:
            break
        elif recurrence_input == "none":
            new_recurrence = Recurrence.NONE
            break
        elif recurrence_input == "daily":
            new_recurrence = Recurrence.DAILY
            break
        elif recurrence_input == "weekly":
            new_recurrence = Recurrence.WEEKLY
            break
        elif recurrence_input == "monthly":
            new_recurrence = Recurrence.MONTHLY
            break
        else:
            print("✗ Error: Invalid recurrence type. Please enter 'none', 'daily', 'weekly', or 'monthly'.")
            continue

    try:
        if service.update_todo(todo_id, title=new_title, description=new_desc, priority=new_priority, tags=new_tags, due_date=new_due_date, recurrence=new_recurrence):
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
    new_todo = service.mark_complete(todo_id)
    if new_todo or service.get_todo_by_id(todo_id).is_complete():
        print("\nTodo marked as complete!")
        print(f"  Title: {todo.title}")
        print(f"  Description: {todo.description}")

        # If recurring, show the new instance
        if new_todo:
            due_display = new_todo.due_date.strftime("%Y-%m-%d %H:%M") if new_todo.due_date else "(no due date)"
            print(f"\n✓ Next occurrence created automatically!")
            print(f"  ID: {new_todo.id}")
            print(f"  Due: {due_display}\n")
        else:
            print()
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


def search_todos_flow(service: TodoService):
    """Handle the search todos flow."""
    print("\n--- Search Todos ---")

    # Get keyword
    keyword = input("Enter search keyword: ").strip()

    if not keyword:
        print("\n✗ Error: Search keyword cannot be empty.\n")
        return

    # Search
    results = service.search_todos(keyword)

    if not results:
        print(f"\nNo matching todos found for '{keyword}'.\n")
        return

    # Display results
    print(f"\n--- Search Results for '{keyword}' ---\n")
    print(" ID | Status | Priority | Title                    | Tags                 | Description")
    print("----+--------+----------+--------------------------+----------------------+---------------------------")

    for todo in results:
        print(str(todo))

    print(f"\nFound {len(results)} matching todo(s).\n")


def sort_todos_flow(service: TodoService):
    """Handle the sort todos flow."""
    print("\n--- Sort Todos ---")
    print("1. Sort by Priority (high → medium → low)")
    print("2. Sort by Date (newest first)")
    print("3. Sort by Date (oldest first)")
    print("4. Sort by Title (A-Z)")
    print("5. Sort by Due Date (earliest first)")
    print("6. Sort by Due Date (latest first)")

    while True:
        try:
            choice = int(input("\nEnter sort type (1-6): "))
            if 1 <= choice <= 6:
                break
            else:
                print("✗ Error: Please enter a number between 1 and 6.")
        except ValueError:
            print("✗ Error: Please enter a valid number.")

    sort_by_map = {
        1: "priority",
        2: "date_newest",
        3: "date_oldest",
        4: "title",
        5: "due_date",
        6: "due_date_desc"
    }

    results = service.sort_todos(sort_by=sort_by_map[choice])

    if not results:
        print("\nNo todos found.\n")
        return

    # Display results
    print("\n--- Sorted Todos ---\n")
    print(" ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence")
    print("----+--------+----------+--------------------------+----------------------+-----------------------+-------------")

    for todo in results:
        print(str(todo))

    print(f"\nTotal: {len(results)} todo(s).\n")


def filter_todos_flow(service: TodoService):
    """Handle the filter todos flow with optional sorting."""
    print("\n--- Filter Todos ---")
    print("1. Filter by Status")
    print("2. Filter by Priority")
    print("3. Filter by Tag")

    while True:
        try:
            choice = int(input("\nEnter filter type (1-3): "))
            if 1 <= choice <= 3:
                break
            else:
                print("✗ Error: Please enter a number between 1 and 3.")
        except ValueError:
            print("✗ Error: Please enter a valid number.")

    results = []

    if choice == 1:
        # Filter by status
        status_input = input("Enter status (complete/incomplete): ").strip().lower()
        if status_input == "complete":
            results = service.filter_by_status(completed=True)
        elif status_input == "incomplete":
            results = service.filter_by_status(completed=False)
        else:
            print("✗ Error: Invalid status. Please enter 'complete' or 'incomplete'.\n")
            return

    elif choice == 2:
        # Filter by priority
        priority_input = input("Enter priority (high/medium/low): ").strip().lower()
        if priority_input == "high":
            results = service.filter_by_priority(Priority.HIGH)
        elif priority_input == "medium":
            results = service.filter_by_priority(Priority.MEDIUM)
        elif priority_input == "low":
            results = service.filter_by_priority(Priority.LOW)
        else:
            print("✗ Error: Invalid priority. Please enter 'high', 'medium', or 'low'.\n")
            return

    elif choice == 3:
        # Filter by tag
        tag_input = input("Enter tag: ").strip()
        if not tag_input:
            print("✗ Error: Tag cannot be empty.\n")
            return
        results = service.filter_by_tag(tag_input)

    # Check if any results
    if not results:
        print("\nNo todos match the selected filter.\n")
        return

    # Ask if user wants to sort the filtered results
    sort_input = input("\nSort filtered results? (y/n): ").strip().lower()
    if sort_input == 'y':
        print("\nSort Options:")
        print("1. Sort by Priority (high → medium → low)")
        print("2. Sort by Date (newest first)")
        print("3. Sort by Date (oldest first)")
        print("4. Sort by Title (A-Z)")
        print("5. Sort by Due Date (earliest first)")
        print("6. Sort by Due Date (latest first)")

        while True:
            try:
                sort_choice = int(input("\nEnter sort type (1-6): "))
                if 1 <= sort_choice <= 6:
                    break
                else:
                    print("✗ Error: Please enter a number between 1 and 6.")
            except ValueError:
                print("✗ Error: Please enter a valid number.")

        sort_by_map = {
            1: "priority",
            2: "date_newest",
            3: "date_oldest",
            4: "title",
            5: "due_date",
            6: "due_date_desc"
        }

        results = service.sort_todos(results, sort_by=sort_by_map[sort_choice])

    # Display results
    print("\n--- Filtered Results ---\n")
    print(" ID | Status | Priority | Title                    | Tags                 | Due Date              | Recurrence")
    print("----+--------+----------+--------------------------+----------------------+-----------------------+-------------")

    for todo in results:
        print(str(todo))

    print(f"\nFound {len(results)} matching todo(s).\n")


def _get_priority_input(default: Priority = Priority.MEDIUM) -> Priority:
    """
    Helper to get and validate priority input.

    Args:
        default: Default priority if user presses Enter

    Returns:
        Valid Priority enum member
    """
    while True:
        priority_input = input(f"Enter priority (high/medium/low, press Enter for {default.name.lower()}): ").strip().lower()

        if not priority_input:
            return default

        if priority_input == "high":
            return Priority.HIGH
        elif priority_input == "medium":
            return Priority.MEDIUM
        elif priority_input == "low":
            return Priority.LOW
        else:
            print("✗ Error: Invalid priority. Please enter 'high', 'medium', or 'low'.")
