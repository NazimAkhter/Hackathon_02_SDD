# Data Model: Advanced Scheduling Features for In-Memory Python Console Todo App

**Feature**: 004-advanced-scheduling
**Date**: 2026-02-08
**Phase**: 1 (Design)

## Purpose

Define the enhanced data model for the Todo domain entity, adding due dates and recurring task capabilities. This model extends the Phase I.5 authoritative model (`003-intermediate-todo-features/data-model.md`) while maintaining backward compatibility per Constitution Principle IV (Domain Model Reusability).

---

## Entity: Recurrence (NEW)

### Description

Represents the recurrence pattern for a todo item. Defines how frequently a task should repeat after completion.

### Definition

```python
from enum import Enum

class Recurrence(Enum):
    """Recurrence types for todos."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
```

### Properties

| Property | Value | Description |
|----------|-------|-------------|
| `NONE` | `"none"` | One-time task (default) |
| `DAILY` | `"daily"` | Repeats every day |
| `WEEKLY` | `"weekly"` | Repeats every 7 days |
| `MONTHLY` | `"monthly"` | Repeats monthly on the same day |

### Usage

- Default value for new todos: `Recurrence.NONE`
- Display: `recurrence.value` → `"none"`, `"daily"`, `"weekly"`, `"monthly"`
- CLI input: User enters "daily", "weekly", "monthly", or skips (defaults to "none")
- Next due date calculation: Each recurrence type has a specific algorithm

---

## Entity: Todo (ENHANCED)

### Description

Extends the Phase I.5 Todo entity with scheduling capabilities: `due_date`, `recurrence`, and `is_recurring_parent`. All existing attributes and behavior remain unchanged.

### Attributes

| Attribute    | Type        | Required | Default             | Change from Phase I.5 | Description |
|--------------|-------------|----------|---------------------|----------------------|-------------|
| `id`         | `int`       | Yes      | Auto-generated      | Unchanged | Unique identifier |
| `title`      | `str`       | Yes      | (none)              | Unchanged | Task summary (1-200 chars) |
| `description`| `str`       | No       | `""`                | Unchanged | Additional details (0-1000 chars) |
| `completed`  | `bool`      | No       | `False`             | Unchanged | Completion status |
| `created_at` | `datetime`  | No       | Current time        | Unchanged | Creation timestamp |
| `priority`   | `Priority`  | No       | `Priority.MEDIUM`   | Unchanged | Urgency level (HIGH/MEDIUM/LOW) |
| `tags`       | `list[str]` | No       | `[]`                | Unchanged | Category labels |
| `due_date`   | `datetime`  | No       | `None`              | **NEW** | Due date and time (optional) |
| `recurrence` | `Recurrence`| No       | `Recurrence.NONE`   | **NEW** | Recurrence pattern |
| `is_recurring_parent` | `bool` | No | `True`          | **NEW** | Tracks active recurring instance |

### Validation Rules

All Phase I.5 validations remain in effect. New validations:

1. **Due Date Validation** (FR-002, FR-003):
   - `due_date` MUST be a datetime object or None
   - Optional field - todos can exist without due dates
   - If provided at CLI, must be parsed from "YYYY-MM-DD HH:MM" format
   - No past-date restriction - past dates are valid (may be intentional for tracking overdue items)

2. **Recurrence Validation** (FR-012, FR-013, FR-021):
   - `recurrence` MUST be a valid `Recurrence` enum member
   - Defaults to `Recurrence.NONE`
   - If `recurrence != NONE`, then `due_date` MUST NOT be None (validation at service layer)
   - Invalid recurrence types rejected at CLI before reaching model

3. **is_recurring_parent Flag**:
   - Boolean flag to prevent duplicate rescheduling
   - Set to `True` for new todos and next recurring instances
   - Set to `False` when a recurring todo is completed (to prevent re-rescheduling if completed again)

