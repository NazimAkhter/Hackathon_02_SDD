# Quickstart Guide: In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Target Audience**: Beginner-intermediate Python developers
**Estimated Setup Time**: 5-10 minutes

## Purpose

Get the Phase I In-Memory Python Console Todo App running on your machine in under 10 minutes. This guide covers installation, first run, basic usage, and validation.

---

## Prerequisites

### Required

- **Python 3.13 or later**
  - Check version: `python --version` or `python3 --version`
  - Download: https://www.python.org/downloads/

- **UV Package Manager**
  - Fast Python package manager (Rust-based)
  - Install: `curl -LsSf https://astral.sh/uv/install.sh | sh`
  - Verify: `uv --version`

### Optional (Recommended)

- **Git** - For version control
  - Verify: `git --version`

- **Terminal/Console** - Any Unix shell (bash, zsh) or Windows PowerShell

---

## Installation

### Step 1: Clone or Download the Project

**If using Git**:
```bash
# Clone the repository
git clone <repository-url>
cd todo-app

# Checkout the Phase I branch
git checkout 001-console-todo
```

**If not using Git**:
- Download the project ZIP from the repository
- Extract to a folder named `todo-app`
- Navigate to that folder in your terminal

### Step 2: Verify Project Structure

Your folder should contain:
```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── __main__.py
│       ├── models.py
│       ├── service.py
│       └── cli.py
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml
└── README.md
```

### Step 3: Install Dependencies

UV automatically creates a virtual environment and installs dependencies:

```bash
# Install project in development mode
uv sync

# Verify installation
uv run python -m todo_app --help  # Should show usage info (if help flag implemented)
```

**Expected Output**:
```
Setting up virtual environment...
Installing dependencies...
✓ Dependencies installed successfully
```

---

## First Run

### Launch the Application

```bash
uv run python -m todo_app
```

**Expected Initial Screen**:
```
========================================
       Welcome to Todo App
========================================

========== Todo App Menu ==========
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo as Complete
6. Exit
===================================

Enter your choice (1-6):
```

### Quick Tutorial: Add Your First Todo

1. **Select "Add Todo"**:
   ```
   Enter your choice (1-6): 1
   ```

2. **Enter todo details**:
   ```
   --- Add New Todo ---
   Enter title: Buy groceries
   Enter description (optional, press Enter to skip): Milk, eggs, bread

   ✓ Todo added successfully! (ID: 1)
   ```

3. **View your todo**:
   ```
   Enter your choice (1-6): 2

   --- All Todos ---

    ID | Status | Title                          | Description
   ----+--------+--------------------------------+---------------------------
     1 | [ ]    | Buy groceries                  | Milk, eggs, bread

   Total: 1 todos (0 completed, 1 incomplete)
   ```

4. **Mark as complete**:
   ```
   Enter your choice (1-6): 5

   --- Mark Todo as Complete ---
   Enter todo ID: 1

   Todo marked as complete!
     Title: Buy groceries
     Description: Milk, eggs, bread
   ```

5. **Verify completion**:
   ```
   Enter your choice (1-6): 2

   --- All Todos ---

    ID | Status | Title                          | Description
   ----+--------+--------------------------------+---------------------------
     1 | [✓]    | Buy groceries                  | Milk, eggs, bread

   Total: 1 todos (1 completed, 0 incomplete)
   ```

6. **Exit the application**:
   ```
   Enter your choice (1-6): 6

   Thank you for using Todo App!
   All data will be lost (in-memory only).
   Goodbye!
   ```

---

## Usage Guide

### Add a New Todo

**Menu Option**: 1

**Steps**:
1. Select option `1`
2. Enter a title (required, max 200 characters)
3. Enter a description (optional, max 1000 characters) or press Enter to skip
4. Todo is created with a unique ID

**Example**:
```
Enter your choice (1-6): 1

--- Add New Todo ---
Enter title: Finish project report
Enter description (optional): Q4 analysis with charts

✓ Todo added successfully! (ID: 2)
```

**Validation**:
- Title cannot be empty
- Title/description length limits enforced
- Leading/trailing whitespace is automatically trimmed

---

### View All Todos

**Menu Option**: 2

**Steps**:
1. Select option `2`
2. All todos are displayed in a table format
3. Status shows `[ ]` for incomplete, `[✓]` for complete

**Example**:
```
Enter your choice (1-6): 2

--- All Todos ---

 ID | Status | Title                          | Description
----+--------+--------------------------------+---------------------------
  1 | [✓]    | Buy groceries                  | Milk, eggs, bread
  2 | [ ]    | Finish project report          | Q4 analysis with charts
  3 | [ ]    | Call dentist                   |

Total: 3 todos (1 completed, 2 incomplete)
```

