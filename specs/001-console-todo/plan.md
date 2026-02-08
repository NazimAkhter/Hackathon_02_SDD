# Implementation Plan: In-Memory Python Console Todo App

**Branch**: `001-console-todo` | **Date**: 2026-01-02 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-console-todo/spec.md`

## Summary

Build a Phase I in-memory Python console todo application with CRUD operations (Create, Read, Update, Delete, Mark Complete). The app uses clean architecture with separated Model, Service, and CLI layers, enabling domain model reuse in Phase II (web application). All data stored in Python dictionary (in-memory only), accessed via numbered menu interface. Target audience: beginner-intermediate Python developers learning spec-driven development and clean architecture principles.

**Technical Approach**: Class-based design using Python 3.13+ dataclasses for Todo entity, TodoService for business logic, CLI module for user interaction. Testing via pytest with 90%+ coverage target for service layer. Package manager: UV (modern Rust-based tool). Entry point: `python -m todo_app`.

---

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None for core app (stdlib only); pytest, pytest-cov, pytest-mock for testing
**Storage**: In-memory (Python dict: `Dict[int, Todo]`)
**Testing**: pytest with unit tests (models, service) and integration tests (CLI flows)
**Target Platform**: Cross-platform console (Linux, macOS, Windows)
**Project Type**: Single project (console application)
**Performance Goals**: <1 second for all operations with 100+ todos; <5 seconds to add/view todos
**Constraints**: No persistence, no external dependencies for domain logic, console-only interface
**Scale/Scope**: Single-user, session-based (data lost on exit), hundreds of todos without degradation

---

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: Incremental Phase-By-Phase Development ✅ PASS

- This is Phase I (foundation) - no prerequisites
- Fully functional in-memory console app before web/AI/cloud layers
- Domain model designed for reuse in Phase II+ (no breaking changes needed)

### Principle II: Simplicity First ✅ PASS

- Console app (simplest UI)
- In-memory storage (simpler than database)
- No web framework, no AI, no cloud infrastructure
- Standard library only (no external dependencies for core logic)

### Principle III: Strong Separation of Concerns ✅ PASS

- **Model Layer** (`models.py`): Todo entity, domain logic
- **Service Layer** (`service.py`): Business logic, CRUD operations
- **CLI Layer** (`cli.py`): User interaction, input/output
- Clear boundaries: CLI calls Service, Service uses Model
- Infrastructure independent: Todo model has no CLI/storage coupling

### Principle IV: Domain Model Reusability ✅ PASS

- Todo dataclass defined in Phase I is authoritative
- No database/framework-specific attributes in Todo model
- Phase II migration path documented: Todo becomes SQLModel without field changes
- Core attributes (id, title, description, completed, created_at) remain unchanged across phases

### Principle V: Spec-Driven Development ✅ PASS

- Specification complete: `specs/001-console-todo/spec.md`
- Plan documenting decisions: this file
- Tasks will reference spec requirements (FR-001 to FR-012, user stories P1-P3)
- Implementation blocked until plan approved

### Principle VI: Automated Testing at Each Phase ✅ PASS

- Unit tests for Todo model (validation, state transitions)
- Unit tests for TodoService (all CRUD operations)
- Integration tests for CLI flows (mocked input/output)
- Target: 90%+ coverage for service layer
- Tests MUST pass before Phase II begins

### Principle VII: Version Control and Feature Branch Workflow ✅ PASS

- Branch: `001-console-todo` (Phase I naming convention)
- Commits will reference task IDs from tasks.md
- PR will include test evidence and spec compliance verification

**Constitution Compliance**: ✅ ALL GATES PASSED

---

## Project Structure

### Documentation (this feature)

```
specs/001-console-todo/
├── spec.md                    # Feature specification (user stories, requirements)
├── plan.md                    # This file (implementation plan)
├── research.md                # Technical decisions and rationale
├── data-model.md              # Todo entity definition and validation rules
├── quickstart.md              # Setup and usage guide
├── contracts/
│   └── cli-interface.md       # CLI input/output contract
├── checklists/
│   └── requirements.md        # Spec quality validation checklist
└── tasks.md                   # (Created by /sp.tasks command - NOT by /sp.plan)
```

### Source Code (repository root)

```
todo-app/
├── src/
│   └── todo_app/
│       ├── __init__.py        # Package initialization
│       ├── __main__.py        # Entry point (main loop, menu display)
│       ├── models.py          # Todo dataclass, domain validation
│       ├── service.py         # TodoService class (CRUD operations)
│       └── cli.py             # CLI interaction functions (flows for each operation)
├── tests/
│   ├── __init__.py
│   ├── unit/
│   │   ├── test_models.py     # Todo dataclass tests (12 test cases)
│   │   └── test_service.py    # TodoService tests (15 test cases)
│   └── integration/
│       └── test_cli.py        # Full CLI flow tests (8 test cases)
├── pyproject.toml             # UV configuration, dependencies, metadata
├── README.md                  # Project overview, links to specs
└── .gitignore                 # Python/UV ignores (.venv, __pycache__, etc.)
```

**Structure Decision**: Single project structure chosen because this is a standalone console application (no frontend/backend split). All Python code under `src/todo_app/` package enables `python -m todo_app` execution and clean imports for Phase II reuse.

---

## Architecture Design

### Layer Diagram

```
┌───────────────────────────────────────────────────────────────┐
│                     User (Terminal)                           │
└────────────────────────────┬──────────────────────────────────┘
                             │
                             ▼
