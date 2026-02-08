# Research & Technical Decisions: In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2026-01-02
**Phase**: 0 (Research)

## Purpose

Document technical decisions, alternatives considered, and rationale for implementation choices in Phase I of the Multi-Phase Todo System.

## Key Technical Decisions

### 1. Data Structure for In-Memory Storage

**Decision**: Use Python dictionary with integer keys mapping to Todo objects

**Rationale**:
- O(1) lookup by ID (primary access pattern for update/delete/mark-complete operations)
- Natural mapping of ID → Todo entity
- Easy to implement sequential ID generation (max(keys) + 1 or len(dict) + 1)
- Supports iteration for "view all" operation
- Familiar pattern for beginner-intermediate Python developers

**Alternatives Considered**:
- **List of Todo objects**: O(n) lookup by ID requires linear search; rejected because update/delete/mark operations would be inefficient
- **List with index as ID**: Fragile when deleting (creates gaps or requires re-indexing); complicates ID management
- **Dataclass with __dict__**: Over-engineered for simple in-memory storage; adds unnecessary abstraction

**Implementation Details**:
```python
# Example structure (not actual implementation code)
todos = {
    1: Todo(id=1, title="...", description="...", completed=False, created_at=...),
    2: Todo(id=2, title="...", description="...", completed=True, created_at=...)
}
```

---

### 2. Menu Style: Numbered Menu vs. Typed Commands

**Decision**: Numbered menu with user input selection (1-6)

**Rationale**:
- Lower cognitive load for users (select number vs. remember command names)
- Reduces input errors (single digit vs. typing "update-todo")
- Clear visual presentation of all available options
- Familiar pattern from legacy terminal applications
- Easier input validation (check if 1-6 vs. parse command strings)

**Alternatives Considered**:
- **Typed commands** (e.g., "add", "delete", "list"): More flexible and scriptable, but higher error rate for manual use; better for Phase II CLI tools
- **Single-letter shortcuts** (a/d/u/v/m/q): Compact but less discoverable; requires memorization

**Menu Design**:
```
========== Todo App ==========
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo as Complete
6. Exit
==============================
Enter your choice (1-6):
```

---

### 3. Error Handling Strategy

**Decision**: Defensive validation with user-friendly error messages and retry prompts

**Rationale**:
- Prevents application crashes from invalid input (empty titles, non-numeric IDs, out-of-range menu choices)
- Supports success criterion SC-006 (self-correcting error messages)
- Maintains application loop instead of terminating on errors
- Educational for beginner developers to see validation patterns

**Error Handling Patterns**:
1. **Input Validation**: Check before processing (non-empty title, numeric ID, valid menu choice)
2. **Entity Lookup**: Verify Todo exists before update/delete/complete operations
3. **Graceful Feedback**: Display clear error message and return to main menu
4. **No Stack Traces**: Catch exceptions and translate to user-friendly messages

**Example Error Messages**:
- "Title is required. Please try again."
- "Todo with ID 5 not found."
- "Invalid choice. Please enter a number between 1 and 6."
- "Please enter a valid number."

---

### 4. Architecture: Function-Based vs. Class-Based Design

**Decision**: Class-based design with separation into Model, Service, and CLI layers

**Rationale**:
- Aligns with constitution principle III (Strong Separation of Concerns)
- Supports principle IV (Domain Model Reusability) - Todo model can be reused in Phase II
- Familiar OOP pattern for Python developers
- Easier to test individual components (mock service in CLI tests)
- Scales better when adding features (e.g., filtering, sorting in future phases)
- Models clean architecture principles for educational value

**Alternatives Considered**:
- **Purely functional**: Simpler for small apps, but harder to reuse domain logic in Phase II; mixing functions and classes is awkward
- **Single-file script**: Violates separation of concerns; makes testing difficult

**Architecture Layers**:

```
┌─────────────────────────────────────┐
│         CLI Layer (cli.py)          │  ← User interaction, menu, input/output
│  - display_menu()                   │
│  - get_user_choice()                │
│  - add_todo_flow()                  │
│  - view_todos_flow()                │
└──────────────┬──────────────────────┘
               │ calls
               ▼
┌─────────────────────────────────────┐
│     Service Layer (service.py)      │  ← Business logic, CRUD operations
│  - TodoService class                │
│    - add_todo(title, desc)          │
│    - get_all_todos()                │
│    - update_todo(id, ...)           │
│    - delete_todo(id)                │
│    - mark_complete(id)              │
└──────────────┬──────────────────────┘
               │ uses
               ▼
┌─────────────────────────────────────┐
│      Model Layer (models.py)        │  ← Domain entities (reusable Phase II+)
│  - Todo dataclass                   │
│    - id: int                        │
│    - title: str                     │
│    - description: str               │
│    - completed: bool                │
│    - created_at: datetime           │
└─────────────────────────────────────┘
```

---

### 5. Python Version and Package Manager

**Decision**: Python 3.13+ with UV package manager

**Rationale**:
- Python 3.13 provides latest performance improvements and type hinting features
- UV is modern, fast package manager (Rust-based) - aligns with "modern Python" best practices
- UV provides deterministic dependency resolution
- Supports future phases (UV works well with FastAPI in Phase II)
- User explicitly requested UV in constraints

**Alternatives Considered**:
- **Poetry**: Popular but slower than UV; more complex configuration
- **pip + requirements.txt**: Traditional but lacks lock file and fast resolution
- **Pipenv**: Falling out of favor in community; slower than UV

**Setup Commands**:
```bash
# Install UV (if not present)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Initialize project
uv init

# Add dev dependencies
uv add --dev pytest pytest-cov
```

