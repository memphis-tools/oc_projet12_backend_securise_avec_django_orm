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
    print(
        """
[bold cyan]Commandes (usage aux seuls utilisateurs authentifiés):[/bold cyan]
[bright_white]oc12_init_application[/bright_white]: initialiser l'application
[bright_white]oc12_update_collaborator_password[/bright_white]: mise à jour mot de passe
[bright_white]oc12_token[/bright_white]: obtenir un jeton d'accès
[bright_white]oc12_logout[/bright_white]: se déconnecter de l'application
[bright_white]oc12_clients[/bright_white]: obtenir les clients de l'entreprise
[bright_white]oc12_collaborators[/bright_white]: [white]obtenir les employés de l'entreprise[/white]
[bright_white]oc12_contracts[/bright_white]: obtenir les contrats de l'entreprise
[bright_white]oc12_events[/bright_white]: obtenir les évènements de l'entreprise
[bright_white]oc12_locations[/bright_white]: obtenir les localités des évènements de l'entreprise
[bright_white]oc12_departments[/bright_white]: [white]obtenir les services de l'entreprise[/white]
[bright_white]oc12_roles[/bright_white]: obtenir les rôles possibles des employés dans l'entreprise
[bright_white]oc12_help[/bright_white]: obtenir de l'aide (ce menu)

[bold cyan]Aides supplémentaires (usage en accès libre):[/bold cyan]
[bright_white]oc12_info_collaborator_password[/bright_white]: afficher politique de mot de passe
[bright_white]oc12_info_metiers[/bright_white]: afficher les métiers possibles attendus pour un client
[bright_white]oc12_info_types_voies[/bright_white]: afficher les mots clefs attendus en complément d'adresse

[bold cyan]Tout modèle métier aura des commandes déclinées afin de permettre des vues filtrées.
Les filtres concernent à la fois visualisation, mise à jour et suppression.[/bold cyan]
Exemples:
oc12_clients [white]client_id=FJONIC35[/white]
oc12_events [white]commercial_id=aa123456789[/white]
oc12_update_[white]contract --contract_id ff555 remain_amount_to_pay=99.99 et status=signed[/white]
oc12_delete_contract --contract_id xx55555
oc12_contracts --help
    """
    )
    return True
