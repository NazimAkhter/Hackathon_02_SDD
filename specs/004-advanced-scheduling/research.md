# Research: Advanced Scheduling Features for In-Memory Python Console Todo App

**Feature**: 004-advanced-scheduling
**Date**: 2026-02-08
**Phase**: 0 (Outline & Research)

## Purpose

Resolve all technical unknowns and architectural decisions before designing the data model, contracts, and implementation plan. Each decision documents what was chosen, why, and what alternatives were considered.

---

## Decision 1: Due Date Representation — datetime Object vs String

**Decision**: Use Python `datetime` object from the standard library.

**Rationale**:
- Native Python type with built-in comparison operators (`<`, `>`, `==`) for overdue detection
- Standard library support for parsing (strptime), formatting (strftime), and arithmetic (timedelta)
- Type safety: `due_date: datetime | None` enforces correct type at the model level
- Easy relative time calculations for "upcoming" (due within 7 days) and "overdue" (past due) logic
- No external dependencies required
- Serialization for future phases: datetime is easily converted to ISO 8601 strings for JSON/database storage

**Alternatives Considered**:
- **String storage (e.g., "2026-02-15 14:00")**: Requires manual parsing and comparison logic, error-prone, no type safety. Rejected for complexity and lack of built-in comparison.
- **Unix timestamp (int)**: Compact but loses human readability, requires timezone handling, harder to debug. Rejected for poor developer experience.
- **dateutil library**: Adds external dependency for minimal benefit (strptime handles our fixed format). Rejected per Simplicity First principle.

**Implementation Sketch**:
```python
from datetime import datetime
from typing import Optional

@dataclass
class Todo:
    # ... existing fields ...
    due_date: Optional[datetime] = None
```

---

## Decision 2: Recurrence Model Design — Enum vs Rule-Based

**Decision**: Use Python `enum.Enum` for recurrence types.

**Rationale**:
- Spec requires exactly 3 recurrence types: daily, weekly, monthly (fixed set, no complex patterns)
- Enum provides type safety and constrains valid values at compile time
- Simple mapping: `NONE`, `DAILY`, `WEEKLY`, `MONTHLY` covers all specified requirements
- Easy to extend later if more types are needed (e.g., `YEARLY`, `BIWEEKLY`)
- Clean integration with match/case statements for next-due-date calculation
- No external recurrence rule library needed (spec explicitly excludes complex patterns like "every other day")

**Alternatives Considered**:
- **Rule-based system (e.g., iCalendar RRULE)**: Over-engineered for 3 simple types, adds complexity and external dependencies. Rejected per Simplicity First.
- **String constants ("daily", "weekly", "monthly")**: No type safety, easy to introduce typos. Rejected in favor of enum for compile-time checks.
- **Boolean flags (is_daily, is_weekly, is_monthly)**: Awkward API, allows invalid states (multiple flags true). Rejected for poor design.

**Implementation Sketch**:
```python
from enum import Enum

class Recurrence(Enum):
    """Recurrence types for todos."""
    NONE = "none"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
```

---

## Decision 3: Recurrence Trigger Point — On Completion vs Time-Based

**Decision**: Trigger recurrence on completion (user action), not time-based automatic creation.

**Rationale**:
- Spec requirement (FR-014): "When a recurring todo is marked complete, system MUST automatically create a new instance"
- Simpler implementation: no background jobs, timers, or cron-like scheduling needed
- User maintains control: recurring tasks don't pile up if the user doesn't complete them
- In-memory constraint: time-based triggers would require persistent state across restarts (not allowed)
- Matches user mental model: "I finish a task, and it gets rescheduled for next time"

**Alternatives Considered**:
- **Time-based automatic creation**: Would create new instances at scheduled times even if previous instance not complete. Adds complexity (background jobs, persistent state), creates clutter (multiple incomplete instances), violates in-memory constraint. Rejected.
- **Hybrid approach (time-based + manual)**: Overly complex for console app scope. Rejected per Simplicity First.

