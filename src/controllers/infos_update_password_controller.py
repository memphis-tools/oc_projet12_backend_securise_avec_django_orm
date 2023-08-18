from rich import print

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.settings import settings
    from src.utils.utils import display_banner
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from settings import settings
    from utils.utils import display_banner


def display_info_password_policy():
    display_banner()
    directives = settings.NEW_PASSWORD_POLICY
    printer.print_message("info", self.app_dict.get_appli_dictionnary()['PASSWORD_POLICY_TITLE'])
    for directive in directives:
        directive_styled = f"{directive}"
        print(f'{directive_styled}: [white]{eval(f"settings.{directive}")}[/white]')
