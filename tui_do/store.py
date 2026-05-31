import dataclasses
import json
from datetime import date
from pathlib import Path
from  .models import Category, Todo, Priority
from .widgets import todo_table

DATA_FILE = Path("data/todos.json")

class DataStore:

    def _load(self) -> None:
        # Read from the json file and populate the categories and todos fields
        if not DATA_FILE.exists():
            return 
        data = json.loads(DATA_FILE.read_text())
        self.categories = [
            Category(name=c["name"], id=c["id"])
            for c in data["categories"]
        ]
        self.todos = [
            Todo(
                title=t["title"],
                category_id=t["category_id"],
                priority=Priority(t["priority"]),
                done=t["done"],
                due_date=date.fromisoformat(t["due_date"]) if t["due_date"] else None,
                notes=t["notes"],
                id=t["id"],
                created_at=t["created_at"],    
            )
            for t in data["todos"]
        ]

    def _save(self) -> None:
        # use the data to write into a json file 
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        payload = {
            "categories": [dataclasses.asdict(c) for c in self.categories],
            "todos": [
                {
                    **dataclasses.asdict(t),
                    "priority": t.priority.value,
                    "due_date": t.due_date.isoformat() if t.due_date else None,
                }
                for t in self.todos
            ],
        }
        DATA_FILE.write_text(json.dumps(payload, indent=2, default=str))

    def add_todo(self, todo:Todo) -> None:
        self.todos.append(todo)
        self._save()
    
    def delete_todo(self, todo_id: str) -> None:
        todo_to_del = next((t for t in self.todos if t.id == todo_id), None)
        if not todo_to_del:
            return
        self.todos.remove(todo_to_del)
        self._save()



    def get_todos_for_category(self, category_id: str) -> list[Todo]:
        return [t for t in self.todos if t.category_id == category_id]
    
    def seed_sample_data(self) -> None:
        work = Category(name="Work")
        personal = Category(name="Personal")
        self.categories = [work, personal]
        self.todos = [
            Todo(title="Write project report", category_id=work.id, priority=Priority.HIGH),
            Todo(title="Buy Groceries", category_id=personal.id, priority=Priority.MEDIUM),            
        ]
        self._save()

    def __init__(self):
        self.categories: list[Category] = []
        self.todos: list[Todo] = []
        self._load()
        if not self.categories:
            self.seed_sample_data()