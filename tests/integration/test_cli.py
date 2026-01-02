"""Integration tests for CLI flows."""
import pytest
from unittest.mock import patch
from io import StringIO
from src.todo_app.__main__ import main


class TestAddTodoFlow:
    """Test add todo integration."""

    def test_add_todo_flow(self):
        """Test full add todo flow with valid input."""
        inputs = [
            '1',  # Choose "Add Todo"
            'Buy milk',  # Title
            'Whole milk',  # Description
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                # Check success message appears
                assert "Todo added successfully!" in output
                assert "ID: 1" in output

    def test_add_todo_empty_title_error(self):
        """Test that empty title shows error and retries."""
        inputs = [
            '1',  # Choose "Add Todo"
            '',  # Empty title (should error)
            'Buy milk',  # Valid title
            '',  # No description
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                # Check error message appears
                assert "Title cannot be empty" in output
                # Check success after retry
                assert "Todo added successfully!" in output


class TestViewTodosFlow:
    """Test view todos integration."""

    def test_view_all_todos_flow(self):
        """Test viewing todos after adding some."""
        inputs = [
            '1', 'Task 1', 'Description 1',  # Add first todo
            '1', 'Task 2', 'Description 2',  # Add second todo
            '1', 'Task 3', '',  # Add third todo (no description)
            '2',  # View all todos
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                # Check all todos appear
                assert "Task 1" in output
                assert "Task 2" in output
                assert "Task 3" in output
                assert "Description 1" in output
                assert "Description 2" in output
                # Check summary
                assert "Total: 3 todos" in output

    def test_view_empty_todos(self):
        """Test viewing when no todos exist."""
        inputs = [
            '2',  # View all todos
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "No todos found" in output


class TestUpdateTodoFlow:
    """Test update todo integration."""

    def test_update_todo_flow(self):
        """Test updating todo title."""
        inputs = [
            '1', 'Original title', 'Original desc',  # Add todo
            '3',  # Update todo
            '1',  # Todo ID
            'Updated title',  # New title
            '',  # Keep description
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Todo updated successfully!" in output

    def test_update_todo_not_found_error(self):
        """Test updating non-existent todo shows error."""
        inputs = [
            '3',  # Update todo
            '999',  # Non-existent ID
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Todo with ID 999 not found" in output


class TestDeleteTodoFlow:
    """Test delete todo integration."""

    def test_delete_todo_flow(self):
        """Test deleting todo with confirmation."""
        inputs = [
            '1', 'Task to delete', '',  # Add todo
            '4',  # Delete todo
            '1',  # Todo ID
            'y',  # Confirm deletion
            '2',  # View todos (should be empty)
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Todo deleted successfully!" in output
                assert "No todos found" in output

    def test_delete_todo_cancelled(self):
        """Test cancelling deletion."""
        inputs = [
            '1', 'Task to keep', '',  # Add todo
            '4',  # Delete todo
            '1',  # Todo ID
            'n',  # Cancel deletion
            '2',  # View todos (should still exist)
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Deletion cancelled" in output
                assert "Task to keep" in output


class TestMarkCompleteFlow:
    """Test mark complete integration."""

    def test_mark_complete_flow(self):
        """Test marking todo as complete."""
        inputs = [
            '1', 'Task', 'Description',  # Add todo
            '5',  # Mark complete
            '1',  # Todo ID
            '2',  # View todos
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Todo marked as complete!" in output
                # Check that view shows completed status
                assert "[✓]" in output

    def test_mark_complete_not_found_error(self):
        """Test marking non-existent todo shows error."""
        inputs = [
            '5',  # Mark complete
            '999',  # Non-existent ID
            '6'  # Exit
        ]

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Todo with ID 999 not found" in output


class TestExitFlow:
    """Test application exit."""

    def test_exit_flow(self):
        """Test clean exit via menu option 6."""
        inputs = ['6']  # Exit immediately

        with patch('builtins.input', side_effect=inputs):
            with patch('sys.stdout', new=StringIO()) as fake_out:
                main()
                output = fake_out.getvalue()

                assert "Thank you for using Todo App!" in output
                assert "Goodbye!" in output