**Implementation Sketch**:
```python
def mark_complete(self, todo_id: int) -> bool:
    todo = self.todos.get(todo_id)
    if not todo:
        return False

    todo.mark_complete()

    # If recurring, create next instance
    if todo.recurrence != Recurrence.NONE:
        self._reschedule_recurring_todo(todo)

    return True
```

---

## Decision 4: Overdue Detection Strategy — View-Time Calculation vs Cached State

**Decision**: Calculate overdue status at view time based on current system time.

**Rationale**:
- Spec requirement (FR-026): "System MUST update overdue status dynamically based on current system time at view time"
- Always accurate: no risk of stale cached state
- Simple implementation: `is_overdue = todo.due_date < datetime.now() and not todo.completed`
- No background jobs or periodic updates required
- Works correctly across clock changes (DST, manual adjustments)
- In-memory constraint: caching would not persist across restarts anyway

**Alternatives Considered**:
- **Cached overdue flag**: Would need to be recalculated periodically or on every operation. Adds complexity, risk of stale state, no performance benefit for console app scale (< 1000 todos). Rejected.
- **Event-driven updates**: Would require background thread or timer to update flags. Overly complex for console app. Rejected.

**Implementation Sketch**:
```python
def is_overdue(self, todo: Todo) -> bool:
    """Check if a todo is overdue (past due date and not complete)."""
    if todo.due_date is None or todo.completed:
        return False
    return datetime.now() > todo.due_date

def get_overdue_todos(self) -> List[Todo]:
    """Return all overdue todos."""
    return [t for t in self.todos.values() if self.is_overdue(t)]
```

---

## Decision 5: Date Input Validation — strptime vs dateutil vs Manual Parsing

**Decision**: Use `datetime.strptime()` from Python standard library with fixed format "YYYY-MM-DD HH:MM".

**Rationale**:
- Spec requirement (FR-003): Fixed format "YYYY-MM-DD HH:MM" (24-hour time)
- Standard library strptime handles this format natively: `datetime.strptime(input, "%Y-%m-%d %H:%M")`
- Type-safe error handling: raises ValueError for invalid formats, which CLI can catch and display clear error message
- No external dependencies required
- Simple validation logic: try/except around strptime call

**Alternatives Considered**:
- **dateutil.parser**: Flexible parsing (e.g., "tomorrow", "next week") but adds external dependency and is more complex than needed. Spec explicitly uses fixed format. Rejected.
- **Manual regex parsing**: Error-prone, reinvents the wheel. Rejected in favor of standard library.
- **Multiple format support**: Would require trying multiple strptime calls or regex alternatives. Adds complexity without benefit. Rejected.

**Implementation Sketch**:
```python
def _parse_due_date(self, date_input: str) -> Optional[datetime]:
    """Parse due date input (YYYY-MM-DD HH:MM) or return None if invalid."""
    if not date_input or not date_input.strip():
        return None

    try:
        return datetime.strptime(date_input.strip(), "%Y-%m-%d %H:%M")
    except ValueError:
        raise ValueError("Invalid date format. Please use YYYY-MM-DD HH:MM (e.g., 2026-02-15 14:00)")
```

---

## Decision 6: Monthly Recurrence Edge Cases — Handling Non-Existent Dates

**Decision**: Use last day of month as fallback when the target day doesn't exist.

**Rationale**:
- Spec requirement (edge case): "monthly recurrence for Jan 31 → Feb has no 31st"
- Spec solution (edge case): "Use last day of month as fallback"
- Python `calendar.monthrange()` provides the number of days in a month
- User expectation: A task due on the 31st monthly should repeat "at the end of each month"
- Deterministic behavior: Same fallback logic for all non-existent dates

**Alternatives Considered**:
- **Skip to next month**: Would create a gap (Jan 31 → Mar 31, skipping Feb entirely). User loses tracking. Rejected.
- **Round down to 28th**: Arbitrary choice, doesn't match "end of month" expectation. Rejected.
- **Error/fail**: Would prevent users from creating monthly tasks on days 29-31. Too restrictive. Rejected.

