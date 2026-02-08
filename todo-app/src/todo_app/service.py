"""Business logic and CRUD operations for todos."""
from datetime import datetime, timedelta
import calendar
from typing import Dict, List, Optional
from src.todo_app.models import Todo, Priority, Recurrence


class TodoService:
    """Service layer for todo CRUD operations."""

    def __init__(self):
        """Initialize service with empty todos dictionary."""
        self.todos: Dict[int, Todo] = {}
        self._next_id = 1  # Track next ID to prevent reuse after deletion

    def _generate_id(self) -> int:
        """Generate next sequential ID for a new todo."""
        current_id = self._next_id
        self._next_id += 1
        return current_id

    def _normalize_tags(self, tags_input: str) -> list[str]:
        """
        Normalize tags from comma-separated string input.

        Args:
            tags_input: Comma-separated tag string (e.g., "work, HOME, errands")

        Returns:
            List of normalized tags (lowercase, trimmed, deduped)
        """
        if not tags_input or not tags_input.strip():
            return []

        # Split on comma, normalize each tag
        raw_tags = tags_input.split(",")
        seen = set()
        normalized = []
        for tag in raw_tags:
            clean = tag.strip().lower()
            if clean and clean not in seen:
                seen.add(clean)
                normalized.append(clean)
        return normalized

    def _parse_due_date(self, date_input: str) -> Optional[datetime]:
        """
        Parse due date input in YYYY-MM-DD HH:MM format.

        Args:
            date_input: Date string in format "YYYY-MM-DD HH:MM"

        Returns:
            datetime object if valid, None if empty input

        Raises:
            ValueError: If date format is invalid
        """
        if not date_input or not date_input.strip():
            return None

        try:
            return datetime.strptime(date_input.strip(), "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Invalid date format. Please use YYYY-MM-DD HH:MM (e.g., 2026-02-15 14:00)")

    def _calculate_next_due_date(self, current_due: datetime, recurrence: Recurrence) -> datetime:
        """
        Calculate next due date based on recurrence type.

        Args:
            current_due: Current due date
            recurrence: Recurrence pattern

        Returns:
            Next due date

        Raises:
            ValueError: If recurrence is NONE or current_due is None
        """
        if recurrence == Recurrence.NONE:
            raise ValueError("Cannot calculate next due date for non-recurring todo")
        if current_due is None:
            raise ValueError("Cannot calculate next due date without current due date")

        if recurrence == Recurrence.DAILY:
            return current_due + timedelta(days=1)

        elif recurrence == Recurrence.WEEKLY:
            return current_due + timedelta(weeks=1)

        elif recurrence == Recurrence.MONTHLY:
            # Add one month, handle non-existent dates
            year = current_due.year
            month = current_due.month + 1
            if month > 12:
                month = 1
                year += 1

            target_day = current_due.day
            max_day = calendar.monthrange(year, month)[1]

            # If target day doesn't exist in next month, use last day
            day = min(target_day, max_day)

            return current_due.replace(year=year, month=month, day=day)

        else:
            return current_due

    def add_todo(
        self,
        title: str,
        description: str = "",
        priority: Priority = Priority.MEDIUM,
        tags: Optional[list[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence: Recurrence = Recurrence.NONE
    ) -> Todo:
        """
        Create and store a new todo.

        Args:
            title: Task summary (required, will be trimmed)
            description: Additional task details (optional)
            priority: Urgency level (default: MEDIUM)
            tags: Category labels (default: empty list)
            due_date: Due date and time (optional)
            recurrence: Recurrence pattern (default: NONE)

        Returns:
            The created Todo object

        Raises:
            ValueError: If title is empty, validation fails, or recurring todo has no due date
        """
        # Validate that recurring todos must have a due_date
        if recurrence != Recurrence.NONE and due_date is None:
            raise ValueError("Recurring todos require a due date")

        todo_id = self._generate_id()
        if tags is None:
            tags = []
        todo = Todo(
            id=todo_id,
            title=title,
            description=description,
            priority=priority,
            tags=tags,
            due_date=due_date,
            recurrence=recurrence
        )
        self.todos[todo_id] = todo
        return todo

    def get_all_todos(self) -> List[Todo]:
        """
        Return list of all todos, ordered by created_at.

        Returns:
            List of Todo objects sorted by creation time (oldest first)
        """
        return sorted(self.todos.values(), key=lambda t: t.created_at)

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo by ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            Todo object if found, None otherwise
        """
        return self.todos.get(todo_id)

    def update_todo(
        self,
        todo_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        priority: Optional[Priority] = None,
        tags: Optional[list[str]] = None,
        due_date: Optional[datetime] = None,
        recurrence: Optional[Recurrence] = None
    ) -> bool:
        """
        Update title, description, priority, tags, due_date, and/or recurrence of an existing todo.

        Args:
            todo_id: The ID of the todo to update
            title: New title (if provided)
            description: New description (if provided)
            priority: New priority level (if provided)
            tags: New tags list (if provided)
            due_date: New due date (if provided, use "clear" sentinel to remove)
            recurrence: New recurrence pattern (if provided)

        Returns:
            True if updated successfully, False if todo not found
        """
        todo = self.todos.get(todo_id)
        if not todo:
            return False

        if title is not None:
            # Create temp todo to validate title
            temp = Todo(id=todo_id, title=title)
            todo.title = temp.title  # Use validated & trimmed title

        if description is not None:
            # Validate description length
            if len(description) > 1000:
                raise ValueError("Description cannot exceed 1000 characters")
            todo.description = description

        if priority is not None:
            if not isinstance(priority, Priority):
                raise ValueError("Priority must be a Priority enum member")
            todo.priority = priority

        if tags is not None:
            # Validate and normalize tags
            if not isinstance(tags, list):
                raise ValueError("Tags must be a list")
            # Use Todo's normalization by creating temp object
            temp = Todo(id=todo_id, title="temp", tags=tags)
            todo.tags = temp.tags

        if due_date is not None:
            if not isinstance(due_date, datetime):
                raise ValueError("due_date must be a datetime object")
            todo.due_date = due_date

        if recurrence is not None:
            if not isinstance(recurrence, Recurrence):
                raise ValueError("Recurrence must be a Recurrence enum member")
            # Validate that recurring todos must have a due_date
            if recurrence != Recurrence.NONE and todo.due_date is None:
                raise ValueError("Recurring todos require a due date")
            todo.recurrence = recurrence

        return True

    def delete_todo(self, todo_id: int) -> bool:
        """
        Remove a todo from storage.

        Args:
            todo_id: The ID of the todo to delete

        Returns:
            True if deleted successfully, False if todo not found
        """
        if todo_id in self.todos:
            del self.todos[todo_id]
            return True
        return False

    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as complete. If recurring, create next instance.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            New todo instance if recurring, None otherwise or if todo not found
        """
        todo = self.todos.get(todo_id)
        if not todo:
            return None

        todo.mark_complete()

        # Only reschedule if this is the active recurring instance
        if todo.recurrence != Recurrence.NONE and todo.is_recurring_parent and todo.due_date:
            next_due = self._calculate_next_due_date(todo.due_date, todo.recurrence)
            new_todo = self.add_todo(
                title=todo.title,
                description=todo.description,
                priority=todo.priority,
                tags=todo.tags.copy(),
                due_date=next_due,
                recurrence=todo.recurrence
            )
            # Mark original as no longer the parent
            todo.is_recurring_parent = False
            return new_todo

        return None

    def search_todos(self, keyword: str) -> List[Todo]:
        """
        Search todos by keyword (case-insensitive, searches title and description).

        Args:
            keyword: Search term to match against title and description

        Returns:
            List of matching Todo objects, ordered by creation time
        """
        if not keyword or not keyword.strip():
            return []

        keyword_lower = keyword.lower()
        matching = [
            todo for todo in self.todos.values()
            if keyword_lower in todo.title.lower()
            or keyword_lower in todo.description.lower()
        ]
        return sorted(matching, key=lambda t: t.created_at)

    def filter_by_status(self, completed: bool) -> List[Todo]:
        """
        Filter todos by completion status.

        Args:
            completed: True for completed todos, False for incomplete

        Returns:
            List of matching Todo objects, ordered by creation time
        """
        matching = [todo for todo in self.todos.values() if todo.completed == completed]
        return sorted(matching, key=lambda t: t.created_at)

    def filter_by_priority(self, priority: Priority) -> List[Todo]:
        """
        Filter todos by priority level.

        Args:
            priority: Priority level to filter by

        Returns:
            List of matching Todo objects, ordered by creation time
        """
        matching = [todo for todo in self.todos.values() if todo.priority == priority]
        return sorted(matching, key=lambda t: t.created_at)

    def filter_by_tag(self, tag: str) -> List[Todo]:
        """
        Filter todos by tag (case-insensitive).

        Args:
            tag: Tag to filter by

        Returns:
            List of matching Todo objects, ordered by creation time
        """
        tag_lower = tag.lower()
        matching = [todo for todo in self.todos.values() if tag_lower in todo.tags]
        return sorted(matching, key=lambda t: t.created_at)

    def sort_todos(self, todos: Optional[List[Todo]] = None, sort_by: str = "priority") -> List[Todo]:
        """
        Sort todos by specified criteria.

        Args:
            todos: List of todos to sort (if None, sorts all todos)
            sort_by: Sort criteria - "priority", "date_newest", "date_oldest", "title", "due_date", "due_date_desc"

        Returns:
            Sorted list of Todo objects
        """
        if todos is None:
            todos = list(self.todos.values())

        if sort_by == "priority":
            return sorted(todos, key=lambda t: t.priority.value)
        elif sort_by == "date_newest":
            return sorted(todos, key=lambda t: t.created_at, reverse=True)
        elif sort_by == "date_oldest":
            return sorted(todos, key=lambda t: t.created_at)
        elif sort_by == "title":
            return sorted(todos, key=lambda t: t.title.lower())
        elif sort_by == "due_date":
            # Todos without due dates go to the end
            return sorted(todos, key=lambda t: t.due_date or datetime.max)
        elif sort_by == "due_date_desc":
            # Todos without due dates go to the start
            return sorted(todos, key=lambda t: t.due_date or datetime.min, reverse=True)
        else:
            return todos

    def get_overdue_todos(self) -> List[Todo]:
        """
        Return all overdue todos (past due date, not complete).

        Returns:
            List of overdue todos, sorted by due date (earliest/most overdue first)
        """
        now = datetime.now()
        overdue = [
            t for t in self.todos.values()
            if t.due_date and t.due_date < now and not t.completed
        ]
        return sorted(overdue, key=lambda t: t.due_date)

    def get_upcoming_todos(self) -> List[Todo]:
        """
        Return all todos due within the next 7 days (not complete).

        Returns:
            List of upcoming todos, sorted by due date (earliest first)
        """
        now = datetime.now()
        seven_days = now + timedelta(days=7)
        upcoming = [
            t for t in self.todos.values()
            if t.due_date and now <= t.due_date <= seven_days and not t.completed
        ]
        return sorted(upcoming, key=lambda t: t.due_date)