┌───────────────────────────────────────────────────────────────┐
│                CLI Layer (cli.py)                             │
│  - display_menu()                 Show main menu              │
│  - get_user_choice()              Get and validate menu input │
│  - add_todo_flow()                Handle add todo interaction │
│  - view_todos_flow()              Display all todos           │
│  - update_todo_flow()             Handle update interaction   │
│  - delete_todo_flow()             Handle delete with confirm  │
│  - mark_complete_flow()           Handle mark complete        │
│                                                                │
│  Responsibilities:                                             │
│  - User input/output                                           │
│  - Input validation (menu choices, numeric IDs)                │
│  - Error message display                                       │
│  - Flow orchestration                                          │
└────────────────────────────┬──────────────────────────────────┘
                             │ calls methods
                             ▼
┌───────────────────────────────────────────────────────────────┐
│              Service Layer (service.py)                       │
│                                                                │
│  class TodoService:                                            │
│    - __init__()                   Initialize empty todos dict │
│    - add_todo(title, desc)        Create and store new todo   │
│    - get_all_todos()              Return list of all todos    │
│    - get_todo_by_id(id)           Retrieve specific todo      │
│    - update_todo(id, ...)         Modify existing todo        │
│    - delete_todo(id)              Remove todo from storage    │
│    - mark_complete(id)            Update completion status    │
│    - _generate_id()               Create unique sequential ID │
│                                                                │
│  Responsibilities:                                             │
│  - Business logic                                              │
│  - CRUD operations                                             │
│  - ID generation                                               │
│  - In-memory storage management (dict operations)              │
│  - Existence validation (ID lookups)                           │
└────────────────────────────┬──────────────────────────────────┘
                             │ uses
                             ▼
┌───────────────────────────────────────────────────────────────┐
│                Model Layer (models.py)                        │
│                                                                │
│  @dataclass                                                    │
│  class Todo:                                                   │
│    - id: int                      Unique identifier           │
│    - title: str                   Task summary (required)     │
│    - description: str             Details (optional, default="")│
│    - completed: bool              Status (default=False)      │
│    - created_at: datetime         Timestamp (auto-generated)  │
│                                                                │
│    - __post_init__()              Validate title/description  │
│    - mark_complete()              Set completed=True          │
│    - is_complete()                Return completion status    │
│    - __str__()                    Format for CLI display      │
│                                                                │
│  Responsibilities:                                             │
│  - Domain entity definition                                    │
│  - Attribute validation (non-empty title, length limits)       │
│  - Domain methods (mark_complete)                              │
│  - Display formatting                                          │
└───────────────────────────────────────────────────────────────┘
```

### Entry Point Flow (__main__.py)

```python
def main():
    """Main application loop"""
    service = TodoService()

    print_welcome()

    try:
        while True:
            display_menu()
            choice = get_user_choice()

            if choice == 1:
                add_todo_flow(service)
            elif choice == 2:
                view_todos_flow(service)
            elif choice == 3:
                update_todo_flow(service)
            elif choice == 4:
                delete_todo_flow(service)
            elif choice == 5:
                mark_complete_flow(service)
            elif choice == 6:
                print_goodbye()
                break
    except KeyboardInterrupt:
        print("\n\nExiting... Goodbye!")
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Key Design Decisions

### 1. Data Structure: Dictionary with Integer Keys

**Decision**: `todos: Dict[int, Todo]`

