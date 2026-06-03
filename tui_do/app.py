from textual.app import App, ComposeResult
from textual.widgets import Header, Footer, Label, ListView, ListItem
from textual.containers import Horizontal
from textual.reactive import reactive
from .store import DataStore
from .widgets.category_list import CategoryList
from .widgets.todo_table import TodoTable
from .screens.modals import AddTodoModal, ConfirmDeleteModal, EditTodoModal, CategoryNameModal
from .models import Todo, Category

class TuiDoApp(App):
    """tui-do get it to-do yeah its a todo list app!"""

    TITLE = "tui-do"

    CSS_PATH = "styles/app.tcss"

    BINDINGS = [
        # ("keybind", "action", "Description"),
        ("space", "toggle_done", "Toggle done"),
        ("e", "edit_todo", "edit todo"),
        ("q", "quit", "Quit"),
        ("a", "add_todo", "Add"),
        ("d", "delete_todo", "Delete todo"),
        ("n", "new_category", "Add category"),
        ("r", "rename_category", "Rename"),
        ("k", "delete_category", "Delete category"),
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
        category_id = event.item.data
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

        self.push_screen(ConfirmDeleteModal(f"Delete '{todo.title}'? This cannot be undone."), on_confirm)

    def action_edit_todo(self) -> None:
        todo_id = self.query_one("#main", TodoTable).get_selected_todo_id()
        if not todo_id:
            self.notify("No todo selected", severity="warning", timeout=2.5)
            return
        todo = next((t for t in self.store.todos if t.id == todo_id), None)
        if not todo:
            return
        
        def on_edit_dismiss(updated_todo: Todo | None ) -> None:
            if updated_todo:
                self.store._save()
                self.query_one("#main", TodoTable).refresh_todos(self.selected_category_id)

        self.push_screen(EditTodoModal(todo), on_edit_dismiss)

    def action_new_category(self) -> None:
        def on_name_recieved(name: str) -> None:
            if not name:
                return
            new_category = Category(name= name)
            self.store.add_category(new_category)
            sidebar = self.query_one("#sidebar", CategoryList)
            item = ListItem(Label(name))
            item.data = new_category.id
            sidebar.append(item)

        self.push_screen(CategoryNameModal(), on_name_recieved)
                

    def action_rename_category(self) -> None:
        selected_category = self.selected_category_id
        if not selected_category:
            self.notify("No category Selected Yet!", severity="warning", timeout=2.5)
            return
        category_to_rename = next((c for c in self.store.categories if c.id == selected_category), None)
        if not category_to_rename:
            return
        existing_name = category_to_rename.name

        def on_name_updated(name: str) -> None:
            if not name:
                return
            self.store.rename_category(selected_category, name)
            for item in self.query_one("#sidebar", CategoryList).query(ListItem):
                if item.data == selected_category:
                    item.query_one(Label).update(name)

        self.push_screen(CategoryNameModal(existing_name), on_name_updated)

    def action_delete_category(self) -> None:
        selected_category_id = self.selected_category_id
        if not selected_category_id:
            self.notify("No category Selected Yet!", severity="warning", timeout=2.5)
            return
        selected_category = next((c for c in self.store.categories if c.id == selected_category_id), None)
        if not selected_category:
            return
        category_name = selected_category.name
        todo_count = len(self.store.get_todos_for_category(selected_category_id))

        def on_delete_confirmed(confirmed: bool ) -> None:
            if not confirmed:
                return
            self.store.delete_category(selected_category_id)
            for item in self.query_one("#sidebar", CategoryList).query(ListItem):
                if item.data == selected_category_id:
                    item.remove()
            self.query_one("#main", TodoTable).clear()
            self.selected_category_id = None

        self.push_screen(ConfirmDeleteModal(f"Delete {category_name}? This will also delete {todo_count} todo{'s' if todo_count != 1 else ''} forever. This action Cannot be undone!"), on_delete_confirmed)


if __name__ == "__main__":
    TuiDoApp().run()


