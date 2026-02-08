# In-Memory Python Console Todo App

**Phase II** of the Multi-Phase Todo System - A command-line todo application with clean architecture, intermediate features, and advanced scheduling capabilities.

## Features

✅ **Full CRUD Operations**
- Add new todos with title and description
- View all todos in a formatted table
- Update existing todo titles and descriptions
- Delete todos with confirmation
- Mark todos as complete

✅ **Priority Management** (Phase I.5)
- Assign priority levels: High, Medium, Low
- Default priority: Medium
- Update priority for existing todos
- Priority displayed in todo list

✅ **Tag/Category System** (Phase I.5)
- Assign multiple tags to each todo
- Tags normalized (lowercase, trimmed, deduplicated)
- Comma-separated input format
- Tags displayed in todo list

✅ **Search Functionality** (Phase I.5)
- Search by keyword across title and description
- Case-insensitive substring matching
- View matching todos in formatted table

✅ **Filter Operations** (Phase I.5)
- Filter by completion status (complete/incomplete)
- Filter by priority level (high/medium/low)
- Filter by tag/category
- Optional sorting of filtered results

✅ **Sort Operations** (Phase I.5)
- Sort by priority (high → medium → low)
- Sort by creation date (newest or oldest first)
- Sort alphabetically by title (A-Z)
- Sort by due date (earliest or latest first)
- Stable sort preserves creation order for equal keys

✅ **Due Dates & Scheduling** (Phase II)
- Assign optional due dates in YYYY-MM-DD HH:MM format
- Visual indicators: ⚠ for overdue, 📅 for due soon (within 7 days)
- View upcoming todos (due within next 7 days)
- View overdue todos (past due, not complete)
- Due date sorting and filtering

✅ **Recurring Tasks** (Phase II)
- Create recurring todos: daily, weekly, or monthly
- Auto-reschedule on completion
- Monthly recurrence handles non-existent dates (e.g., Jan 31 → Feb 28)
- Disable or modify recurrence patterns
- Recurring todos marked with 🔁 icon

✅ **Clean Architecture**
- **Model Layer**: Todo dataclass with validation
- **Service Layer**: Business logic and CRUD operations
- **CLI Layer**: User interaction and display formatting

✅ **Robust Validation**
- Title required (max 200 characters)
- Description optional (max 1000 characters)
- ID existence validation
- Input type validation

✅ **Test Coverage**
- 46 total tests (12 model, 15 service, 19 integration)
- 88% overall coverage
- 100% coverage on models, 98% on service

## Quick Start

### Prerequisites

- Python 3.11 or later
- UV package manager

### Installation

```bash
# Install UV if not already installed
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
cd "todo app"

# Install dependencies
uv sync

# Run the application
uv run python -m todo_app
```

### Usage

The app presents a numbered menu with 11 options:

```
========== Todo App Menu ==========
1. Add Todo
2. View All Todos
3. View Upcoming Todos
4. View Overdue Todos
5. Update Todo
6. Delete Todo
7. Mark Todo as Complete
8. Search Todos
9. Filter Todos
10. Sort Todos
11. Exit
===================================
```

Simply enter the number (1-11) to select an option.

**Enhanced Workflows**:
- **Add Todo**: Prompts for title, description, priority, tags, due date (YYYY-MM-DD HH:MM), and recurrence (none/daily/weekly/monthly)
- **Update Todo**: Allows updating all fields including due date and recurrence
- **View Todos**: Displays priority, tags, due date with status indicators, and recurrence
- **View Upcoming**: Shows todos due within next 7 days
- **View Overdue**: Shows todos past their due date (not complete)
- **Mark Complete**: Auto-reschedules recurring tasks to next occurrence
- **Search**: Enter keyword to find todos by title or description
- **Filter**: Choose status, priority, or tag filter with optional sorting (including due date sort)
- **Sort**: Sort all todos by priority, date, title, or due date

## Project Structure

```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py       # Package initialization
│       ├── __main__.py       # Entry point
│       ├── models.py         # Todo dataclass
│       ├── service.py        # Business logic
│       └── cli.py            # CLI interactions
├── tests/
│   ├── unit/
│   │   ├── test_models.py    # Model tests
│   │   └── test_service.py   # Service tests
│   └── integration/
│       ├── test_cli.py       # CLI flow tests
│       └── test_main.py      # Entry point tests
├── specs/
│   └── 001-console-todo/     # Design documents
├── pyproject.toml            # Project configuration
└── README.md                 # This file
```

## Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/todo_app --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_models.py -v
```

## Architecture

The application follows the **Clean Architecture** pattern with clear separation of concerns:

- **Models** (`models.py`): Domain entities with validation
- **Service** (`service.py`): Business logic, CRUD operations, in-memory storage
- **CLI** (`cli.py`): User interface, input/output formatting
- **Entry Point** (`__main__.py`): Application lifecycle management

This design enables easy migration to Phase II (web application) by reusing the model and service layers.

## Key Design Decisions

- **In-memory storage**: Dictionary-based storage (data lost on exit)
- **Sequential IDs**: Auto-generated, never reused after deletion
- **Menu-driven UI**: Numbered choices for ease of use
- **Validation-first**: All inputs validated before processing
- **TDD approach**: Tests written before implementation

## Limitations (Phase II)

- No persistence (data lost on exit)
- Single-user only
- No undo functionality
- Console-only interface
- No fuzzy search or regex matching
- No combined multi-dimensional filtering (e.g., status AND priority simultaneously)
- No natural language date input (requires YYYY-MM-DD HH:MM format)
- Simple recurrence only (daily/weekly/monthly, no complex patterns)
- Session-scoped recurring (tasks only reschedule when marked complete during session)

These will be addressed in future phases (persistence, web app, AI integration, cloud deployment).

## Documentation

For detailed documentation, see:
- **Specification**: `specs/001-console-todo/spec.md`
- **Implementation Plan**: `specs/001-console-todo/plan.md`
- **Data Model**: `specs/001-console-todo/data-model.md`
- **CLI Contract**: `specs/001-console-todo/contracts/cli-interface.md`
- **Quickstart Guide**: `specs/001-console-todo/quickstart.md`

## Development

### Adding Features

1. Update `specs/001-console-todo/spec.md` with new user story
2. Run `/sp.plan` to update implementation plan
3. Run `/sp.tasks` to generate task breakdown
4. Implement following TDD (tests first, then code)

### Contributing

This is a learning project following Spec-Driven Development (SDD) methodology. All changes should:
- Follow the existing architecture
- Include tests with >90% coverage
- Update relevant documentation

## License

Educational project - GIAIC Quarter 4 Hackathon

## Version

**0.3.0** - Phase II Console Application with Advanced Scheduling (Due Dates, Recurring Tasks, Upcoming/Overdue Views)
