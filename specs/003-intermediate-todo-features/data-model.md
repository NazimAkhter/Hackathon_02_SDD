# Data Model: Intermediate Features for In-Memory Python Console Todo App

**Feature**: 003-intermediate-todo-features
**Date**: 2026-02-08
**Phase**: 1 (Design)

## Purpose

Define the enhanced data model for the Todo domain entity, adding priority levels and tags/categories. This model extends the Phase I authoritative model (`001-console-todo/data-model.md`) while maintaining backward compatibility per Constitution Principle IV (Domain Model Reusability).

---

## Entity: Priority (NEW)

### Description

Represents the urgency level of a todo item. Three fixed levels provide a simple but effective way to rank tasks.

### Definition

```python
from enum import Enum

class Priority(Enum):
    """Priority levels for todo items, ordered by urgency."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3
```

### Properties

| Property | Value | Description |
|----------|-------|-------------|
| `HIGH` | `1` | Most urgent tasks |
| `MEDIUM` | `2` | Default priority for new todos |
| `LOW` | `3` | Least urgent tasks |

### Usage

- Integer values enable natural sorting: `sorted(todos, key=lambda t: t.priority.value)` → HIGH first
- Display: `priority.name` → `"HIGH"`, `"MEDIUM"`, `"LOW"`
- Comparison: `Priority.HIGH.value < Priority.MEDIUM.value` → `True`
- Default: `Priority.MEDIUM` when user skips priority prompt

---

## Entity: Todo (ENHANCED)

### Description

Extends the Phase I Todo entity with two new attributes: `priority` and `tags`. All existing attributes and behavior remain unchanged.

### Attributes

| Attribute    | Type        | Required | Default             | Change from Phase I | Description |
|--------------|-------------|----------|---------------------|---------------------|-------------|
| `id`         | `int`       | Yes      | Auto-generated      | Unchanged | Unique identifier |
| `title`      | `str`       | Yes      | (none)              | Unchanged | Task summary (1-200 chars) |
| `description`| `str`       | No       | `""`                | Unchanged | Additional details (0-1000 chars) |
| `completed`  | `bool`      | No       | `False`             | Unchanged | Completion status |
| `created_at` | `datetime`  | No       | Current time        | Unchanged | Creation timestamp |
| `priority`   | `Priority`  | No       | `Priority.MEDIUM`   | **NEW** | Urgency level (HIGH/MEDIUM/LOW) |
| `tags`       | `list[str]` | No       | `[]`                | **NEW** | Zero or more category labels |

### Validation Rules

All Phase I validations remain in effect. New validations:

1. **Priority Validation** (FR-001, FR-002):
   - `priority` MUST be a valid `Priority` enum member
   - Defaults to `Priority.MEDIUM` when not provided
   - Invalid values at CLI are caught before reaching the model

2. **Tags Validation** (FR-005, FR-006):
   - `tags` MUST be a list of strings
   - Each tag MUST be normalized: lowercase, whitespace-trimmed
   - Empty strings MUST be removed from the list
   - Duplicate tags MUST be removed (preserving first occurrence order)
   - Default: empty list `[]`

### Python Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class Priority(Enum):
    """Priority levels for todo items."""
    HIGH = 1
    MEDIUM = 2
    LOW = 3


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
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    priority: Priority = Priority.MEDIUM
    tags: list[str] = field(default_factory=list)

    def __post_init__(self):
        """Validate todo attributes after initialization."""
        # Title validation (unchanged from Phase I)
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")
        self.title = self.title.strip()
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        if len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Priority validation (NEW)
        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be a Priority enum member, got {type(self.priority)}")

        # Tags normalization (NEW)
        if not isinstance(self.tags, list):
            raise ValueError("Tags must be a list")
        # Normalize: lowercase, trim, remove empty, deduplicate
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

    def mark_complete(self) -> None:
        """Mark this todo as complete."""
        self.completed = True

    def is_complete(self) -> bool:
        """Check if todo is complete."""
        return self.completed

    def __str__(self) -> str:
        """Human-readable representation for CLI display."""
        status = "[✓]" if self.completed else "[ ]"
        priority_display = self.priority.name
        title_display = self.title[:21] + "..." if len(self.title) > 24 else self.title
        tags_display = ", ".join(self.tags) if self.tags else ""
        if len(tags_display) > 20:
            tags_display = tags_display[:17] + "..."
        desc_display = self.description[:27] + "..." if len(self.description) > 30 else self.description
        return (
            f"{self.id:3d} | {status:6s} | {priority_display:8s} | "
            f"{title_display:24s} | {tags_display:20s} | {desc_display}"
        )
```

### State Transitions

Unchanged from Phase I:

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

Priority and tags can be modified at any time (no state transition constraints).

---

## Storage Structure

### In-Memory Representation

Unchanged structure, enhanced content:

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
        tags=["home", "errands"]
    ),
    2: Todo(
        id=2,
        title="Call dentist",
        description="",
        completed=True,
        created_at=datetime(2026, 2, 8, 10, 5),
        priority=Priority.MEDIUM,
        tags=["health"]
    ),
    3: Todo(
        id=3,
        title="Finish report",
        description="Q4 analysis",
        completed=False,
        created_at=datetime(2026, 2, 8, 10, 10),
        priority=Priority.LOW,
        tags=["work", "reports"]
    ),
}
```

### ID Generation

Unchanged from Phase I: sequential integers, never reused after deletion.

---

## Tag Normalization Examples

| Raw Input | Normalized Output |
|-----------|-------------------|
| `"Work, HOME, errands"` | `["work", "home", "errands"]` |
| `" Work , HOME "` | `["work", "home"]` |
| `""` (empty) | `[]` |
| `"work, work, WORK"` | `["work"]` (deduped) |
| `"a,  , b,,"` | `["a", "b"]` (empty removed) |

---

## Backward Compatibility

### Phase I Model → Phase I.5 Model (This Feature)

**Changes**:
- Added `priority: Priority = Priority.MEDIUM`
- Added `tags: list[str] = field(default_factory=list)`
- Both have defaults → existing code creating `Todo(id=..., title=...)` continues to work
- `__str__()` format updated (wider table) — this is an expected change for enhanced display

**Impact on existing tests**:
- `test_models.py`: Existing tests pass unchanged (new fields have defaults)
- `test_service.py`: Existing tests pass unchanged (service methods still accept same args)
- `test_cli.py`: View output format changes (table wider) — tests need updating for new columns
- `test_main.py`: Menu option numbers shift (Exit now 9) — tests need updating

### Phase II Forward Compatibility

- `priority` maps to a database enum/string column
- `tags` maps to a JSON array column or a separate tags table
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
| Completion boolean       | `completed` is `True` or `False`        | Python type system           |
| Timestamp immutability   | `created_at` set once, never modified   | No setter provided           |
| Priority enum            | Must be `Priority.HIGH/MEDIUM/LOW`      | Todo.__post_init__           |
| Priority default         | `Priority.MEDIUM` when not specified    | Dataclass default            |
| Tags type                | Must be `list[str]`                     | Todo.__post_init__           |
| Tags normalization       | Lowercase, trimmed, no empties, no dupes| Todo.__post_init__           |

---

## References

- Phase I Data Model: `specs/001-console-todo/data-model.md`
- Feature Spec: `specs/003-intermediate-todo-features/spec.md`
- Research: `specs/003-intermediate-todo-features/research.md` (Decisions #1, #2, #10)
- Constitution: `.specify/memory/constitution.md` (Principle IV: Domain Model Reusability)