**Behavior**:
- Todos ordered by creation time (oldest first)
- Long titles/descriptions truncated with "..."
- If no todos exist, shows "No todos found" message

---

### Update a Todo

**Menu Option**: 3

**Steps**:
1. Select option `3`
2. Enter the ID of the todo to update
3. Enter new title (or press Enter to keep current)
4. Enter new description (or press Enter to keep current)

**Example**:
```
Enter your choice (1-6): 3

--- Update Todo ---
Enter todo ID: 2

Current Todo:
  ID: 2
  Title: Finish project report
  Description: Q4 analysis with charts
  Status: Incomplete

Enter new title (press Enter to keep current): Finish Q4 project report
Enter new description (press Enter to keep current): Complete analysis with charts and recommendations

✓ Todo updated successfully!
```

**Validation**:
- ID must exist
- New title/description follow same validation as Add Todo
- Pressing Enter without input keeps current value

---

### Delete a Todo

**Menu Option**: 4

**Steps**:
1. Select option `4`
2. Enter the ID of the todo to delete
3. Review the todo details
4. Confirm deletion with `y` or cancel with `n`

**Example**:
```
Enter your choice (1-6): 4

--- Delete Todo ---
Enter todo ID: 3

Are you sure you want to delete this todo?
  Title: Call dentist
  Description:

Confirm deletion (y/n): y

✓ Todo deleted successfully!
```

**Behavior**:
- Requires confirmation before deletion
- ID is not reused (e.g., if you delete ID 3, next new todo will be ID 4)
- Deletion is permanent (no undo in Phase I)

---

### Mark Todo as Complete

**Menu Option**: 5

**Steps**:
1. Select option `5`
2. Enter the ID of the todo to mark as complete

**Example**:
```
Enter your choice (1-6): 5

--- Mark Todo as Complete ---
Enter todo ID: 2

Todo marked as complete!
  Title: Finish Q4 project report
  Description: Complete analysis with charts and recommendations
```

**Behavior**:
- Changes status from incomplete `[ ]` to complete `[✓]`
- If already complete, shows info message (not error)
- Idempotent (calling twice is safe)

**Note**: Phase I does NOT support unmarking (complete → incomplete). This may be added in Phase II.

---

### Exit the Application

**Menu Option**: 6

**Steps**:
1. Select option `6`
2. Application displays goodbye message and exits

**Example**:
```
Enter your choice (1-6): 6

Thank you for using Todo App!
All data will be lost (in-memory only).
Goodbye!
```

**Alternative Exit**:
- Press `Ctrl+C` at any prompt to exit immediately
- Shows: "Exiting... Goodbye!"

---

## Validation Checklist

After installation, verify the application works correctly:

- [ ] **Application launches**: `uv run python -m todo_app` shows main menu
- [ ] **Add todo works**: Can create a todo with title and description
- [ ] **View works**: Can see added todo in the list
- [ ] **Mark complete works**: Can mark todo as complete, status changes to `[✓]`
- [ ] **Update works**: Can modify todo title and/or description
- [ ] **Delete works**: Can delete a todo after confirmation
- [ ] **Empty title rejected**: Trying to add todo with empty title shows error
- [ ] **Invalid ID handled**: Entering non-existent ID shows "not found" error
- [ ] **Exit works**: Option 6 cleanly exits the application

**Success Criteria Met**:
- ✅ SC-001: Adding todo completes in under 5 seconds
- ✅ SC-002: Complete/incomplete todos visually distinct (`[ ]` vs `[✓]`)
- ✅ SC-003: All CRUD operations work without errors

---

## Running Tests

### Run All Tests

```bash
# Run unit and integration tests
uv run pytest

# Run with coverage report
uv run pytest --cov=src/todo_app --cov-report=term-missing
```

**Expected Output**:
```
==================== test session starts ====================
collected 25 items

tests/unit/test_models.py ............                  [ 48%]
tests/unit/test_service.py .........                    [ 84%]
tests/integration/test_cli.py ....                      [100%]

==================== 25 passed in 0.42s =====================
```

### Run Specific Test Files

```bash
# Unit tests only
uv run pytest tests/unit/

# Integration tests only
uv run pytest tests/integration/

# Specific test file
uv run pytest tests/unit/test_models.py
```

### Test Coverage Goal

Target: **90%+ coverage** for service layer (business logic)

```bash
uv run pytest --cov=src/todo_app --cov-report=html
# Open htmlcov/index.html in browser to view detailed coverage
```

---

## Troubleshooting

### Issue: "command not found: uv"

**Solution**: UV not installed or not in PATH

```bash
# Install UV
curl -LsSf https://astral.sh/uv/install.sh | sh

# Add to PATH (if needed)
export PATH="$HOME/.cargo/bin:$PATH"  # Add to ~/.bashrc or ~/.zshrc

# Verify
uv --version
```

