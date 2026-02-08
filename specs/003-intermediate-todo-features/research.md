# Research: Intermediate Features for In-Memory Python Console Todo App

**Feature**: 003-intermediate-todo-features
**Date**: 2026-02-08
**Phase**: 0 (Outline & Research)

## Purpose

Resolve all technical unknowns and architectural decisions before designing the data model, contracts, and implementation plan. Each decision documents what was chosen, why, and what alternatives were considered.

---

## Decision 1: Priority Representation — Enum vs. String

**Decision**: Use Python `enum.Enum` for priority levels.

**Rationale**:
- Enum constrains valid values at the type level (`Priority.HIGH`, `Priority.MEDIUM`, `Priority.LOW`)
- Prevents typos and invalid values (e.g., "hig", "urgent") — invalid values raise an error at construction
- Provides natural ordering for sorting: assign integer values (`HIGH=1`, `MEDIUM=2`, `LOW=3`) so `sorted()` works directly on `.value`
- Clean integration with dataclass: `priority: Priority = Priority.MEDIUM`
- String comparison for display: `priority.name.lower()` → "high", "medium", "low"

**Alternatives Considered**:
- **Plain string** ("high", "medium", "low"): No type safety, requires manual validation everywhere, easy to introduce typos, sorting requires a mapping dict. Rejected.
- **Integer (1, 2, 3)**: Compact but obscure — users must remember what each number means. Rejected for user-facing domain model.

**Implementation Sketch**:
```python
from enum import Enum

class Priority(Enum):
    HIGH = 1
    MEDIUM = 2
    LOW = 3
```

---

## Decision 2: Tag/Category Structure — Single vs. Multiple Tags

**Decision**: Support multiple tags per todo, stored as a `list[str]`.

**Rationale**:
- Spec requirement FR-005: "zero or more tags/categories"
- Users describe real-world tasks with multiple contexts (e.g., a task can be both "work" and "meeting")
- `list[str]` is the simplest Python structure for ordered, mutable collections of strings
- Tags entered as comma-separated string at CLI, parsed and normalized (lowercase, trimmed) before storage
- Supports efficient filtering: `if tag in todo.tags`

**Alternatives Considered**:
- **Single category string**: Too restrictive — spec explicitly says "one or more tags". Rejected.
- **Set[str]**: No duplicates and unordered — slightly better semantics but less predictable display order, and `set` isn't directly JSON-serializable for future phases. Rejected in favor of list with dedup at input time.
- **Predefined category enum**: Too rigid — spec says "free-form text labels". Rejected.

**Tag Normalization Rules**:
1. Split input on comma: `"Work, HOME, errands"` → `["Work", " HOME", " errands"]`
2. Strip whitespace: `["Work", "HOME", "errands"]`
3. Convert to lowercase: `["work", "home", "errands"]`
4. Remove empty strings (from trailing commas)
5. Remove duplicates while preserving order

---

## Decision 3: Search Scope — Title Only vs. Full Task Fields

**Decision**: Search across both title and description fields (case-insensitive substring match).

**Rationale**:
- Spec requirement FR-009: "search todos by keyword across both title and description fields"
- Users often put actionable details in the description (e.g., "grocery store" in description when title is "Shopping")
- Simple `keyword.lower() in field.lower()` substring match — no external library needed
- Case-insensitive by spec requirement FR-010

**Alternatives Considered**:
- **Title only**: Misses important context in descriptions. Rejected per spec FR-009.
- **Fuzzy matching (Levenshtein distance)**: Over-engineered for Phase I console app, requires external library. Rejected per Simplicity First principle.
- **Regex search**: Powerful but error-prone for users typing special characters, unnecessary complexity. Rejected.
- **Search across tags too**: Not in spec, but trivial to add later. Keeping scope minimal for now.

**Implementation Sketch**:
```python
def search_todos(self, keyword: str) -> list[Todo]:
    keyword_lower = keyword.lower()
    return [
        todo for todo in self.todos.values()
        if keyword_lower in todo.title.lower()
        or keyword_lower in todo.description.lower()
    ]
```