**Implementation Sketch**:
```python
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

def _calculate_next_due_date(self, current_due: datetime, recurrence: Recurrence) -> datetime:
    """Calculate next due date based on recurrence type."""
    if recurrence == Recurrence.DAILY:
        return current_due + timedelta(days=1)
    elif recurrence == Recurrence.WEEKLY:
        return current_due + timedelta(weeks=1)
    elif recurrence == Recurrence.MONTHLY:
        # Add one month
        next_month = current_due + relativedelta(months=1)
        # Handle non-existent dates (e.g., Jan 31 → Feb)
        target_day = current_due.day
        max_day = calendar.monthrange(next_month.year, next_month.month)[1]
        if target_day > max_day:
            # Use last day of month
            return next_month.replace(day=max_day)
        return next_month
    else:
        return current_due
```

**Note**: While `dateutil.relativedelta` is shown above for clarity, we can achieve the same result using only the standard library by manually calculating the next month and handling day overflow. If we want to avoid `dateutil`, we'll use `calendar` module for month arithmetic.

---

## Decision 7: Integration with Existing Features — Due Dates and Filter/Sort

**Decision**: Extend existing filter and sort mechanisms to support due_date field.

**Rationale**:
- Spec requirement (US5 - FR-023): "System MUST support sorting todos by due date"
- Existing architecture (Phase I.5) already has `filter_by_*` and `sort_todos` methods
- Additive integration: add `filter_by_due_date_range()` and extend `sort_todos()` with "due_date" option
- Backward compatible: existing filters and sorts continue to work unchanged
- Consistent API: users interact with due date filtering the same way as priority/tag filtering

**Alternatives Considered**:
- **Separate due date filtering UI**: Would fragment user experience (different menus for different filter types). Rejected for inconsistency.
- **Combined filter dimensions**: Allow filtering by priority AND due date simultaneously. More complex, not required by spec. Deferred to future enhancement.

**Implementation Sketch**:
```python
def filter_by_due_date_range(self, start_date: datetime, end_date: datetime) -> List[Todo]:
    """Filter todos by due date range."""
    matching = [
        todo for todo in self.todos.values()
        if todo.due_date and start_date <= todo.due_date <= end_date
    ]
    return sorted(matching, key=lambda t: t.due_date or datetime.max)

def sort_todos(self, todos: Optional[List[Todo]] = None, sort_by: str = "priority") -> List[Todo]:
    # ... existing priority, date_newest, date_oldest, title sorts ...

    if sort_by == "due_date":
        # Todos without due dates go to the end
        return sorted(todos, key=lambda t: t.due_date or datetime.max)
    elif sort_by == "due_date_desc":
        return sorted(todos, key=lambda t: t.due_date or datetime.min, reverse=True)
    # ...
```

---

## Decision 8: Display Format — Relative vs Absolute Date Formatting

**Decision**: Use absolute format for list display ("2026-02-15 14:00"), with optional relative indicators ("⚠ OVERDUE", "📅 DUE SOON").

**Rationale**:
- Spec requirement (FR-006): "System MUST display due dates in a human-readable format"
- Spec acceptance (US1-5): Shows absolute dates in examples ("2026-02-15 14:00")
- Spec acceptance (US2-1): Visual indicators for overdue and due soon
- Absolute format provides precise information (exact date and time)
- Relative format ("in 7 days") requires recalculation on every view, less precise
- Hybrid approach: absolute date + status indicator provides both precision and quick visual cues

**Alternatives Considered**:
- **Pure relative format ("in 7 days", "2 days ago")**: Less precise, harder to understand at a glance (is "in 7 days" next Monday or Tuesday?). Rejected.
- **Both relative and absolute**: Would clutter display. Rejected for simplicity.
- **Relative only for upcoming/overdue**: Inconsistent display (some todos show "in 3 days", others show "2026-02-20"). Rejected for inconsistency.

