# CLI Interface Contract: In-Memory Python Console Todo App

**Feature**: 001-console-todo
**Date**: 2026-01-02
**Type**: Console Application Interface

## Purpose

Define the contract between the user and the console application. This document specifies exact input/output formats, menu structures, error messages, and interaction flows to ensure consistent implementation and testing.

---

## Application Entry Point

### Execution

```bash
# Development mode (using UV)
uv run python -m todo_app

# Installed mode (future - Phase I uses dev mode)
todo-app
```

### Initial Display

Upon launch, the application displays the main menu:

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

---

## Menu Operations Contract

### Operation 1: Add Todo

#### Input Flow

```
Enter your choice (1-6): 1

--- Add New Todo ---
Enter title: Buy groceries
Enter description (optional, press Enter to skip): Milk, eggs, bread

✓ Todo added successfully! (ID: 1)

[Return to main menu]
```

#### Input Validation

**Title Validation**:
- **Empty title**:
  ```
  Enter title:
  ✗ Error: Title cannot be empty. Please try again.
  Enter title: Buy groceries
  ```

- **Whitespace-only title**:
  ```
  Enter title:
  ✗ Error: Title cannot be empty. Please try again.
  Enter title: Valid Title
  ```

- **Title too long (>200 characters)**:
  ```
  Enter title: [201+ characters]
  ✗ Error: Title cannot exceed 200 characters. Please try again.
  Enter title: Shorter title
  ```

**Description Validation**:
- Optional field (pressing Enter with no input = empty string, valid)
- **Description too long (>1000 characters)**:
  ```
  Enter description (optional): [1001+ characters]
  ✗ Error: Description cannot exceed 1000 characters. Please try again.
  Enter description (optional): Shorter description
  ```

#### Success Output

```
✓ Todo added successfully! (ID: {generated_id})
```

#### Behavior

- ID is auto-generated (sequential: 1, 2, 3, ...)
- Title is trimmed of leading/trailing whitespace before saving
- Description defaults to empty string if user presses Enter
- New todo defaults to incomplete status (`completed=False`)
- Returns to main menu after completion

---

### Operation 2: View All Todos

#### Input

```
Enter your choice (1-6): 2
```

#### Output - With Todos

```
--- All Todos ---

 ID | Status | Title                          | Description
----+--------+--------------------------------+---------------------------
  1 | [ ]    | Buy groceries                  | Milk, eggs, bread
  2 | [✓]    | Call dentist                   |
  3 | [ ]    | Finish project report          | Q4 analysis due Friday

Total: 3 todos (1 completed, 2 incomplete)

[Return to main menu]
```

**Format Specification**:
- Header row with column names
- Separator row (`----+--------+...`)
- Each todo on one line
- Status: `[ ]` = incomplete, `[✓]` = complete
- ID right-aligned in 3-character field
- Title left-aligned, max 30 characters displayed (truncate with "..." if longer)
- Description left-aligned, max 50 characters displayed (truncate with "..." if longer)
- Summary line with counts

#### Output - No Todos

```
--- All Todos ---

No todos found. Add your first todo to get started!

[Return to main menu]
```

#### Behavior

- Displays all todos (no filtering in Phase I)
- Todos ordered by creation time (oldest first)
- Returns to main menu after display

---

### Operation 3: Update Todo

#### Input Flow - Successful Update

```
Enter your choice (1-6): 3

--- Update Todo ---
Enter todo ID: 1

Current Todo:
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete

Enter new title (press Enter to keep current): Buy groceries and cook dinner
Enter new description (press Enter to keep current):

✓ Todo updated successfully!

[Return to main menu]
```

#### Input Flow - Update Only Description

```
Enter todo ID: 1

Current Todo:
  ID: 1
  Title: Buy groceries
  Description: Milk, eggs, bread
  Status: Incomplete

Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current): Milk, eggs, bread, chicken

✓ Todo updated successfully!
```

#### Error Handling

**Non-existent ID**:
```
Enter todo ID: 999

✗ Error: Todo with ID 999 not found.

[Return to main menu]
```