**Rationale**:
- O(1) lookup for update/delete/mark-complete (primary operations)
- Natural ID → Todo mapping
- Simple ID generation: `max(todos.keys()) + 1`
- Supports iteration for view-all operation

**Alternative Rejected**: List with index as ID (fragile on deletion, requires re-indexing)

**Reference**: `research.md` - Decision #1

---

### 2. Menu Style: Numbered Options

**Decision**: Display menu with numbered choices (1-6), user enters single digit

**Format**:
```
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

**Rationale**:
- Lower cognitive load (select number vs. type command)
- Simpler input validation (check if 1-6)
- Familiar pattern for console apps
- Reduces typos

**Alternative Rejected**: Typed commands (e.g., "add", "delete") - higher error rate, more complex parsing

**Reference**: `research.md` - Decision #2

---

### 3. Error Handling: Defensive Validation

**Strategy**: Validate all user input, display friendly error messages, return to menu (never crash)

**Validation Points**:
- Menu choice: Must be 1-6, numeric
- Todo ID: Must be numeric, must exist in `todos` dict
- Title: Cannot be empty/whitespace-only, max 200 chars
- Description: Max 1000 chars

**Error Message Format**:
```
✗ Error: {specific problem}

[Return to main menu]
```

**Examples**:
- `✗ Error: Title cannot be empty. Please try again.`
- `✗ Error: Todo with ID 999 not found.`
- `✗ Error: Please enter a valid number.`

**Rationale**: Supports SC-006 (self-correcting error messages), educational for beginners

**Reference**: `research.md` - Decision #3, `contracts/cli-interface.md`

---

### 4. Architecture: Class-Based with Layer Separation

**Decision**: Use classes for Service layer, dataclass for Model, functions for CLI

**Rationale**:
- Aligns with Constitution Principle III (Separation of Concerns)
- TodoService encapsulates state (todos dict) and CRUD operations
- Todo dataclass is pure domain entity (reusable in Phase II)
- CLI functions orchestrate flows without business logic
- Testable: Can mock service in CLI tests, test service in isolation

**Alternative Rejected**: Purely functional (harder to reuse in Phase II OOP context)

**Reference**: `research.md` - Decision #4

---

### 5. Python Tooling: Python 3.13 + UV

**Decision**: Require Python 3.13+, use UV for package management

**Rationale**:
- Python 3.13: Latest features, improved performance, modern type hints
- UV: Fast (Rust-based), deterministic dependency resolution, industry trend
- User explicitly requested UV in constraints
- Prepares for Phase II (UV works well with FastAPI)

**Setup**:
```bash
uv init
uv add --dev pytest pytest-cov pytest-mock
uv run python -m todo_app
```

**Reference**: `research.md` - Decision #5

---

### 6. Testing Strategy: pytest with Unit + Integration

**Decision**: Use pytest for all tests, separate unit and integration

**Test Organization**:
```
tests/
├── unit/
│   ├── test_models.py     # Todo validation, methods (12 tests)
│   └── test_service.py    # CRUD operations (15 tests)
└── integration/
    └── test_cli.py        # Full flows with mocked I/O (8 tests)
```

**Coverage Target**: 90%+ for `service.py` (business logic)

**Integration Test Pattern**:
```python
with patch('builtins.input', side_effect=['1', 'Buy milk', '', '6']):
    with patch('sys.stdout', new=StringIO()) as fake_out:
        main()
        assert "Buy milk" in fake_out.getvalue()
```

**Rationale**: pytest is standard, simple syntax, rich plugins, supports both unit and integration

**Reference**: `research.md` - Decision #6

---

### 7. ID Generation: Sequential Integers

**Decision**: IDs are sequential starting from 1, using `max(todos.keys()) + 1`

**Implementation**:
```python
def _generate_id(self) -> int:
    return max(self.todos.keys()) + 1 if self.todos else 1
```

**Properties**:
- IDs: 1, 2, 3, 4, ...
- Not reused after deletion (e.g., delete ID 2, next is 5 not 2)
- Simple, predictable for users

**Tradeoff**: Gaps after deletion (acceptable for Phase I)

**Reference**: `research.md` - Decision #7

---

### 8. Display Format: Tabular with Status Icons

**Decision**: Display todos in table format with visual status markers

**Format**:
```
 ID | Status | Title                          | Description
----+--------+--------------------------------+---------------------------
  1 | [ ]    | Buy groceries                  | Milk, eggs, bread
  2 | [✓]    | Call dentist                   |
