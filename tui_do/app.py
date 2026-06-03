from textual.app import App, ComposeResult
from textual.widgets import Header, Footer,ListView
from textual.containers import Horizontal
from textual.reactive import reactive
from .store import DataStore
from .widgets.category_list import CategoryList
from .widgets.todo_table import TodoTable

class TuiDoApp(App):
    """tui-do get it to-do yeah its a todo list app!"""

    TITLE = "tui-do"

    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        # ("keybind", "action", "Description"),
        ("ctrl+q", "quit", "Quit"),
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
    

    def action_quit(self) -> None:
        self.exit()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        category_id = event.item.data
        self.selected_category_id = category_id
        self.query_one("#main", TodoTable).refresh_todos(category_id)

    
if __name__ == "__main__":
    TuiDoApp().run()


