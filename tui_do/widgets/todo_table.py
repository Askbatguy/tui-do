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
                key=todo.id,
            )
    
    def get_selected_todo_id(self) -> str | None:
        if self.row_count == 0:
            return None
        row_key, _ = self.coordinate_to_cell_key(self.cursor_coordinate)
        return row_key.value
    
    def toggle_done(self) -> None:
        todo_id = self.get_selected_todo_id()
        if not todo_id:
            return
        current_row = self.cursor_row
        todo = next(t for t in self.app.store.todos if t.id == todo_id)
        todo.done = not todo.done
        self.app.store._save()
        self.refresh_todos(self.app.selected_category_id)
        if self.row_count > 0:
            self.move_cursor(row=current_row)
