from textual.widgets import ListView, ListItem, Label

class CategoryList(ListView):
    def on_mount(self) -> None:
        self._populate()

    def _populate(self) -> None:
        for category in self.app.store.categories:
            item = ListItem(Label(category.name))
            item.data = category.id
            self.append(item)
