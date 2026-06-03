from textual.widgets import ListView, ListItem, Label
from ..models import Category
from ..screens.modals import CategoryNameModal, ConfirmDeleteModal

class CategoryList(ListView):

    BINDINGS = [
        ("a", "new_category", "Add"),
        ("d", "delete_category", "Delete"),
        ("e", "rename_category", "Edit"),
    ]

    def on_mount(self) -> None:
        self._populate()

    def _populate(self) -> None:
        for category in self.app.store.categories:
            todos = self.app.store.get_todos_for_category(category.id)
            done_count = sum(t.done for t in todos)
            total_count = len(todos)
            item = ListItem(Label(f"{category.name} ({done_count}/{total_count})"))
            item.data = category.id
            self.append(item)

    def action_new_category(self) -> None:
        def on_name_recieved(name: str) -> None:
            if not name:
                return
            new_category = Category(name= name)
            self.app.store.add_category(new_category)
            item = ListItem(Label(f"{name} (0/0)"))
            item.data = new_category.id
            self.append(item)

        self.app.push_screen(CategoryNameModal(), on_name_recieved)
                
    def action_rename_category(self) -> None:
        selected_category = self.app.selected_category_id
        if not selected_category:
            self.app.notify("No category Selected Yet!", severity="warning", timeout=2.5)
            return
        category_to_rename = next((c for c in self.app.store.categories if c.id == selected_category), None)
        if not category_to_rename:
            return
        existing_name = category_to_rename.name

        def on_name_updated(name: str) -> None:
            if not name:
                return
            self.app.store.rename_category(selected_category, name)
            for item in self.query(ListItem):
                if item.data == selected_category:
                    item.query_one(Label).update(name)

        self.app.push_screen(CategoryNameModal(existing_name), on_name_updated)

    def action_delete_category(self) -> None:
        selected_category_id = self.app.selected_category_id
        if not selected_category_id:
            self.app.notify("No category Selected Yet!", severity="warning", timeout=2.5)
            return
        selected_category = next((c for c in self.app.store.categories if c.id == selected_category_id), None)
        if not selected_category:
            return
        category_name = selected_category.name
        todo_count = len(self.app.store.get_todos_for_category(selected_category_id))

        def on_delete_confirmed(confirmed: bool ) -> None:
            if not confirmed:
                return
            self.app.store.delete_category(selected_category_id)
            for item in self.query(ListItem):
                if item.data == selected_category_id:
                    item.remove()
            self.app.query_one("#main").clear()
            self.app.selected_category_id = None

        self.app.push_screen(ConfirmDeleteModal(f"Delete {category_name}? This will also delete {todo_count} todo{'s' if todo_count != 1 else ''} forever. This action Cannot be undone!"), on_delete_confirmed)

    def refresh_category_count(self, category_id: str) -> None:
        for item in self.query(ListItem):
            if item.data == category_id:
                todos = self.app.store.get_todos_for_category(category_id)
                done_count = sum(t.done for t in todos)
                total_count = len(todos)
                category = next(c for c in self.app.store.categories if c.id == category_id)
                item.query_one(Label).update(f"{category.name} ({done_count}/{total_count})")