**Invalid ID (non-numeric)**:
```
Enter todo ID: abc

✗ Error: Please enter a valid number.

[Return to main menu]
```

**Empty title when trying to update**:
```
Enter new title (press Enter to keep current):

[Title validation - same as Add Todo]
✗ Error: Title cannot be empty. Please enter a title or press Enter to keep current.
```

#### Behavior

- User can press Enter to keep current value (no change)
- Both title and description can be updated in one operation
- If both are kept (two Enters), no change occurs but success message shown
- Same validation rules as Add Todo apply to new title/description
- Returns to main menu after completion

---

### Operation 4: Delete Todo

#### Input Flow - Successful Deletion

```
Enter your choice (1-6): 4

--- Delete Todo ---
Enter todo ID: 2

Are you sure you want to delete this todo?
  Title: Call dentist
  Description:

Confirm deletion (y/n): y

✓ Todo deleted successfully!

[Return to main menu]
```

#### Input Flow - Cancelled Deletion

```
Enter todo ID: 2

Are you sure you want to delete this todo?
  Title: Call dentist
  Description:

Confirm deletion (y/n): n

Deletion cancelled.

[Return to main menu]
```

#### Error Handling

**Non-existent ID**:
```
Enter todo ID: 999

✗ Error: Todo with ID 999 not found.

[Return to main menu]
```

**Invalid ID (non-numeric)**:
```
Enter todo ID: abc

✗ Error: Please enter a valid number.

[Return to main menu]
```

**Invalid confirmation input**:
```
Confirm deletion (y/n): maybe

✗ Error: Please enter 'y' for yes or 'n' for no.
Confirm deletion (y/n): y

✓ Todo deleted successfully!
```

#### Behavior

- Displays todo details before confirmation
- Requires explicit 'y' to proceed (case-insensitive: 'y' or 'Y')
- 'n' or any other input cancels deletion
- ID is not reused after deletion
- Returns to main menu after completion

---

### Operation 5: Mark Todo as Complete

#### Input Flow - Successful Mark Complete

```
Enter your choice (1-6): 5

--- Mark Todo as Complete ---
Enter todo ID: 1

Todo marked as complete!
  Title: Buy groceries
  Description: Milk, eggs, bread

[Return to main menu]
```

#### Error Handling

**Non-existent ID**:
```
Enter todo ID: 999

✗ Error: Todo with ID 999 not found.

[Return to main menu]
```

**Invalid ID (non-numeric)**:
```
Enter todo ID: abc

✗ Error: Please enter a valid number.

[Return to main menu]
```

**Already Complete**:
```
Enter todo ID: 2

ℹ Info: This todo is already marked as complete.
  Title: Call dentist

[Return to main menu]
```

#### Behavior

- Changes `completed` status from `False` to `True`
- If already complete, displays info message (not error)
- Idempotent operation (calling twice is safe)
- Returns to main menu after completion

---

### Operation 6: Exit

#### Input Flow

```
Enter your choice (1-6): 6

Thank you for using Todo App!
All data will be lost (in-memory only).
Goodbye!

[Application terminates]
```

#### Behavior

- Cleanly exits the application loop
- Displays farewell message
- Reminds user that data is not persisted
- Returns exit code 0

---

## Error Handling Contract

### Invalid Menu Choice

```
Enter your choice (1-6): 7

✗ Error: Invalid choice. Please enter a number between 1 and 6.

[Re-display menu]
```

```
Enter your choice (1-6): abc

✗ Error: Please enter a valid number.

[Re-display menu]
```

### Keyboard Interrupt (Ctrl+C)

```
Enter your choice (1-6): ^C

Exiting... Goodbye!

[Application terminates with exit code 0]
```

**Implementation**:
```python
try:
    main_loop()
except KeyboardInterrupt:
    print("\n\nExiting... Goodbye!")
    sys.exit(0)
```

---

## Display Conventions

### Status Icons

- `[ ]` - Incomplete todo
- `[✓]` - Complete todo
- `✓` - Success message prefix
- `✗` - Error message prefix
- `ℹ` - Info message prefix

### Text Formatting

