from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Button, Input, Label, Select, Static, ListView, ListItem
from textual.containers import Vertical, Horizontal
from textual.fuzzy import Matcher
from ..models import Todo, Priority


class AddTodoModal(ModalScreen):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
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
        if priority_val is Select.NULL:
            priority_val = Priority.MEDIUM.value
            self.app.notify("Priority defaulted to medium - edit todo to change", timeout=3)
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
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message

    def compose(self) -> ComposeResult:
        with Vertical(id="dialog"):
            yield Label( self.message ,id="dialog-title")
            with Horizontal(id="dialog-buttons"):
                yield Button("Delete", variant="error", id="btn-confirm")
                yield Button("Cancel", variant="default", id="btn-cancel")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-confirm":
            self.dismiss(True)
        else:
            self.dismiss(False)

class EditTodoModal(ModalScreen):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
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

class CategoryNameModal(ModalScreen):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
    def __init__(self, existing_name: str = "") -> None:
        super().__init__()
        self.existing_name = existing_name

    def compose(self) -> ComposeResult:
        is_rename = bool(self.existing_name)
        with Vertical(id="dialog"):
            yield Label("Rename Category" if is_rename else "New Category", id="dialog-title")
            yield Input(
                value=self.existing_name,
                placeholder="Category name",
                id="input-name"
            )
            with Horizontal(id="dialog-buttons"):
                yield Button("Save" if is_rename else "Add", variant="primary", id="btn-confirm")
                yield Button("Cancel", variant="default",id="btn-cancel")
    
    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "btn-cancel":
            self.dismiss(None)
        elif event.button.id == "btn-confirm":
            name = self.query_one("#input-name", Input).value.strip()
            if not name:
                self.query_one("#dialog-title", Label).update("⚠️ Name is required")
                return
            self.dismiss(name)


class TodoDetailModal(ModalScreen):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
    def __init__(self, todo: Todo) -> None:
        super().__init__()
        self.todo = todo

    def compose(self) -> ComposeResult:
        category = next(c for c in self.app.store.categories if c.id == self.todo.category_id)

        if self.todo.done:
            due_str = f"{self.todo.due_date} ([green]Completed ✅[/green])" if self.todo.due_date else "Completed ✅"
        elif self.todo.days_until_due is None:
           due_str = "No due date"
        elif self.todo.days_until_due < 0:
            due_str = f"{self.todo.due_date} ([red]{abs(self.todo.days_until_due)} days overdue!!![/red])"
        elif self.todo.days_until_due == 0:
            due_str = f"{self.todo.due_date} ([yellow]Due today![/yellow])"
        else:
            due_str = f"{self.todo.due_date} ([green]{self.todo.days_until_due} days remaining[/green])"
        
        priority_colours = {
            "high": "orange",
            "medium": "yellow",
            "low": "green",
        }
        colour = priority_colours[self.todo.priority.value]

        with Vertical(id="todo-detail"):
            yield Static(f"[bold]{self.todo.title}[/bold]", id="detail-title")
            yield Static(f"[dim]Category:[/dim] {category.name}")
            yield Static(f"[dim]Priority:[/dim] [{colour}]{self.todo.priority.value}[/{colour}]")
            yield Static(f"[dim]Due:[/dim] {due_str}")
            yield Static(f"[dim]Created:[/dim] {self.todo.created_at}")
            yield Static(f"[dim]Notes:[/dim] {self.todo.notes if self.todo.notes else 'No Notes!'}")
            yield Static(f"[dim]Done:[/dim] {'✅ [green]Yes[/green]' if self.todo.done else '☐ [yellow]No[/yellow]'}")
            yield Static(f"[dim italic]press any key to close[/dim italic]", id="detail-hint")
        
    def on_key(self, event) -> None:
        event.stop()
        self.dismiss()
        
    def on_click(self, event) -> None:
        event.stop()
        self.dismiss()

class GlobalSearchModal(ModalScreen[Todo | None]):
    BINDINGS = [("escape", "dismiss(None)", "Cancel")]
    
    def compose(self) -> ComposeResult:
        with Vertical(id="search-panel"):
            yield Static("Press \\[Esc] to exit",id="search-hint")
            yield Input(placeholder="Search todos...",id="search-field")
            yield Static("Title",classes="result-header")
            yield Static("[cyan dim]\\[Category Name]---Priority---Due Date[/cyan dim]", classes="result-header")
            yield ListView(id="search-results")
    
    def on_input_changed(self, event:Input.Changed) -> None:
        search_term = event.value
        results = self.query_one("#search-results", ListView)
        if not search_term:
            results.clear()
            return
        
        results.clear()
        matcher = Matcher(search_term, case_sensitive= False)
        scored = []
        for todo in self.app.store.todos:
            score = matcher.match(todo.title)
            if score > 0:
                scored.append((score, todo))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        
        todos = [todo for score, todo in scored]

        for todo in todos:
            category = next(c for c in self.app.store.categories if c.id == todo.category_id)
            due = str(todo.due_date) if todo.due_date else "--"
            highlighted_title = matcher.highlight(todo.title)
            suffix = f"[cyan dim]\\[{category.name}] {todo.priority.value} {due}[/cyan dim]"
            item = ListItem(Label(highlighted_title), Label(suffix))
            item.data = todo
            results.append(item)

    def on_list_view_selected(self, event: ListView.Selected):
        todo = event.item.data 
        self.dismiss(todo)
