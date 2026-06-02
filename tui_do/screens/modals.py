from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select
from textual.containers import Vertical, Horizontal
from ..models import Todo, Priority


class AddTodoModal(ModalScreen):
    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Add Todo", id="dialog-title")
            yield Input(placeholder="Title", id="input-title")
            yield Select(
                [(p.value, p.value) for p in Priority],
                prompt="Priority",
                id="input-priority",
            )
            yield Input(placeholder="Due date (YYYY-MM-DD) - optional", id="input-due")
            yield Input(placeholder="Notes -optional", id="input-notes")
            with Horizontal(id="dialog-buttons"):
                yield Button("Add", variant="primary", id="btn-add")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-add":
            self._submit()

    def _submit(self) -> None:
        title = self.query_one("#input-title", Input).value.strip()
        if not title:
            self.query_one("#dialog-title", Label).update("⚠️ Title is required")
            return
        
        priority_val = self.query_one("#input-priority", Select).value
        due_raw = self.query_one("#input-due",Input).value.strip()
        notes = self.query_one("#input-notes", Input).value.strip()

        due_date = None
        if due_raw:
            try: 
                from datetime import date
                due_date = date.fromisoformat(due_raw)
            except ValueError:
                self.query_one("#dialog-title", Label).update("⚠️ Date must be YYYY-MM-DD")
                return

        self.dismiss(Todo(
            title=title,
            category_id="",
            priority=Priority(priority_val),
            due_date=due_date,
            notes=notes,
        )) 

class ConfirmDeleteModal(ModalScreen):
    def __init__(self, todo_title: str) -> None:
        super().__init__()
        self.todo_title = todo_title

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label(f"Delete '{self.todo_title}'?",id="dialog-title")
            yield Label("This cannot be undone.", id="dialog-subtitle")
            with Horizontal(id="dialog-buttons"):
                yield Button("Delete", variant="error", id="btn-confirm")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)

class EditTodoModal(ModalScreen):
    def __init__(self, todo: Todo) -> None:
        super().__init__()
        self.todo = todo

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label("Edit Todo", id="dialog-title")
            yield Input(value= self.todo.title, id="input-title")
            yield Select(
                [(p.value, p.value) for p in Priority],
                prompt="Priority",
                id="input-priority",
            )
            yield Input(
                value= self.todo.due_date.isoformat() if self.todo.due_date else "",
                placeholder="Due date (YYYY-MM-DD) - optional",
                id="input-due",
                )
            yield Input(
                value= self.todo.notes,
                placeholder="Notes -optional",
                id="input-notes",
                )
            with Horizontal(id="dialog-buttons"):
                yield Button("Save", variant="primary", id="btn-save")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_mount(self) -> None:
        self.query_one("#input-priority", Select).value = self.todo.priority.value

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-save":
            self._submit()

    def _submit(self) -> None:
        title = self.query_one("#input-title", Input).value.strip()
        if not title:
            self.query_one("#dialog-title", Label).update("⚠️ Title is required")
            return
        
        priority_val = self.query_one("#input-priority", Select).value
        priority = self.todo.priority if priority_val is Select.BLANK else Priority(priority_val)
        due_raw = self.query_one("#input-due",Input).value.strip()
        notes = self.query_one("#input-notes", Input).value.strip()

        due_date = None
        if due_raw:
            try: 
                from datetime import date
                due_date = date.fromisoformat(due_raw)
            except ValueError:
                self.query_one("#dialog-title", Label).update("⚠️ Date must be YYYY-MM-DD")
                return

        self.todo.title = title
        self.todo.priority = priority
        self.todo.due_date = due_date
        self.todo.notes = notes
        self.dismiss(self.todo)
