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
        with Vertical(id="splash"):
            yield Label(ASCII_ART, id="splash-title")
            yield Label("A Terminal Todo-list app made with Textual", id="splash-subtitle")
            yield Label("Press Any Key to Continue", id= "splash-hint")

    def on_key(self, event) -> None:
        event.stop()
        self.dismiss()
        
