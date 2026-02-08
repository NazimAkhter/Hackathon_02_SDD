"""Specific tests for __main__.py entry point as requested by user."""
import pytest
from unittest.mock import patch
from io import StringIO
import sys


def test_main_module_execution():
    """Test that __main__.py can be executed as a module."""
    # This verifies the module can be imported and run
    from src.todo_app import __main__
    assert hasattr(__main__, 'main')
    assert callable(__main__.main)


def test_main_welcome_and_menu_display():
    """Test that main() displays welcome message and menu."""
    from src.todo_app.__main__ import main

    inputs = ['6']  # Exit immediately

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

            # Check welcome message
            assert "Welcome to Todo App" in output
            # Check menu displays
            assert "Todo App Menu" in output
            assert "1. Add Todo" in output
            assert "2. View All Todos" in output
            assert "3. Update Todo" in output
            assert "4. Delete Todo" in output
            assert "5. Mark Todo as Complete" in output
            assert "6. Exit" in output


def test_main_goodbye_message():
    """Test that main() displays goodbye message on exit."""
    from src.todo_app.__main__ import main

    inputs = ['6']  # Exit

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

            assert "Thank you for using Todo App!" in output
            assert "All data will be lost (in-memory only)." in output
            assert "Goodbye!" in output


def test_main_keyboard_interrupt_handling():
    """Test that Ctrl+C is handled gracefully."""
    from src.todo_app.__main__ import main

    # Simulate KeyboardInterrupt during input
    with patch('builtins.input', side_effect=KeyboardInterrupt()):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with pytest.raises(SystemExit) as exc_info:
                main()

            output = fake_out.getvalue()
            assert "Exiting... Goodbye!" in output
            assert exc_info.value.code == 0


def test_main_full_crud_workflow():
    """Test a complete CRUD workflow through main()."""
    from src.todo_app.__main__ import main

    inputs = [
        '1', 'Task 1', 'Description 1',  # Add first todo
        '2',  # View todos
        '5', '1',  # Mark todo 1 complete
        '3', '1', 'Updated Task 1', '',  # Update todo 1 title
        '1', 'Task 2', '',  # Add second todo
        '4', '2', 'y',  # Delete todo 2
        '2',  # View final state
        '6'  # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

            # Verify all operations succeeded
            assert "Todo added successfully!" in output
            assert "Todo marked as complete!" in output
            assert "Todo updated successfully!" in output
            assert "Todo deleted successfully!" in output

            # Verify final state shows updated task 1
            assert "Updated Task 1" in output
            assert "[✓]" in output  # Completed status


def test_main_error_handling():
    """Test that main() handles errors gracefully."""
    from src.todo_app.__main__ import main

    inputs = [
        '1', '', 'Valid Title', '',  # Try empty title, then valid
        '3', '999',  # Try to update non-existent todo
        '4', '999',  # Try to delete non-existent todo
        '5', '999',  # Try to mark non-existent todo complete
        '6'  # Exit
    ]

    with patch('builtins.input', side_effect=inputs):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

            # Check error messages appear
            assert "Title cannot be empty" in output
            assert "Todo with ID 999 not found" in output
            # But app should continue running
            assert "Goodbye!" in output


def test_main_service_isolation():
    """Test that each main() call starts with fresh service instance."""
    from src.todo_app.__main__ import main

    # First run: add a todo
    inputs1 = ['1', 'Task 1', '', '6']
    with patch('builtins.input', side_effect=inputs1):
        with patch('sys.stdout', new=StringIO()):
            main()

    # Second run: should not have the previous todo (fresh service)
    inputs2 = ['2', '6']  # View todos
    with patch('builtins.input', side_effect=inputs2):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

            # Should show no todos (fresh service instance)
            assert "No todos found" in output


def test_main_module_name_guard():
    """Test that __name__ == '__main__' guard works correctly."""
    # This test verifies the module can be imported without executing main()
    # The import below should not trigger main() execution
    import importlib
    import sys

    # Remove module if already imported
    if 'src.todo_app.__main__' in sys.modules:
        del sys.modules['src.todo_app.__main__']

    # Import without triggering execution
    with patch('builtins.input') as mock_input:
        module = importlib.import_module('src.todo_app.__main__')

        # main() should not have been called during import
        mock_input.assert_not_called()

        # But main function should exist
        assert hasattr(module, 'main')
        assert callable(module.main)
