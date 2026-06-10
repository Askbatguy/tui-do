from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import ScrollableContainer
from textual.widgets import Header, Footer, Static

class HelpMenu(Screen):

    BINDINGS = [
        ("escape", "exit_help", "exit help menu"),
        ("q", "exit_help", "exit help menu"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        with ScrollableContainer(id="help-menu"):
            yield Static(HELP_CONTENT,id="Help-content")
        yield Footer()

    def action_exit_help(self) -> None:
        self.app.pop_screen()

HELP_CONTENT = """
[bold yellow]━━━ KEYBOARD REFERENCE ━━━[/bold yellow]

[bold]NAVIGATION[/bold]
  [cyan]Tab[/cyan]         Switch focus between sidebar and todo table
  [cyan]↑ / ↓[/cyan]       Move between categories or todos
  [cyan]Enter[/cyan]       View todo details
  [cyan]Ctrl+Q[/cyan]      Quit the app
  [cyan]/[/cyan]           Search todos across all categories

[bold]TODOS[/bold]  [dim](focus the todo table first)[/dim]
  [cyan]a[/cyan]           Add a new todo
  [cyan]d[/cyan]           Delete selected todo
  [cyan]e[/cyan]           Edit selected todo
  [cyan]Space[/cyan]       Toggle todo as done/not done
  [cyan]h[/cyan]           Hide/show completed todos
  [cyan]s[/cyan]           Cycle sort: none → name → priority → due date

[bold]CATEGORIES[/bold]  [dim](focus the sidebar first)[/dim]
  [cyan]a[/cyan]           Add a new category
  [cyan]d[/cyan]           Delete category and all its todos
  [cyan]e[/cyan]           Rename category

[bold]MOUSE[/bold]
  [cyan]Left click[/cyan]      View todo details
  [cyan]Right click[/cyan]     Edit todo
  [cyan]Click ☐ / ✅[/cyan]         Toggle done

[bold yellow]━━━ HOW TO USE TUI-DO ━━━[/bold yellow]

[bold]Getting Started[/bold]
  When you first launch tui-do, two sample categories ("Work" and 
  "Personal") are created with example todos so you can explore 
  the app straight away. Feel free to delete them when you're ready 
  to add your own.

  When you open tui-do you'll see two panels. The left sidebar lists 
  your categories — think of these as projects or areas of your life. 
  The right panel shows the todos inside the selected category.

  Press [cyan]Tab[/cyan] to switch focus between the two panels. The active panel 
  is highlighted with a coloured border. Keybindings in the footer 
  update to show what's available in the focused panel.

[bold]Working with Categories[/bold]
  Focus the sidebar with [cyan]Tab[/cyan] and press [cyan]a[/cyan] to create your first category.
  Give it a name like "Work", "Personal", or "Shopping". Each category 
  shows a [cyan](done/total)[/cyan] count so you can see progress at a glance.

  Press [cyan]e[/cyan] to rename a category and [cyan]d[/cyan] to delete one. Deleting a category 
  removes all its todos permanently — you'll be warned first.

[bold]Managing Todos[/bold]
  Select a category, then [cyan]Tab[/cyan] to the todo panel and press [cyan]a[/cyan] to add a todo.
  Fill in the title (required), priority, due date, and notes. Due dates 
  use the format [cyan]YYYY-MM-DD[/cyan] (e.g. 2026-06-15).

  Todos with passed due dates show in [red]red[/red]. Press [cyan]Space[/cyan] to mark a todo 
  done — it'll turn green and stop showing as overdue.

[bold]Tips & Tricks[/bold]
  • Press [cyan]s[/cyan] to cycle through sort modes — handy for seeing what's 
    due soonest.
  • Press [cyan]h[/cyan] to hide completed todos and reduce clutter.
  • Press [cyan]/[/cyan] to search todos across all categories.
  • Right-click any todo to edit it instantly.
  • The splash screen on startup shows your most urgent todos.
  • Use [cyan]Ctrl+P[/cyan] to switch themes — tui-do looks great in any theme!
  • Every time you open tui-do, the splash screen shows a 
    [cyan]TODAY'S BRIEFING[/cyan] — your most urgent todos ranked by deadline. 
    Overdue todos appear first in [red]red[/red], followed by upcoming ones 
    in [green]green[/green]. A great way to start your day!

[bold yellow]━━━ THE DAILY BRIEFING ━━━[/bold yellow]

  The splash screen on startup isn't just decoration — it's your 
  daily priorities at a glance. It scans ALL your todos across ALL 
  categories and surfaces the most urgent ones:

  [red]🔴 Overdue[/red]     Tasks past their due date, most overdue first
  [yellow]🟡 Due today[/yellow]   Tasks due right now — don't miss these!
  [green]🟢 Upcoming[/green]    Tasks due soon, closest deadline first

  Completed todos never appear in the briefing. Up to 5 todos are 
  shown. If you see nothing, you're all caught up! 🎉

"""