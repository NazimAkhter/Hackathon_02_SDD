"""Business logic and CRUD operations for todos."""
from typing import Dict, List, Optional
from src.todo_app.models import Todo


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

    def add_todo(self, title: str, description: str = "") -> Todo:
        """
        Create and store a new todo.

        Args:
            title: Task summary (required, will be trimmed)
            description: Additional task details (optional)

        Returns:
            The created Todo object

        Raises:
            ValueError: If title is empty or validation fails
        """
        todo_id = self._generate_id()
        todo = Todo(id=todo_id, title=title, description=description)
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
        description: Optional[str] = None
    ) -> bool:
        """
        Update title and/or description of an existing todo.

        Args:
            todo_id: The ID of the todo to update
            title: New title (if provided)
            description: New description (if provided)

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

    def mark_complete(self, todo_id: int) -> bool:
        """
        Mark a todo as complete.

        Args:
            todo_id: The ID of the todo to mark complete

        Returns:
            True if marked complete, False if todo not found
        """
        todo = self.todos.get(todo_id)
        if not todo:
            return False
        todo.mark_complete()
        return True
