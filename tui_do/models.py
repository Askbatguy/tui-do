from dataclasses import dataclass, field
from datetime import date
from enum import Enum
import uuid

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class SortMode(Enum):
    NONE = "none"
    NAME = "name"
    PRIORITY = "priority"
    DUE_DATE = "due date"

@dataclass
class Todo:
    title: str
    category_id: str
    priority: Priority = Priority.MEDIUM
    done: bool = False
    due_date: date | None = None
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: date.today().isoformat())

    @property
    def is_overdue(self) -> bool:
        return self.due_date is not None and not self.done and self.due_date < date.today()

@dataclass
class Category:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