```

**Status Icons**:
- `[ ]` = Incomplete
- `[✓]` = Complete

**Column Widths**:
- ID: 3 chars (right-aligned)
- Status: 6 chars
- Title: 30 chars (truncate with "...")
- Description: 50 chars (truncate with "...")

**Rationale**: Satisfies SC-002 (clear visual distinction), readable without external libraries

**Reference**: `research.md` - Decision #8, `contracts/cli-interface.md`

---

### 9. Module Structure: Package with __main__.py

**Decision**: Structure as `src/todo_app/` package with `__main__.py` entry point

**Execution**: `uv run python -m todo_app`

**Benefits**:
- Clean module organization
- Supports `python -m` execution pattern
- Follows modern Python packaging best practices
- Enables Phase II to import `from todo_app.models import Todo`

**Reference**: `research.md` - Decision #9

---

### 10. Graceful Exit: Menu Option + Ctrl+C Handling

**Decision**: Two exit paths: menu option 6 (intentional) and Ctrl+C (interrupt)

**Menu Exit**:
```
Enter your choice (1-6): 6

Thank you for using Todo App!
All data will be lost (in-memory only).
Goodbye!
```

**Keyboard Interrupt**:
```python
try:
    main_loop()
except KeyboardInterrupt:
    print("\n\nExiting... Goodbye!")
    sys.exit(0)
