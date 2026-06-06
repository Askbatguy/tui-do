from textual.app import ComposeResult
from textual.screen import ModalScreen
from textual.widgets import Label, Static
from textual.containers import Vertical



ASCII_ART = """
 ███████████ █████  █████ █████            ██████████      ███████   
▒█▒▒▒███▒▒▒█▒▒███  ▒▒███ ▒▒███            ▒▒███▒▒▒▒███   ███▒▒▒▒▒███ 
▒   ▒███  ▒  ▒███   ▒███  ▒███             ▒███   ▒▒███ ███     ▒▒███
    ▒███     ▒███   ▒███  ▒███  ██████████ ▒███    ▒███▒███      ▒███
    ▒███     ▒███   ▒███  ▒███ ▒▒▒▒▒▒▒▒▒▒  ▒███    ▒███▒███      ▒███
    ▒███     ▒███   ▒███  ▒███             ▒███    ███ ▒▒███     ███ 
    █████    ▒▒████████   █████            ██████████   ▒▒▒███████▒  
   ▒▒▒▒▒      ▒▒▒▒▒▒▒▒   ▒▒▒▒▒            ▒▒▒▒▒▒▒▒▒▒      ▒▒▒▒▒▒▒    
"""


class SplashScreen(ModalScreen):
    def compose(self) -> ComposeResult:
        
        urgent_todos = [
            t for t in self.app.store.todos if t.days_until_due is not None and not t.done
        ]
        urgent_todos = sorted(urgent_todos, key=lambda t: t.days_until_due)
        urgent_todos = urgent_todos[:5]
        
        with Vertical(id="splash"):
            yield Label(ASCII_ART, id="splash-title")
            yield Label("A Terminal Todo-list app made with Textual", id="splash-subtitle")
            yield Label("Press Any Key to Continue", id= "splash-hint")
            if urgent_todos:
                yield Static("--" * 45, id="splash-divider")
                yield Static("TODAY'S BRIEFING", id="splash-brief-title")
                for todo in urgent_todos:
                    if todo.days_until_due < 0:
                        urgency = f"🔴 {abs(todo.days_until_due)} days overdue!!!"
                    elif todo.days_until_due == 0:
                        urgency = f"🟡 Due Today!!"
                    else:
                        urgency = f"🟢 {todo.days_until_due} days left"
                    
                    category = next(c for c in self.app.store.categories if c.id == todo.category_id )
                    yield Static(f"{urgency:<30} {todo.title:<30} \\[{category.name}]")
            

    def on_key(self, event) -> None:
        event.stop()
        self.dismiss()
        self.app.notify("Press [?] if you get lost!", timeout=4)
        
    def on_click(self, event) -> None:
        event.stop()
        self.dismiss()
        self.app.notify("Press [?] if you get lost!", timeout=4)