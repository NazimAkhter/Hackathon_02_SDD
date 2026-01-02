"""Unit tests for Todo model."""
import pytest
from datetime import datetime
from src.todo_app.models import Todo


class TestTodoCreation:
    """Test todo creation and defaults."""

    def test_todo_creation_with_defaults(self):
        """Test creating a todo with minimal required fields."""
        todo = Todo(id=1, title="Buy milk")
        assert todo.id == 1
        assert todo.title == "Buy milk"
        assert todo.description == ""
        assert todo.completed == False
        assert isinstance(todo.created_at, datetime)

    def test_todo_creation_with_all_fields(self):
        """Test creating a todo with all fields specified."""
        now = datetime.now()
        todo = Todo(
            id=2,
            title="Finish report",
            description="Q4 analysis",
            completed=True,
            created_at=now
        )
        assert todo.id == 2
        assert todo.title == "Finish report"
        assert todo.description == "Q4 analysis"
        assert todo.completed == True
        assert todo.created_at == now


class TestTodoValidation:
    """Test todo validation rules."""

    def test_todo_title_validation_empty(self):
        """Test that empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Todo(id=1, title="")

    def test_todo_title_validation_whitespace(self):
        """Test that whitespace-only title raises ValueError."""
        with pytest.raises(ValueError, match="Title cannot be empty"):
            Todo(id=1, title="   ")

    def test_todo_title_trimming(self):
        """Test that title whitespace is trimmed."""
        todo = Todo(id=1, title="  Buy groceries  ")
        assert todo.title == "Buy groceries"

    def test_todo_title_max_length(self):
        """Test that title exceeding 200 chars raises ValueError."""
        long_title = "x" * 201
        with pytest.raises(ValueError, match="Title cannot exceed 200 characters"):
            Todo(id=1, title=long_title)

    def test_todo_description_max_length(self):
        """Test that description exceeding 1000 chars raises ValueError."""
        long_desc = "x" * 1001
        with pytest.raises(ValueError, match="Description cannot exceed 1000 characters"):
            Todo(id=1, title="Valid title", description=long_desc)


class TestTodoMethods:
    """Test todo domain methods."""

    def test_todo_mark_complete(self):
        """Test marking todo as complete."""
        todo = Todo(id=1, title="Task")
        assert todo.completed == False
        todo.mark_complete()
        assert todo.completed == True

    def test_todo_mark_complete_idempotent(self):
        """Test that marking complete twice is safe."""
        todo = Todo(id=1, title="Task", completed=True)
        todo.mark_complete()
        assert todo.completed == True

    def test_todo_is_complete(self):
        """Test is_complete() returns correct status."""
        todo_incomplete = Todo(id=1, title="Task")
        todo_complete = Todo(id=2, title="Task", completed=True)
        assert todo_incomplete.is_complete() == False
        assert todo_complete.is_complete() == True

    def test_todo_str_incomplete(self):
        """Test __str__ format for incomplete todo."""
        todo = Todo(id=1, title="Buy milk", description="Whole milk")
        result = str(todo)
        assert "  1" in result
        assert "[ ]" in result
        assert "Buy milk" in result
        assert "Whole milk" in result

    def test_todo_str_complete(self):
        """Test __str__ format for complete todo."""
        todo = Todo(id=2, title="Call dentist", completed=True)
        result = str(todo)
        assert "  2" in result
        assert "[✓]" in result
        assert "Call dentist" in result
