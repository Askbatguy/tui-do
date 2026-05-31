from textual.app import App
from textual.widgets import ListView, ListItem, Label
from ..models import Category

class CategoryList(ListView):
    def on_mount(self) -> None:
        self.refresh_categories()

    def refresh_categories(self) -> None:
        self.clear()
        for category in self.app.store.categories:
            self.append(ListItem(Label(category.name), id=f"cat-{category.id}"))

    
