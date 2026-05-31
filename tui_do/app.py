from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView
from textual.containers import Horizontal
from textual.reactive import reactive
from .store import DataStore
from .widgets.category_list import CategoryList
from .widgets.todo_table import TodoTable
from .screens.modals import AddTodoModal, ConfirmDeleteModal
from .models import Todo

class TuiDoApp(App):
    """tui-do get it to-do yeah its a todo list app!"""

    TITLE = "tui-do"

    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        # ("keybind", "action", "Description"),
        ("q", "quit", "Quit"),
        ("a", "add_todo", "Add"),
        ("d", "delete_todo", "Delete"),
        ("space", "toggle_done", "Toggle done"),
        ("/", "search", "Search"),
    ]

    selected_category_id: reactive[str | None] = reactive(None)

    def compose(self) -> ComposeResult:
        self.store = DataStore()
        yield Header()
        with Horizontal():
            yield CategoryList(id="sidebar")
            yield TodoTable(id="main")
        yield Footer()
    
    def on_mount(self) -> None:
        self.store = DataStore()

    def action_quit(self) -> None:
        self.exit()

    def action_toggle_done(self) -> None:
        self.query_one("#main", TodoTable).toggle_done()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        category_id = event.item.id.replace("cat-", "")
        self.selected_category_id = category_id
        self.query_one("#main", TodoTable).refresh_todos(category_id)

    def action_add_todo(self) -> None:
        if not self.selected_category_id:
            self.notify("Select a category first", severity="warning", timeout=2.50)
            return

        def on_modal_dismiss(new_todo: Todo | None) -> None:
            if new_todo:
                new_todo.category_id = self.selected_category_id
                self.store.add_todo(new_todo)
                self.query_one("#main", TodoTable).refresh_todos(self.selected_category_id)
        
        self.push_screen(AddTodoModal(), on_modal_dismiss)

    def action_delete_todo(self) -> None:
        todo_id = self.query_one("#main", TodoTable).get_selected_todo_id()
        if not todo_id:
            self.notify("No todo selected", severity="warning", timeout=2.5)
            return
        todo = next((t for t in self.store.todos if t.id == todo_id), None)
        if not todo:
            return
        
        def on_confirm(confirmed: bool) -> None:
            if confirmed:
                self.store.delete_todo(todo_id)
                self.query_one("#main", TodoTable).refresh_todos(self.selected_category_id)

        self.push_screen(ConfirmDeleteModal(todo.title), on_confirm)

if __name__ == "__main__":
    TuiDoApp().run()


