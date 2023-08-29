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
    printer.print_message("info", APP_DICT.get_appli_dictionnary()["HELP_MENU_TITLE"])
    print(f"""
    [bold cyan]Arguments:[/bold cyan]
    [bright_white]oc12_token[/bright_white]: [cyan]obtenir un jeton d'accès[/cyan]
    [bright_white]oc12_logout[/bright_white]: [cyan]se déconnecter de l'application[/cyan]
    [bright_white]oc12_clients[/bright_white]: [cyan]obtenir les clients de l'entreprise[/cyan]
    [bright_white]oc12_collaborators[/bright_white]: [cyan]obtenir les employés /collaborateurs de l'entreprise[/cyan]
    [bright_white]oc12_contracts[/bright_white]: [cyan]obtenir les contrats de l'entreprise[/cyan]
    [bright_white]oc12_events[/bright_white]: [cyan]obtenir les évènements de l'entreprise[/cyan]
    [bright_white]oc12_locations[/bright_white]: [cyan]obtenir les localités des évènements de l'entreprise[/cyan]
    [bright_white]oc12_departments[/bright_white]: [cyan]obtenir les départements /services de l'entreprise[/cyan]
    [bright_white]oc12_roles[/bright_white]: [cyan]obtenir les rôles possibles des employés dans l'entreprise[/cyan]
    [bright_white]oc12_help[/bright_white]: [cyan]obtenir de l'aide (ce menu)[/cyan]

    [bold cyan]Tout modèle métier aura des commandes déclinées afin de permettre des vues filtrées.
    Les filtres concernent à la fois visualisation, mise à jour et suppression.[/bold cyan]
    Exemples:
    [bright_white]oc12_clients[/bright_white] [cyan]client_id=FJONIC35[/cyan]
    [bright_white]oc12_events[/bright_white] [cyan]commercial_id=aa123456789[/cyan]
    [bright_white]oc12_update_contract[/bright_white] [cyan]--contract_id ff555 remain_amount_to_pay=99.99 et status=signed[/cyan]
    [bright_white]oc12_delete_contract[/bright_white] [cyan]--contract_id xx55555[/cyan]
    [bright_white]oc12_contracts[/bright_white] [cyan]--help[/cyan]
    """)
    return True
