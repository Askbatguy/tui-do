from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label
from textual.containers import Horizontal

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
        yield Header()
        with Horizontal():
            yield Label("Sidebar goes here", id="sidebar")
            yield Label("Main content goes here", id="main")
        yield Footer()
    
    def action_quit(self) -> None:
        self.exit()

if __name__ == "__main__":
    TuiDoApp().run()