```

**Rationale**: Professional UX, satisfies edge case "How does app handle graceful exit"

**Reference**: `research.md` - Decision #10

---

## Implementation Phases (for /sp.tasks)

When `/sp.tasks` is run, tasks will be organized into these phases:

### Phase 1: Project Setup
- Initialize UV project with `pyproject.toml`
- Create directory structure (`src/todo_app/`, `tests/unit/`, `tests/integration/`)
- Configure pytest and coverage tools
- Create `__init__.py` files

### Phase 2: Model Layer (Domain)
- Implement `Todo` dataclass in `models.py`
- Add validation in `__post_init__` (title non-empty, length limits)
- Implement `mark_complete()`, `is_complete()`, `__str__()` methods
- Write unit tests in `tests/unit/test_models.py` (12 test cases)

### Phase 3: Service Layer (Business Logic)
- Implement `TodoService` class in `service.py`
- Add `add_todo()`, `get_all_todos()`, `get_todo_by_id()` methods
- Add `update_todo()`, `delete_todo()`, `mark_complete()` methods
- Implement `_generate_id()` helper
- Write unit tests in `tests/unit/test_service.py` (15 test cases)

### Phase 4: CLI Layer (User Interaction)
- Implement CLI functions in `cli.py`:
  - `display_menu()`, `get_user_choice()`
  - `add_todo_flow()`, `view_todos_flow()`
  - `update_todo_flow()`, `delete_todo_flow()`, `mark_complete_flow()`
- Implement input validation and error handling
- Implement display formatting (table, status icons)

### Phase 5: Entry Point (Main Loop)
- Implement `main()` function in `__main__.py`
- Add welcome/goodbye messages
- Add main loop with menu dispatch
- Add Ctrl+C handling

### Phase 6: Integration Testing
- Write CLI flow tests in `tests/integration/test_cli.py` (8 test cases)
- Test full user journeys (add → view → mark complete → delete)
- Test error paths (invalid IDs, empty titles)

### Phase 7: Documentation & Validation
- Create `README.md` with project overview
- Verify all spec requirements met (FR-001 to FR-012, US1-US5)
- Run full test suite with coverage report
- Validate success criteria (SC-001 to SC-007)

---

## Testing Strategy

### Unit Tests (25 test cases total)

**test_models.py (12 tests)**:
1. Todo creation with defaults
2. Todo creation with all fields
3. Empty title raises ValueError
4. Whitespace-only title raises ValueError
5. Title trimming (leading/trailing whitespace)
6. Title max length (201 chars raises ValueError)
7. Description max length (1001 chars raises ValueError)
8. mark_complete() sets completed=True
9. mark_complete() is idempotent
10. is_complete() returns correct boolean
11. __str__() format for incomplete todo
12. __str__() format for complete todo

**test_service.py (15 tests)**:
1. add_todo() creates todo with generated ID
2. add_todo() increments IDs sequentially
3. add_todo() trims title whitespace
4. get_all_todos() returns empty list when no todos
5. get_all_todos() returns all todos ordered by created_at
6. get_todo_by_id() returns correct todo
7. get_todo_by_id() returns None for non-existent ID
8. update_todo() modifies title successfully
9. update_todo() modifies description successfully
10. update_todo() returns False for non-existent ID
11. delete_todo() removes todo from storage
12. delete_todo() returns False for non-existent ID
13. mark_complete() sets todo to completed
14. mark_complete() returns False for non-existent ID
15. ID generation reuses max+1 (not reuses deleted IDs)

### Integration Tests (8 test cases)

**test_cli.py (8 tests)**:
1. Full add todo flow (input title + description, verify output)
2. View all todos flow (add 3 todos, verify table display)
3. Update todo flow (add, update title, verify change)
4. Delete todo flow (add, delete with confirmation, verify removal)
5. Mark complete flow (add, mark complete, verify status change)
6. Error: Add todo with empty title (verify error message)
7. Error: Update non-existent ID (verify error message)
8. Exit flow (select option 6, verify goodbye message)

**Integration Test Pattern**:
- Mock `builtins.input` with `side_effect` list
- Mock `sys.stdout` with `StringIO` to capture output
- Run `main()` function
- Assert output contains expected strings

### Coverage Target

**Minimum Required**: 90% coverage for `src/todo_app/service.py`

**Command**:
```bash
uv run pytest --cov=src/todo_app --cov-report=term-missing
```

**Success Criteria**: All tests pass, coverage ≥ 90% for service layer

---

## Acceptance Criteria (Mapped to Spec)

### User Story 1: Add New Todo Items (P1) ✅

**Acceptance Scenarios**:
- [x] AC1.1: Add todo with title and description → creates with unique ID
- [x] AC1.2: Add todo with title only → creates with empty description
- [x] AC1.3: Add todo with empty title → displays error "Title is required"

**Implementation**: `add_todo_flow()` in CLI, `add_todo()` in Service, validation in Todo.__post_init__

---

### User Story 2: View All Todos (P1) ✅

**Acceptance Scenarios**:
- [x] AC2.1: View 3 todos → displays all with ID, title, description, status
- [x] AC2.2: View when no todos → displays "No todos found"
- [x] AC2.3: View 10 todos (5 complete, 5 incomplete) → clear visual distinction

**Implementation**: `view_todos_flow()` in CLI, `get_all_todos()` in Service, Todo.__str__() for formatting

---

### User Story 3: Mark Todo as Complete (P2) ✅

**Acceptance Scenarios**:
- [x] AC3.1: Mark incomplete todo → status changes to complete
- [x] AC3.2: Mark already complete todo → displays "already complete"
- [x] AC3.3: Mark non-existent ID → displays "Todo not found"

**Implementation**: `mark_complete_flow()` in CLI, `mark_complete()` in Service, Todo.mark_complete() method

---

### User Story 4: Update Existing Todos (P3) ✅

**Acceptance Scenarios**:
- [x] AC4.1: Update title → title changes, description unchanged
- [x] AC4.2: Update description only → description changes, title unchanged
- [x] AC4.3: Update non-existent ID → displays "Todo not found"

**Implementation**: `update_todo_flow()` in CLI, `update_todo()` in Service

---

### User Story 5: Delete Todos (P3) ✅

**Acceptance Scenarios**:
- [x] AC5.1: Delete existing todo with confirmation → todo removed
- [x] AC5.2: Delete non-existent ID → displays "Todo not found"
- [x] AC5.3: Delete ID 3 from 5 todos → only 4 remain, deleted not shown

**Implementation**: `delete_todo_flow()` in CLI with confirmation prompt, `delete_todo()` in Service

---

### Functional Requirements Coverage

| Requirement | Implementation                                  | Test Coverage |
|-------------|-------------------------------------------------|---------------|
| FR-001      | Todo.__post_init__(), add_todo()               | test_models.py, test_service.py |
| FR-002      | TodoService._generate_id()                      | test_service.py |
| FR-003      | view_todos_flow(), get_all_todos(), Todo.__str__() | test_cli.py |
| FR-004      | mark_complete_flow(), mark_complete()           | test_cli.py, test_service.py |
| FR-005      | update_todo_flow(), update_todo()               | test_cli.py, test_service.py |
| FR-006      | delete_todo_flow(), delete_todo()               | test_cli.py, test_service.py |
| FR-007      | Todo.__post_init__() title validation          | test_models.py |
| FR-008      | CLI validation in all flows                     | test_cli.py |
| FR-009      | TodoService.todos dict (in-memory)              | Architecture |
| FR-010      | display_menu(), get_user_choice()               | test_cli.py |
| FR-011      | main() loop in __main__.py                      | Architecture |
| FR-012      | Todo.completed bool, mark_complete()            | test_models.py |

---

### Success Criteria Validation

| Criterion | Validation Method                                    | Target   |
|-----------|------------------------------------------------------|----------|
| SC-001    | Integration test timing (add + view)                 | < 5 sec  |
| SC-002    | Visual inspection of output ([ ] vs [✓])             | Manual   |
| SC-003    | Integration tests for all CRUD operations            | All pass |
| SC-004    | Performance test with 100 todos                      | < 1 sec  |
| SC-005    | Integration tests with valid input                   | 90% pass |
| SC-006    | Error message clarity (manual review)                | Manual   |
| SC-007    | Code review by beginner-intermediate developer       | Manual   |

---

## Dependencies

### Runtime (Core Application)

**None.** Phase I uses only Python standard library.

Modules used:
- `dataclasses` - Todo entity
- `datetime` - Timestamps
- `typing` - Type hints
- `sys` - Exit handling

### Development (Testing & Tooling)

Managed by UV in `pyproject.toml`:

```toml
[project]
name = "todo-app"
version = "0.1.0"
requires-python = ">=3.13"

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-cov>=4.1.0",
    "pytest-mock>=3.12.0"
]
```

**Install**: `uv add --dev pytest pytest-cov pytest-mock`

---

## Risks & Mitigations

### Risk 1: IDs Become Large After Many Deletions

**Description**: Sequential ID generation means IDs grow forever (not reused after deletion)

**Impact**: After 1000 add/delete cycles, IDs could be 4-5 digits

**Mitigation**: Acceptable for Phase I (session-based, data lost on exit). Phase II will use database auto-increment (same behavior).

**Decision**: No change needed for Phase I.

---

### Risk 2: Unicode Handling in Different Terminals

**Description**: Unicode checkmark (✓) may not display correctly on all terminals

**Impact**: Status display might show incorrect character or box

**Mitigation**:
- Use basic ASCII fallback in environments without Unicode support
- Test on Windows Command Prompt, PowerShell, Unix terminals
- Document terminal requirements in quickstart.md

**Decision**: Use Unicode by default, provide ASCII fallback if needed (environment detection)

---

### Risk 3: Input Validation Edge Cases

**Description**: Unexpected user input (e.g., very long strings, special characters, null bytes)

**Impact**: Could cause crashes or unexpected behavior

**Mitigation**:
- Comprehensive input validation in CLI and Todo model
- Integration tests for edge cases
- Try/except blocks around all input operations
- Length limits enforced (200 chars title, 1000 chars description)

**Decision**: Defensive validation everywhere, extensive edge case testing

---

## Phase II Migration Notes

### Todo Model Compatibility

**Phase I (Current)**:
```python
@dataclass
class Todo:
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
```

**Phase II (SQLModel)**:
```python
from sqlmodel import SQLModel, Field