---

### 6. Testing Framework and Strategy

**Decision**: pytest with unit tests for service layer and integration tests for CLI flows

**Rationale**:
- pytest is de facto standard for Python testing
- Rich plugin ecosystem (pytest-cov for coverage, pytest-mock for mocking)
- Simple syntax (`assert` statements vs. unittest boilerplate)
- Supports both unit and integration tests in same framework
- Aligns with constitution principle VI (Automated Testing at Each Phase)

**Test Organization**:
```
tests/
├── unit/
│   ├── test_models.py       # Todo dataclass validation
│   └── test_service.py      # TodoService CRUD operations
└── integration/
    └── test_cli.py          # Full CLI flows with mocked input
```

**Testing Approach**:
- **Unit Tests**: Test TodoService methods in isolation (add, update, delete, mark_complete, get_all)
- **Integration Tests**: Test full user flows by mocking `input()` and capturing `print()` output
- **Coverage Target**: 90%+ for service layer (core business logic)

---

### 7. ID Generation Strategy

**Decision**: Sequential integers starting from 1, using `max(todos.keys()) + 1` or `1` if empty

**Rationale**:
- Simple and predictable for users (IDs are 1, 2, 3...)
- No external dependencies (no UUID library)
- Sufficient for in-memory single-user application
- Easy to type (single/double digits for typical usage)
- Aligns with spec assumption: "Todo IDs are sequential integers starting from 1"

**Implementation**:
```python
def _generate_id(self) -> int:
    return max(self.todos.keys()) + 1 if self.todos else 1
```

**Tradeoff**: IDs are not reused after deletion (e.g., delete ID 2, next ID is 4 not 2). This is acceptable for Phase I but noted for future consideration.

---

### 8. Display Format for Todos

**Decision**: Tabular text format with visual markers for completion status

**Rationale**:
- Satisfies SC-002 (clear visual distinction between complete/incomplete)
- Readable in terminal without external libraries (no rich/tabulate dependency in Phase I)
- Simple string formatting using f-strings
- Educational value (shows basic Python formatting)

**Display Format**:
```
ID | Status | Title                  | Description
---+--------+------------------------+---------------------------
1  | [ ]    | Buy groceries          | Milk, eggs, bread
2  | [✓]    | Call dentist           | Schedule annual checkup
3  | [ ]    | Finish project report  | Due Friday
```

**Status Markers**:
- `[ ]` = Incomplete
- `[✓]` = Complete

**Alternative Considered**: JSON output - too technical for target audience; better for Phase II API

---

### 9. Module Structure and Entry Point

**Decision**: Package structure with `__main__.py` entry point

**Rationale**:
- Enables `python -m todo_app` execution pattern
- Clean module organization (src/todo_app/ package)
- Follows modern Python packaging best practices
- Supports future expansion (Phase II can import src/todo_app/models.py)

**Project Structure**:
```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── __main__.py      # Entry point (main loop)
│       ├── models.py         # Todo dataclass
│       ├── service.py        # TodoService class
│       └── cli.py            # CLI interaction functions
├── tests/
│   ├── unit/
│   └── integration/
├── pyproject.toml            # UV configuration
└── README.md
```

**Execution**:
```bash
# Development
uv run python -m todo_app

# After installation
todo-app  # (if console script configured in pyproject.toml)
```

---

### 10. Graceful Exit Handling

**Decision**: Menu option "6. Exit" plus Ctrl+C handling with cleanup message

**Rationale**:
- Satisfies edge case: "How does the app handle graceful exit"
- Provides two exit paths: intentional (menu) and interrupt (Ctrl+C)
- Educational value (shows signal handling pattern)
- Professional UX (no abrupt termination)

**Implementation**:
- Menu option 6 breaks main loop gracefully
- `try/except KeyboardInterrupt` catches Ctrl+C and displays "Exiting... Goodbye!"
- No cleanup needed (in-memory only), but pattern established for Phase II

---

## Best Practices Research

### Python Dataclasses for Todo Model

**Recommendation**: Use `@dataclass` decorator for Todo entity

**Benefits**:
- Auto-generates `__init__`, `__repr__`, `__eq__`
- Type hints built-in (supports SC-007: code understandability)
- Less boilerplate than manual class definition
- Standard library (no external dependency)
- Immutable option with `frozen=True` (not needed for Phase I but good to know)

**Example**:
```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = None

    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
```

---

### Input Validation Best Practices

**Recommendation**: Validate early, fail gracefully, provide specific error messages

**Patterns**:
1. **Non-empty strings**: `if not title.strip(): raise ValueError("Title is required")`
2. **Numeric input**: Use `try/except ValueError` around `int()` conversion
3. **Range validation**: Check menu choice in 1-6 range
4. **Existence check**: Verify ID in `todos` dict before operations

---

### Testing Best Practices for CLI Applications

**Recommendation**: Mock `input()` and capture `print()` for integration tests

**Pattern**:
```python
from unittest.mock import patch
from io import StringIO

def test_add_todo_flow():
    with patch('builtins.input', side_effect=['1', 'Buy milk', 'Whole milk', '6']):
        with patch('sys.stdout', new=StringIO()) as fake_out:
            run_app()
            output = fake_out.getvalue()
            assert "Buy milk" in output
```

---

## Unresolved Items

None. All technical decisions documented and justified.

---

## References

- Constitution: `.specify/memory/constitution.md`
- Specification: `specs/001-console-todo/spec.md`
- Python Dataclasses: https://docs.python.org/3/library/dataclasses.html
- UV Package Manager: https://docs.astral.sh/uv/
- pytest Documentation: https://docs.pytest.org/