### Python Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Priority levels for todo items."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class Recurrence(Enum):
    """Recurrence types for todo items."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"


@dataclass
class Todo:
    """
    Represents a task item in the todo application.

    Attributes:
        id: Unique identifier (auto-generated)
        title: Task summary (required, non-empty)
        description: Additional task details (optional)
        completed: Completion status (default: False)
        created_at: Creation timestamp (auto-generated)
        priority: Urgency level (default: MEDIUM)
        tags: Category labels (default: empty list)
        due_date: Due date and time (optional)
        recurrence: Recurrence pattern (default: NONE)
        is_recurring_parent: Active recurring instance flag (default: True)
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    is_recurring_parent: bool = True

    def __post_init__(self):
        """Validate todo attributes after initialization."""
        # Title validation (unchanged from Phase I.5)
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        self.title = self.title.strip()
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        if len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Priority validation (unchanged from Phase I.5)
        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be a Priority enum member, got {type(self.priority)}")

        # Tags normalization (unchanged from Phase I.5)
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list")
        seen = set()
        normalized = []
        for tag in self.tags:
            if not isinstance(tag, str):
                raise ValueError("Each tag must be a string")
            clean = tag.strip().lower()
            if clean and clean not in seen:
                seen.add(clean)
                normalized.append(clean)
        self.tags = normalized

        # Due date validation (NEW)
        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise ValueError("due_date must be a datetime object or None")

        # Recurrence validation (NEW)
        if not isinstance(self.recurrence, Recurrence):
            raise ValueError(f"Recurrence must be a Recurrence enum member, got {type(self.recurrence)}")

    def mark_complete(self) -> None:
        """Mark this todo as complete."""
        self.completed = True

    def is_complete(self) -> bool:
        """Check if todo is complete."""
        return self.completed

    def is_overdue(self) -> bool:
        """Check if this todo is overdue (past due date and not complete)."""
        if self.due_date is None or self.completed:
            return False
        return datetime.now() > self.due_date

    def is_due_soon(self) -> bool:
        """Check if this todo is due within the next 7 days (and not complete)."""
        if self.due_date is None or self.completed:
            return False
        now = datetime.now()
        days_until_due = (self.due_date - now).days
        return 0 <= days_until_due <= 7

    def __str__(self) -> str:
        """Human-readable representation for CLI display."""
        status = "[✓]" if self.completed else "[ ]"
        priority_display = self.priority.name
        title_display = self.title[:21] + "..." if len(self.title) > 24 else self.title
        tags_display = ", ".join(self.tags) if self.tags else ""
        if len(tags_display) > 20:
            tags_display = tags_display[:17] + "..."

        # Due date display with status indicator
        if self.due_date:
            due_display = self.due_date.strftime("%Y-%m-%d %H:%M")
            if not self.completed:
                if self.is_overdue():
                    due_display = f"⚠ {due_display}"
                elif self.is_due_soon():
                    due_display = f"📅 {due_display}"
        else:
            due_display = "(no due date)"

        # Recurrence display
        recurrence_display = ""
        if self.recurrence != Recurrence.NONE:
            recurrence_display = f"🔁 {self.recurrence.value}"

        return (
            f"{self.id:3d} | {status:6s} | {priority_display:8s} | "
            f"{title_display:24s} | {tags_display:20s} | {due_display:22s} | "
            f"{recurrence_display:12s}"
        )
```

### State Transitions

Completion state (unchanged from Phase I.5):

```
┌─────────────┐                              ┌─────────────┐
│ Incomplete  │ ──── mark_complete() ───────>│  Complete   │
│ (False)     │                              │  (True)     │
└─────────────┘                              └─────────────┘
     ^
     │
     └────────────── new Todo() ──────────────
                   (default state)
```

Recurring state transitions (NEW):

```
┌──────────────────────┐
│ Recurring Parent     │ mark_complete() + recurrence != NONE
│ is_recurring_parent  │ ───────────────────────────────────────┐
│ = True               │                                         │
└──────────────────────┘                                         │
         │                                                       │
         │ mark_complete()                                      │
         │                                                       ▼
         ▼                                         ┌──────────────────────────┐
┌──────────────────────┐                          │ New Recurring Instance   │
│ Completed Instance   │                          │ is_recurring_parent=True │
│ is_recurring_parent  │<─────────────────────────│ due_date = calculated    │
│ = False              │       Created            │ recurrence = same        │
└──────────────────────┘                          └──────────────────────────┘
```

Overdue status (calculated dynamically):

```
due_date < now() AND not completed → OVERDUE (⚠ indicator)
due_date within 7 days AND not completed → DUE SOON (📅 indicator)
```

---

## Service Layer Methods (NEW/ENHANCED)

### Recurrence Rescheduling

```python
def _calculate_next_due_date(self, current_due: datetime, recurrence: Recurrence) -> datetime:
    """
    Calculate next due date based on recurrence type.

    Args:
        current_due: Current due date
        recurrence: Recurrence pattern

    Returns:
        Next due date

    Raises:
        ValueError: If recurrence is NONE or current_due is None
    """
    from datetime import timedelta
    import calendar

    if recurrence == Recurrence.DAILY:
        return current_due + timedelta(days=1)

    elif recurrence == Recurrence.WEEKLY:
        return current_due + timedelta(weeks=1)

    elif recurrence == Recurrence.MONTHLY:
        # Add one month, handle non-existent dates
        year = current_due.year
        month = current_due.month + 1
        if month > 12:
            month = 1
            year += 1

        target_day = current_due.day
        max_day = calendar.monthrange(year, month)[1]

        # If target day doesn't exist in next month, use last day
        day = min(target_day, max_day)

        return current_due.replace(year=year, month=month, day=day)

    else:
        return current_due
