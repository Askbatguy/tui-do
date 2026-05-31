from dataclasses import dataclass, field
from datetime import date
from enum import Enum
import uuid

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

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

@dataclass
class Category:
    name: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    