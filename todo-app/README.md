# In-Memory Python Console Todo App

**Phase I** of the Multi-Phase Todo System - A command-line todo application with clean architecture.

## Features

✅ **Full CRUD Operations**
- Add new todos with title and description
- View all todos in a formatted table
- Update existing todo titles and descriptions
- Delete todos with confirmation
- Mark todos as complete

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

The app presents a numbered menu with 6 options:

```
========== Todo App Menu ==========
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo as Complete
6. Exit
===================================
```

Simply enter the number (1-6) to select an option.

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

## Limitations (Phase I)

- No persistence (data lost on exit)
- Single-user only
- No filtering or search
- No undo functionality
- Console-only interface

These will be addressed in future phases (web app, AI integration, cloud deployment).

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

**0.1.0** - Phase I Console Application
