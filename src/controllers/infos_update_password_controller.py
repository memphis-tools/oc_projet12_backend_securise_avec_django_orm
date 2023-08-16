from rich import print

try:
    from src.settings import settings
    from src.utils.utils import display_banner
except ModuleNotFoundError:
    from settings import settings
    from utils.utils import display_banner


def display_info_password_policy():
    display_banner()
    directives = settings.NEW_PASSWORD_POLICY
    title = "[bold #F7E987]POLITIQUE DES MOTS DE PASSE[/bold #F7E987]"
    print(title)
    for directive in directives:
        directive_styled = f"[bold cyan]{directive}[/bold cyan]"
        print(f'{directive_styled}: [white]{eval(f"settings.{directive}")}[/white]')