---

## Decision 4: Filter Logic — Single vs. Combined Filters

**Decision**: Single filter dimension per operation (status OR priority OR category), with combined filter+sort as a separate menu option.

**Rationale**:
- Spec assumption: "Filtering applies one filter dimension at a time from the menu"
- Spec User Story 6 (P3): Combined filter and sort as distinct feature
- Simplifies CLI interaction: user chooses one filter type, enters one value
- Avoids complex multi-step filter builder UI in a console app
- The "Filter & Sort" menu option provides the combined experience

**Alternatives Considered**:
- **Multi-dimensional filter (AND logic)**: Requires complex multi-step input ("Filter by priority? [Enter to skip] Filter by status? [Enter to skip]..."). Too complex for console. Rejected for Phase I.
- **Filter chaining (additive)**: Accumulates filters across operations — confusing state management. Rejected.

**Filter Types**:
1. **By Status**: complete / incomplete
2. **By Priority**: high / medium / low
3. **By Category**: user enters a tag name

**Filter Method Signatures**:
```python
def filter_by_status(self, completed: bool) -> list[Todo]
def filter_by_priority(self, priority: Priority) -> list[Todo]
def filter_by_tag(self, tag: str) -> list[Todo]
```

---

## Decision 5: Sort Precedence Rules

**Decision**: Three sort options (priority, creation date, alphabetical by title) with stable sort behavior for equal keys.

**Rationale**:
- Spec requirements FR-016, FR-017, FR-018
- Python's `sorted()` is stable by default — equal elements retain their original order (creation order)
- Priority sort uses enum integer values: HIGH(1) < MEDIUM(2) < LOW(3), so ascending sort = highest first
- Date sort: ascending = oldest first, descending = newest first (offer both)
- Alphabetical: case-insensitive `title.lower()` as sort key

**Alternatives Considered**:
- **Multi-key sort (primary + secondary)**: Over-engineered for spec scope. Users can sort by one dimension at a time. Rejected.
- **Custom sort order configuration**: Too complex for console UI. Rejected.

**Sort Options**:
1. **By Priority**: HIGH → MEDIUM → LOW (ascending by enum value)
2. **By Date (newest first)**: Descending by `created_at`
3. **By Date (oldest first)**: Ascending by `created_at`
4. **By Title (A-Z)**: Ascending alphabetical, case-insensitive

**Implementation Sketch**:
```python
def sort_todos(self, todos: list[Todo], sort_by: str) -> list[Todo]:
    if sort_by == "priority":
        return sorted(todos, key=lambda t: t.priority.value)
    elif sort_by == "date_newest":
        return sorted(todos, key=lambda t: t.created_at, reverse=True)
    elif sort_by == "date_oldest":
        return sorted(todos, key=lambda t: t.created_at)
    elif sort_by == "title":
        return sorted(todos, key=lambda t: t.title.lower())
    return todos
```

---

## Decision 6: Menu Extension Strategy

**Decision**: Extend existing menu from 6 options to 9 options (add Search, Filter, Sort).

**Rationale**:
- Spec FR-020: "present new menu options for Search, Filter, and Sort operations"
- Existing menu: 1-Add, 2-View, 3-Update, 4-Delete, 5-Complete, 6-Exit
- New menu: keep existing items, insert new features before Exit
- Exit always last (user expectation)

**New Menu Layout**:
```
1. Add Todo
2. View All Todos
3. Update Todo
4. Delete Todo
5. Mark Todo as Complete
6. Search Todos
7. Filter Todos
8. Sort Todos
9. Exit
```

**Alternatives Considered**:
- **Sub-menus**: Search/Filter/Sort under a "View" sub-menu. Adds navigation depth, confusing for console. Rejected.
- **Keep Exit at 6, add 7-9 after**: Non-standard — users expect Exit last. Rejected.
- **Combined "Search & Filter" option**: Spec treats them as separate stories (P2 search, P2 filter, P3 sort). Keep separate for clean mapping.

