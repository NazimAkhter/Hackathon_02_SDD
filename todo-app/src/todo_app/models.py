"""Domain models for the todo application."""
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional


class Priority(Enum):
    """Priority levels for todo items, ordered by urgency."""
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
        # Title validation
        if not self.title or not self.title.strip():
            raise ValueError("Title cannot be empty")

        # Trim title
        self.title = self.title.strip()

        # Length validation
        if len(self.title) > 200:
            raise ValueError("Title cannot exceed 200 characters")

        if len(self.description) > 1000:
            raise ValueError("Description cannot exceed 1000 characters")

        # Priority validation
        if not isinstance(self.priority, Priority):
            raise ValueError(f"Priority must be a Priority enum member, got {type(self.priority)}")

        # Tags normalization
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

        # Due date validation
        if self.due_date is not None and not isinstance(self.due_date, datetime):
            raise ValueError("due_date must be a datetime object or None")

        # Recurrence validation
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
