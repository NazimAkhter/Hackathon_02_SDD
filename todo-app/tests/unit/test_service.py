"""Unit tests for TodoService."""
import pytest
from src.todo_app.service import TodoService
from src.todo_app.models import Todo


class TestAddTodo:
    """Test adding todos."""

    def test_add_todo_creates_with_id(self):
        """Test that add_todo creates todo with generated ID."""
        service = TodoService()
        todo = service.add_todo("Buy milk", "Whole milk")
        assert todo.id == 1
        assert todo.title == "Buy milk"
        assert todo.description == "Whole milk"
        assert todo.completed == False

    def test_add_todo_increments_ids(self):
        """Test that IDs increment sequentially."""
        service = TodoService()
        todo1 = service.add_todo("Task 1")
        todo2 = service.add_todo("Task 2")
        todo3 = service.add_todo("Task 3")
        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

    def test_add_todo_trims_title(self):
        """Test that title whitespace is trimmed."""
        service = TodoService()
        todo = service.add_todo("  Buy groceries  ")
        assert todo.title == "Buy groceries"


class TestGetTodos:
    """Test retrieving todos."""

    def test_get_all_todos_empty(self):
        """Test get_all_todos returns empty list when no todos."""
        service = TodoService()
        todos = service.get_all_todos()
        assert todos == []

    def test_get_all_todos_ordered(self):
        """Test get_all_todos returns todos ordered by created_at."""
        service = TodoService()
        todo1 = service.add_todo("First")
        todo2 = service.add_todo("Second")
        todo3 = service.add_todo("Third")

        todos = service.get_all_todos()
        assert len(todos) == 3
        assert todos[0].id == todo1.id
        assert todos[1].id == todo2.id
        assert todos[2].id == todo3.id

    def test_get_todo_by_id_found(self):
        """Test get_todo_by_id returns correct todo."""
        service = TodoService()
        todo = service.add_todo("Task")
        retrieved = service.get_todo_by_id(1)
        assert retrieved is not None
        assert retrieved.id == 1
        assert retrieved.title == "Task"

    def test_get_todo_by_id_not_found(self):
        """Test get_todo_by_id returns None for non-existent ID."""
        service = TodoService()
        retrieved = service.get_todo_by_id(999)
        assert retrieved is None


class TestUpdateTodo:
    """Test updating todos."""

    def test_update_todo_title(self):
        """Test updating only the title."""
        service = TodoService()
        todo = service.add_todo("Old title", "Description")
        result = service.update_todo(1, title="New title")
        assert result == True
        assert todo.title == "New title"
        assert todo.description == "Description"

    def test_update_todo_description(self):
        """Test updating only the description."""
        service = TodoService()
        todo = service.add_todo("Title", "Old description")
        result = service.update_todo(1, description="New description")
        assert result == True
        assert todo.title == "Title"
        assert todo.description == "New description"

    def test_update_todo_not_found(self):
        """Test updating non-existent todo returns False."""
        service = TodoService()
        result = service.update_todo(999, title="New title")
        assert result == False


class TestDeleteTodo:
    """Test deleting todos."""

    def test_delete_todo_success(self):
        """Test deleting existing todo."""
        service = TodoService()
        service.add_todo("Task")
        result = service.delete_todo(1)
        assert result == True
        assert service.get_todo_by_id(1) is None

    def test_delete_todo_not_found(self):
        """Test deleting non-existent todo returns False."""
        service = TodoService()
        result = service.delete_todo(999)
        assert result == False

    def test_id_generation_after_deletion(self):
        """Test that IDs are not reused after deletion."""
        service = TodoService()
        service.add_todo("Task 1")
        service.add_todo("Task 2")
        service.delete_todo(2)
        todo3 = service.add_todo("Task 3")
        assert todo3.id == 3  # Not 2


class TestMarkComplete:
    """Test marking todos complete."""

    def test_mark_complete_success(self):
        """Test marking todo as complete."""
        service = TodoService()
        todo = service.add_todo("Task")
        assert todo.completed == False
        result = service.mark_complete(1)
        assert result == True
        assert todo.completed == True

    def test_mark_complete_not_found(self):
        """Test marking non-existent todo returns False."""
        service = TodoService()
        result = service.mark_complete(999)
        assert result == False
