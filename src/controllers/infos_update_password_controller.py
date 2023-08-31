"""
Description:
Utilisée par info_console. Infos générales à propos de la poilitique de mots de passe.
Un utilisateur doit pouvoir mettre à jour son mot de passe.
Noter qu'un nouvel utilisateur crée par le service Gestion, aura un mot de passe à changer.
"""
from rich import print

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.settings import settings
    from src.utils.utils import display_banner
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from settings import settings
    from utils.utils import display_banner


APP_DICT = language_bridge.LanguageBridge()


def display_info_password_policy():
    """
    Description:
    Appelée par info_console.
    Sert à présenter à l'utilisateur la politique de mots de passe, dans le terminal courant.
    """
    display_banner()
    directives = settings.NEW_PASSWORD_POLICY
    printer.print_message(
        "info", APP_DICT.get_appli_dictionnary()["PASSWORD_POLICY_TITLE"]
    )
    for directive in directives:
        directive_styled = f"{directive}"
        print(f'{directive_styled}: [white]{eval(f"settings.{directive}")}[/white]')
