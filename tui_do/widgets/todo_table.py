from textual.widgets import DataTable
from textual.app import App
from ..models import Todo
from ..screens.modals import AddTodoModal, EditTodoModal, ConfirmDeleteModal


class TodoTable(DataTable):

    BINDINGS = [
        ("a", "add_todo", "Add"),
        ("d", "delete_todo", "Delete"),
        ("e", "edit_todo", "Edit"),
        ("space", "toggle_done", "Toggle done"),
    ]

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

    def action_toggle_done(self) -> None:
        self.toggle_done()

    def action_add_todo(self) -> None:
        if not self.app.selected_category_id:
            self.app.notify("Select a category first", severity="warning", timeout=2.50)
            return

        def on_modal_dismiss(new_todo: Todo | None) -> None:
            if new_todo:
                new_todo.category_id = self.app.selected_category_id
                self.app.store.add_todo(new_todo)
                self.refresh_todos(self.app.selected_category_id)
        
        self.app.push_screen(AddTodoModal(), on_modal_dismiss)

    def action_delete_todo(self) -> None:
        todo_id = self.get_selected_todo_id()
        if not todo_id:
            self.app.notify("No todo selected", severity="warning", timeout=2.5)
            return
        todo = next((t for t in self.app.store.todos if t.id == todo_id), None)
        if not todo:
            return
        
        def on_confirm(confirmed: bool) -> None:
            if confirmed:
                self.app.store.delete_todo(todo_id)
                self.refresh_todos(self.app.selected_category_id)

        self.app.push_screen(ConfirmDeleteModal(f"Delete '{todo.title}'? This cannot be undone."), on_confirm)

    def action_edit_todo(self) -> None:
        todo_id = self.get_selected_todo_id()
        if not todo_id:
            self.app.notify("No todo selected", severity="warning", timeout=2.5)
            return
        todo = next((t for t in self.app.store.todos if t.id == todo_id), None)
        if not todo:
            return
        
        def on_edit_dismiss(updated_todo: Todo | None ) -> None:
            if updated_todo:
                self.app.store._save()
                self.refresh_todos(self.app.selected_category_id)

        self.app.push_screen(EditTodoModal(todo), on_edit_dismiss)

