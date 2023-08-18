"""
Description:
De l'aide, de l'info pour les commandes. A compléter progressivement.
On insistera avant tout sur une application fonctionnelle et sécurisée, quitte à alimenter l'aide dans un 2ème temps.
"""
import click
from rich import print

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.utils.utils import display_banner
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from utils.utils import display_banner


APP_DICT = language_bridge.LanguageBridge()


@click.command
def help():
    """
    Description:
    Dédiée à introduire aux fonctions d'usage.
    """
    display_banner()
    printer.print_message("error", APP_DICT.get_appli_dictionnary()['HELP_MENU_TITLE'])

    basic_pos_commands = """
oc12_init_application: [green](ré)initialiser l'application (admin only)[/green]
oc12_token: [green]obtenir un jeton d'accès[/green]
oc12_logout: [green]se déconnecter de l'application[/green]
oc12_clients: [green]obtenir les clients de l'entreprise[/green]
oc12_collaborators: [green]obtenir les employés /collaborateurs de l'entreprise[/green]
oc12_contracts: [green]obtenir les contrats de l'entreprise[/green]
oc12_events: [green]obtenir les évènements de l'entreprise[/green]
oc12_locations: [green]obtenir les localités des évènements de l'entreprise[/green]
oc12_departments: [green]obtenir les départements /services de l'entreprise[/green]
oc12_roles: [green]obtenir les rôles possibles des employés dans l'entreprise[/green]
oc12_help: [green]obtenir de l'aide (ce menu)[/green]
    """

    print(basic_pos_commands)
