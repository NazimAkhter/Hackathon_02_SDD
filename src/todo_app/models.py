"""Domain models for the todo application."""
from dataclasses import dataclass, field
from datetime import datetime


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
    """
    id: int
    title: str
    description: str = ""
    completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)

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

    def mark_complete(self) -> None:
        """Mark this todo as complete."""
        self.completed = True

    def is_complete(self) -> bool:
        """Check if todo is complete."""
        return self.completed

    def __str__(self) -> str:
        """Human-readable representation for CLI display."""
        status = "[✓]" if self.completed else "[ ]"
        # Truncate title if longer than 30 chars
        title_display = self.title[:27] + "..." if len(self.title) > 30 else self.title
        # Truncate description if longer than 50 chars
        desc_display = self.description[:47] + "..." if len(self.description) > 50 else self.description
        return f"{self.id:3d} | {status:6s} | {title_display:30s} | {desc_display}"
