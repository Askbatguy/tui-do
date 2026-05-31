from textual.widgets import DataTable
from textual.app import App

class TodoTable(DataTable):
    def on_mount(self) -> None:
        self.add_columns("Title", "Priority", "Due Date", "Done")
    
    def refresh_todos(self, category_id: str) -> None:
        self.clear()
        todos = self.app.store.get_todos_for_category(category_id)
        for todo in todos:
            self.add_row(
                todo.title,
                todo.priority.value,
                str(todo.due_date) if todo.due_date else "—",
                "✅" if todo.done else "☐",
            )