- **Sections**: Surrounded by `---` (e.g., `--- Add New Todo ---`)
- **Menus**: Surrounded by `===` (e.g., `========== Todo App Menu ==========`)
- **Prompts**: End with colon and space (e.g., `Enter title: `)
- **Blank lines**: One blank line between sections for readability

### Column Widths (View All Todos)

| Column       | Width | Alignment | Truncation |
|--------------|-------|-----------|------------|
| ID           | 3     | Right     | N/A        |
| Status       | 6     | Left      | N/A        |
| Title        | 30    | Left      | "..."      |
| Description  | 50    | Left      | "..."      |

---

## Input Constraints Summary

| Input Type       | Validation Rule                          | Error Message                                  |
|------------------|------------------------------------------|------------------------------------------------|
| Menu choice      | Integer 1-6                              | "Invalid choice. Please enter 1-6."            |
| Menu choice      | Numeric input                            | "Please enter a valid number."                 |
| Todo ID          | Positive integer                         | "Please enter a valid number."                 |
| Todo ID          | Exists in todos dict                     | "Todo with ID {id} not found."                 |
| Title            | Non-empty after trim                     | "Title cannot be empty."                       |
| Title            | <= 200 characters                        | "Title cannot exceed 200 characters."          |
| Description      | <= 1000 characters                       | "Description cannot exceed 1000 characters."   |
| Delete confirm   | 'y' or 'n' (case-insensitive)            | "Please enter 'y' for yes or 'n' for no."      |

---

## Success Messages Summary

| Operation          | Message                                    |
|--------------------|--------------------------------------------|
| Add todo           | `✓ Todo added successfully! (ID: {id})`    |
| Update todo        | `✓ Todo updated successfully!`             |
| Delete todo        | `✓ Todo deleted successfully!`             |
| Mark complete      | `Todo marked as complete!`                 |
| Delete cancelled   | `Deletion cancelled.`                      |
| Already complete   | `ℹ Info: This todo is already marked as complete.` |

---

## Testing Interface

### Integration Test Mocking

**Pattern for mocking user input**:
```python
from unittest.mock import patch

# Simulate adding a todo
with patch('builtins.input', side_effect=['1', 'Buy milk', 'Whole milk', '6']):
    main()
```

**Pattern for capturing output**:
```python
from io import StringIO
import sys

with patch('sys.stdout', new=StringIO()) as fake_out:
    main()
    output = fake_out.getvalue()
    assert "Buy milk" in output
```

### Unit Test Contracts

TodoService methods should accept/return these types:

```python
class TodoService:
    def add_todo(self, title: str, description: str = "") -> Todo:
        """Returns newly created Todo object"""

    def get_all_todos(self) -> list[Todo]:
        """Returns list of all todos, ordered by created_at"""

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """Returns Todo if exists, None otherwise"""

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None) -> bool:
        """Returns True if updated, False if not found"""

    def delete_todo(self, todo_id: int) -> bool:
        """Returns True if deleted, False if not found"""

    def mark_complete(self, todo_id: int) -> bool:
        """Returns True if marked, False if not found or already complete"""
```

---

## Phase Compatibility

### Phase I (Current)

This contract defines the console interface for Phase I.

### Phase II (Web Application)

- Console interface remains available as CLI tool
- Web UI follows different contract (HTTP endpoints)
- Core operations map 1:1 to API endpoints:
  - Add Todo → `POST /api/todos`
  - View All → `GET /api/todos`
  - Update → `PUT /api/todos/{id}`
  - Delete → `DELETE /api/todos/{id}`
  - Mark Complete → `PATCH /api/todos/{id}/complete`

### Phase III+ (AI Chatbot, Kubernetes, Cloud)

- Console interface unchanged
- Additional interfaces added (chat, API, webhooks)
- All interfaces operate on same Todo domain model

---

## References

- Specification: `specs/001-console-todo/spec.md` (User Stories 1-5, FR-001 to FR-012)
- Data Model: `specs/001-console-todo/data-model.md` (Todo entity definition)
- Research: `specs/001-console-todo/research.md` (Decision #2: Menu Style, #3: Error Handling, #8: Display Format)
