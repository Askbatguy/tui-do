from textual.app import App, ComposeResult
from textual.widgets import Header, Footer,ListView, ListItem, ProgressBar, Label
from textual.containers import Horizontal, Vertical
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
            with Vertical(id="main-panel"):
                with Horizontal(id="todo-header"):
                    yield Label("Select a category", id="category-label")
                    yield Label("", id="task-count")
                yield ProgressBar(total=100, id="todo-progress", show_eta= False)
                yield TodoTable(id="main")
        yield Footer()
    

    def action_quit(self) -> None:
        self.exit()

    def on_list_view_selected(self, event: ListView.Selected) -> None:
        category_id = event.item.data
        self.selected_category_id = category_id

        for item in self.query_one("#sidebar", CategoryList).query(ListItem):
            item.remove_class("selected-category")
        event.item.add_class("selected-category")

        todos = self.store.get_todos_for_category(category_id)
        done_count = sum(t.done for t in todos)
        total_count = len(todos)
        category = next (c for c in self.store.categories if c.id == category_id)
        self.query_one("#category-label", Label).update(f"📋 {category.name}")
        self.query_one("#task-count", Label).update(f"{done_count} of {total_count} done")
        progress_bar = self.query_one("#todo-progress", ProgressBar)
        progress_bar.total = total_count if total_count > 0 else 1
        progress_bar.progress = done_count
        self.query_one("#main", TodoTable).refresh_todos(category_id)

    def refresh_todo_header(self) -> None:
        if not self.selected_category_id:
            return
        todos = self.store.get_todos_for_category(self.selected_category_id)
        done_count = sum(t.done for t in todos)
        total_count = len(todos)
        self.query_one("#task-count", Label).update(f"{done_count} of {total_count} done")
        progress_bar = self.query_one("#todo-progress", ProgressBar)
        progress_bar.total = total_count if total_count > 0 else 1
        progress_bar.progress = done_count


if __name__ == "__main__":
    TuiDoApp().run()


