import pathlib
import random

from rich.console import Console
from rich.theme import Theme
console = Console(width=40)

console.print("Hello, [bold blue]Niki[/] :poop:")
console.rule(f"[bold blue]:rose:niki:basketball:[/]\n")


custom_theme = Theme({
    "chill": "dim cyan",
    "warning": "magenta",
    "death": "bold red"
})

console = Console(theme=custom_theme)
console.print("This is an informational message", style="chill")
console.print("This is a warning", style="warning")
console.print("This is a danger alert!", style="death")