---

## Decision 7: Update Flow for New Fields (Priority, Tags)

**Decision**: Extend the existing update flow to include priority and tags update prompts.

**Rationale**:
- Spec FR-003: "allow users to update the priority of an existing todo"
- Spec FR-007: "allow users to update the tags of an existing todo"
- Existing update flow already shows current values and allows Enter-to-skip
- Same pattern applies: show current priority, prompt for new; show current tags, prompt for new
- Consistent UX with existing title/description update flow

**Update Flow Order**:
1. Enter todo ID
2. Display current todo (title, description, status, priority, tags)
3. Prompt: new title (Enter to keep)
4. Prompt: new description (Enter to keep)
5. Prompt: new priority (Enter to keep) — show valid options
6. Prompt: new tags (Enter to keep) — comma-separated

---

## Decision 8: Add Todo Flow for New Fields

**Decision**: Add priority and tags prompts to the add todo flow, after title/description.

**Rationale**:
- Spec FR-001: "assign a priority level at creation time"
- Spec FR-005: "assign zero or more tags at creation time"
- Natural flow: Title (required) → Description (optional) → Priority (optional, default medium) → Tags (optional)
- Priority prompt shows valid options and accepts Enter for default
- Tags prompt accepts comma-separated values, Enter for no tags

---

## Decision 9: Display Format Enhancement

**Decision**: Extend the view table to include priority and tags columns.

**Rationale**:
- Spec FR-004: "display the priority level alongside each todo"
- Spec FR-008: "display tags alongside each todo"
- Existing table: `ID | Status | Title | Description`
- Enhanced table: `ID | Status | Priority | Title | Tags | Description`
- Priority column: 8 chars (HIGH/MEDIUM/LOW display)
- Tags column: 20 chars max (truncate with "...")

**Enhanced Display Format**:
```
 ID | Status | Priority | Title                    | Tags               | Description
----+--------+----------+--------------------------+--------------------+---------------------------
  1 | [ ]    | HIGH     | Buy groceries            | home, errands      | Milk, eggs, bread
  2 | [✓]    | MEDIUM   | Call dentist              |                    |
  3 | [ ]    | LOW      | Read book                | personal           | Chapter 5-8
```

---

## Decision 10: Enum Import Strategy for Domain Model Reusability

**Decision**: Define `Priority` enum in `models.py` alongside `Todo` dataclass.

**Rationale**:
- Keeps all domain entities in one module (Separation of Concerns — model layer)
- Both `Priority` and `Todo` are domain concepts, not service/CLI concerns
- Clean import: `from src.todo_app.models import Todo, Priority`
- Supports Constitution Principle IV: domain model reusable across phases

---

## Summary of All Unknowns Resolved

| Unknown | Resolution | Decision # |
|---------|-----------|------------|
| Priority representation | Python Enum (HIGH=1, MEDIUM=2, LOW=3) | #1 |
| Tag structure | `list[str]`, comma-separated input, normalized | #2 |
| Search scope | Title + Description, case-insensitive substring | #3 |
| Filter logic | Single dimension per operation | #4 |
| Sort precedence | Stable sort by one key; 4 options | #5 |
| Menu layout | Extended to 9 options (add Search, Filter, Sort) | #6 |
| Update flow | Extend with priority + tags prompts | #7 |
| Add flow | Extend with priority + tags prompts | #8 |
| Display format | Add Priority + Tags columns to table | #9 |
| Enum location | In models.py with Todo | #10 |

---

## References

- Specification: `specs/003-intermediate-todo-features/spec.md`
- Phase I Plan: `specs/001-console-todo/plan.md`
- Phase I Data Model: `specs/001-console-todo/data-model.md`
- Constitution: `.specify/memory/constitution.md`
- Python enum docs: https://docs.python.org/3/library/enum.html
