from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView
from textual.containers import Horizontal
from .store import DataStore
from .widgets.category_list import CategoryList

class TuiDoApp(App):
    """tui-do get it to-do yeah its a todo list app!"""

    TITLE = "tui-do"

    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        # ("keybind", "action", "Description"),
        ("q", "quit", "Quit"),
        ("a", "add_todo", "Add"),
        ("d", "delete_todo", "Delete"),
        ("/", "search", "Search"),
    ]

    def compose(self) -> ComposeResult:
        self.store = DataStore()
        yield Header()
        with Horizontal():
            yield CategoryList(id="sidebar")
            yield Label("Main content goes here", id="main")
        yield Footer()
    
    def on_mount(self) -> None:
        self.store = DataStore()

    def action_quit(self) -> None:
        self.exit()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        category_id = event.item.id.replace("cat-", "")
        category = next(c for c in self.store.categories if c.id == category_id)
        todos = self.store.get_todos_for_category(category_id)
        self.query_one('#main', Label).update(f"📋 {category.name} ({len(todos)} tasks)")

if __name__ == "__main__":
    TuiDoApp().run()