### Issue: "Python version 3.13 not found"

**Solution**: Install Python 3.13+

```bash
# Check current version
python3 --version

# If < 3.13, download from python.org or use package manager
# macOS: brew install python@3.13
# Ubuntu: sudo apt install python3.13
# Windows: Download installer from python.org
```

### Issue: Application doesn't start after installation

**Solution**: Reinstall dependencies

```bash
# Remove existing virtual environment
rm -rf .venv

# Reinstall
uv sync

# Try running again
uv run python -m todo_app
```

### Issue: "ModuleNotFoundError: No module named 'todo_app'"

**Solution**: Ensure you're in the project root and using `uv run`

```bash
# Check current directory
pwd  # Should show .../todo-app

# Verify src/ folder exists
ls src/todo_app/  # Should show __main__.py, models.py, etc.

# Run with uv
uv run python -m todo_app
```

### Issue: Tests fail with import errors

**Solution**: Install test dependencies

```bash
uv add --dev pytest pytest-cov pytest-mock
uv sync
uv run pytest
```

---

## Known Limitations (Phase I)

These are intentional constraints for Phase I:

1. **No persistence**: All data lost when app exits (in-memory only)
2. **No multi-user support**: Single-user application
3. **No filtering/search**: View shows all todos (cannot filter by status, search by keyword)
4. **No sorting options**: Always ordered by creation time
5. **No undo**: Deleted todos cannot be recovered
6. **No unmark complete**: Cannot change status from complete → incomplete
7. **No priority/tags**: Basic todo structure only
8. **No due dates**: No time-based features

These limitations will be addressed in future phases:
- **Phase II**: Persistence (database), multi-user, search/filter
- **Phase III**: AI-powered priority/tags, smart search
- **Phase IV/V**: Distributed system, advanced features

---

## Next Steps

### For Users

1. **Add your real todos**: Use the app for actual task tracking
2. **Explore edge cases**: Try long titles, Unicode characters, many todos
3. **Test error handling**: Try invalid inputs to see error messages
4. **Provide feedback**: Report issues or suggestions to the development team

### For Developers

1. **Review the code**:
   - Read `src/todo_app/models.py` to understand the Todo entity
   - Review `src/todo_app/service.py` for business logic
   - Explore `src/todo_app/cli.py` for user interaction patterns

2. **Run tests**:
   ```bash
   uv run pytest --cov=src/todo_app --cov-report=term-missing
   ```

3. **Extend the application** (learning exercises):
   - Add a "view incomplete only" filter
   - Implement todo sorting (by title, creation date)
   - Add color output (using `colorama` library)

4. **Prepare for Phase II**:
   - Review `data-model.md` for Phase II migration notes
   - Understand how Todo model will map to SQLModel
   - Plan API endpoints based on current CLI operations

---

## Support & Resources

### Documentation

- **Specification**: `specs/001-console-todo/spec.md` - Feature requirements
- **Implementation Plan**: `specs/001-console-todo/plan.md` - Architecture and decisions
- **Data Model**: `specs/001-console-todo/data-model.md` - Todo entity definition
- **CLI Contract**: `specs/001-console-todo/contracts/cli-interface.md` - Interface specification

### Commands Reference

| Task                     | Command                              |
|--------------------------|--------------------------------------|
| Install dependencies     | `uv sync`                            |
| Run application          | `uv run python -m todo_app`          |
| Run tests                | `uv run pytest`                      |
| Run tests with coverage  | `uv run pytest --cov=src/todo_app`   |
| Add dependency           | `uv add <package>`                   |
| Add dev dependency       | `uv add --dev <package>`             |
| Update dependencies      | `uv sync --upgrade`                  |

### Getting Help

- Check this quickstart guide first
- Review troubleshooting section above
- Consult the full specification in `specs/001-console-todo/spec.md`
- For bugs/issues: Create an issue in the project repository

---

## Success!

You've successfully set up and run the Phase I In-Memory Python Console Todo App!

**You can now**:
- ✅ Add, view, update, delete, and mark todos as complete
- ✅ Understand the clean architecture (model → service → CLI layers)
- ✅ Run automated tests to verify functionality
- ✅ Prepare for Phase II (web application with persistence)

**Remember**: This is Phase I of a 5-phase journey:
- **Phase I** (Current): ✅ Console app, in-memory storage
- **Phase II** (Next): Web app with FastAPI, Next.js, Neon DB
- **Phase III**: AI-powered chatbot using OpenAI ChatKit
- **Phase IV**: Kubernetes deployment with Minikube
- **Phase V**: Cloud deployment on DigitalOcean with Kafka & Dapr

Enjoy using Todo App, and happy coding! 🚀