**Implementation Sketch**:
```python
def __str__(self) -> str:
    """Human-readable representation for CLI display."""
    status = "[✓]" if self.completed else "[ ]"
    priority_display = self.priority.name
    title_display = self.title[:21] + "..." if len(self.title) > 24 else self.title
    tags_display = ", ".join(self.tags) if self.tags else ""

    # Due date display with status indicator
    if self.due_date:
        due_display = self.due_date.strftime("%Y-%m-%d %H:%M")
        if not self.completed:
            if self.due_date < datetime.now():
                due_display = f"⚠ {due_display}"  # Overdue
            elif (self.due_date - datetime.now()).days <= 7:
                due_display = f"📅 {due_display}"  # Due soon
    else:
        due_display = "(no due date)"

    recurrence_display = ""
    if self.recurrence != Recurrence.NONE:
        recurrence_display = f"🔁 {self.recurrence.value}"

    return (
        f"{self.id:3d} | {status:6s} | {priority_display:8s} | "
        f"{title_display:24s} | {tags_display:20s} | {due_display:22s} | "
        f"{recurrence_display:12s}"
    )
```

---

## Decision 9: Preventing Duplicate Recurring Instances

**Decision**: Use a boolean flag `is_recurring_parent` to track which todo is the "current" recurring instance and prevent duplicate rescheduling.

**Rationale**:
- Spec requirement (FR-015): "System MUST prevent duplicate rescheduling"
- Edge case: User marks a recurring todo complete twice in quick succession
- Solution: When a recurring todo is marked complete, create the next instance and set `is_recurring_parent=False` on the completed instance
- Only todos with `is_recurring_parent=True` trigger rescheduling on completion
- Simple boolean flag, no complex state machine required

**Alternatives Considered**:
- **Check for existing next instance**: Would require searching for todos with the same title and next due date. Fragile if user changes title. Rejected.
- **Single reschedule per ID**: Would require tracking reschedule history in a separate data structure. Adds complexity. Rejected.
- **Disable recurrence on completion**: Would prevent users from completing and immediately marking complete again (legitimate use case). Rejected.

**Implementation Sketch**:
```python
@dataclass
class Todo:
    # ... existing fields ...
    due_date: Optional[datetime] = None
    recurrence: Recurrence = Recurrence.NONE
    is_recurring_parent: bool = True  # Only true recurring instance triggers reschedule

def mark_complete(self, todo_id: int) -> bool:
    todo = self.todos.get(todo_id)
    if not todo:
        return False

    todo.mark_complete()

    # Only reschedule if this is the active recurring instance
    if todo.recurrence != Recurrence.NONE and todo.is_recurring_parent:
        next_due = self._calculate_next_due_date(todo.due_date, todo.recurrence)
        new_todo = self.add_todo(
            title=todo.title,
            description=todo.description,
            priority=todo.priority,
            tags=todo.tags,
            due_date=next_due,
            recurrence=todo.recurrence
        )
        # Mark original as no longer the parent
        todo.is_recurring_parent = False

    return True
```

---

## Summary of All Unknowns Resolved

| Unknown | Resolution | Decision # |
|---------|-----------|------------|
| Due date representation | Python datetime object | #1 |
| Recurrence model | Enum (NONE, DAILY, WEEKLY, MONTHLY) | #2 |
| Recurrence trigger | On completion (user action) | #3 |
| Overdue detection | View-time calculation with datetime.now() | #4 |
| Date input validation | strptime with "%Y-%m-%d %H:%M" format | #5 |
| Monthly recurrence edge cases | Last day of month fallback | #6 |
| Integration with existing features | Extend filter/sort methods additively | #7 |
| Display format | Absolute dates + visual indicators | #8 |
| Duplicate reschedule prevention | is_recurring_parent boolean flag | #9 |

---

## References

- Specification: `specs/004-advanced-scheduling/spec.md`
- Phase I.5 Plan: `specs/003-intermediate-todo-features/plan.md`
- Phase I.5 Data Model: `specs/003-intermediate-todo-features/data-model.md`
- Constitution: `.specify/memory/constitution.md`
- Python datetime docs: https://docs.python.org/3/library/datetime.html
- Python enum docs: https://docs.python.org/3/library/enum.html
- Python calendar docs: https://docs.python.org/3/library/calendar.html