class Todo(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str = Field(max_length=200)
    description: str = Field(default="", max_length=1000)
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.now)
    user_id: int = Field(foreign_key="user.id")  # NEW
```

**Migration Path**: Core fields unchanged, new fields added (user_id). Phase I code reusable with import path change.

---

### Service Layer Reuse

**Phase I**: TodoService manages in-memory dict

**Phase II**: TodoService becomes TodoRepository, operates on database session

**Compatibility**: Method signatures remain same (`add_todo(title, desc)` → `add_todo(title, desc)`), implementation changes from dict operations to ORM queries.

---

## Next Steps

1. **Run `/sp.tasks`** to generate task breakdown from this plan
2. **Review and approve tasks** before implementation begins
3. **Run `/sp.implement`** to execute tasks via Claude Code
4. **Validate against acceptance criteria** after implementation
5. **Create pull request** with test evidence and spec compliance

---

## References

- **Specification**: `specs/001-console-todo/spec.md`
- **Research**: `specs/001-console-todo/research.md`
- **Data Model**: `specs/001-console-todo/data-model.md`
- **CLI Contract**: `specs/001-console-todo/contracts/cli-interface.md`
- **Quickstart**: `specs/001-console-todo/quickstart.md`
- **Constitution**: `.specify/memory/constitution.md`
- **Python Dataclasses**: https://docs.python.org/3/library/dataclasses.html
- **UV Package Manager**: https://docs.astral.sh/uv/
- **pytest Documentation**: https://docs.pytest.org/