```

### Overdue and Upcoming Filters

```python
def get_overdue_todos(self) -> List[Todo]:
    """Return all overdue todos (past due date, not complete)."""
    now = datetime.now()
    return sorted(
        [t for t in self.todos.values() if t.due_date and t.due_date < now and not t.completed],
        key=lambda t: t.due_date  # Earliest (most overdue) first
    )

def get_upcoming_todos(self) -> List[Todo]:
    """Return all todos due within the next 7 days (not complete)."""
    now = datetime.now()
    seven_days = now + timedelta(days=7)
    return sorted(
        [t for t in self.todos.values()
         if t.due_date and now <= t.due_date <= seven_days and not t.completed],
        key=lambda t: t.due_date  # Earliest first
    )
```

---

## Storage Structure

### In-Memory Representation

Enhanced structure with new fields:

```python
# Type: Dict[int, Todo]
todos = {
    1: Todo(
        id=1,
        title="Buy groceries",
        description="Milk, eggs, bread",
        completed=False,
        created_at=datetime(2026, 2, 8, 10, 0),
        priority=Priority.HIGH,
        tags=["home", "errands"],
        due_date=datetime(2026, 2, 10, 18, 0),  # NEW: Feb 10, 6 PM
        recurrence=Recurrence.NONE,             # NEW: One-time task
        is_recurring_parent=True                # NEW: Active instance
    ),
    2: Todo(
        id=2,
        title="Daily standup",
        description="",
        completed=False,
        created_at=datetime(2026, 2, 8, 10, 5),
        priority=Priority.MEDIUM,
        tags=["work"],
        due_date=datetime(2026, 2, 9, 9, 0),    # NEW: Tomorrow 9 AM
        recurrence=Recurrence.DAILY,            # NEW: Daily recurring
        is_recurring_parent=True                # NEW: Active instance
    ),
    3: Todo(
        id=3,
        title="Pay rent",
        description="Landlord expects payment by 5th",
        completed=False,
        created_at=datetime(2026, 2, 8, 10, 10),
        priority=Priority.HIGH,
        tags=["bills"],
        due_date=datetime(2026, 3, 5, 12, 0),   # NEW: March 5, noon
        recurrence=Recurrence.MONTHLY,          # NEW: Monthly recurring
        is_recurring_parent=True                # NEW: Active instance
    ),
}
```

### ID Generation

Unchanged from Phase I.5: sequential integers, never reused after deletion.

---

## Backward Compatibility

### Phase I.5 Model → Phase II (This Feature)

**Changes**:
- Added `due_date: Optional[datetime] = None`
- Added `recurrence: Recurrence = Recurrence.NONE`
- Added `is_recurring_parent: bool = True`
- All three have defaults → existing code creating `Todo(id=..., title=...)` continues to work
- `__str__()` format updated (wider table for due date and recurrence columns)
- Added `is_overdue()` and `is_due_soon()` methods (non-breaking - new functionality)

**Impact on existing tests**:
- `test_models.py`: Existing tests pass unchanged (new fields have defaults)
- `test_service.py`: Existing tests pass unchanged (service methods maintain existing signatures)
- `test_cli.py`: View output format changes (table wider) — tests need updating for new columns
- `test_main.py`: Menu option numbers shift — tests need updating

### Phase III Forward Compatibility

- `due_date` maps to a database TIMESTAMP column
- `recurrence` maps to a database ENUM or VARCHAR column
- `is_recurring_parent` maps to a database BOOLEAN column
- Core fields unchanged

---

## Data Constraints Summary

| Constraint               | Rule                                    | Enforcement                  |
|--------------------------|-----------------------------------------|------------------------------|
| ID uniqueness            | Each ID appears exactly once            | TodoService (generator)      |
| ID positivity            | ID >= 1                                 | TodoService (starts at 1)    |
| Title non-empty          | `title.strip()` not empty               | Todo.__post_init__           |
| Title length             | <= 200 characters                       | Todo.__post_init__           |
| Description length       | <= 1000 characters                      | Todo.__post_init__           |
| Due date type            | Must be datetime or None                | Todo.__post_init__           |
| Due date optionality     | Optional for all todos                  | Default = None               |
| Recurrence type          | Must be Recurrence enum member          | Todo.__post_init__           |
| Recurrence default       | `Recurrence.NONE` when not specified    | Dataclass default            |
| Recurring requires due date | If recurrence != NONE, due_date != None | TodoService validation       |
| is_recurring_parent type | Must be boolean                         | Python type system           |
| Overdue calculation      | due_date < now() and not completed      | Todo.is_overdue() method     |
| Due soon calculation     | 0 <= days_until_due <= 7 and not completed | Todo.is_due_soon() method |

---

## References

- Phase I.5 Data Model: `specs/003-intermediate-todo-features/data-model.md`
- Feature Spec: `specs/004-advanced-scheduling/spec.md`
- Research: `specs/004-advanced-scheduling/research.md` (Decisions #1-#9)
- Constitution: `.specify/memory/constitution.md` (Principle IV: Domain Model Reusability)
