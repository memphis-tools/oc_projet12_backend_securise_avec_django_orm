"""
Description: Toutes les commandes pour obtenir des infos sur les formats ou donnés attendues.
"""
import click
from rich import print

try:
    from src.clients.info_console import InformationConsoleClient
except ModuleNotFoundError:
    from clients.info_console import InformationConsoleClient


@click.command
def get_password_policy():
    """
    Description: commande dédiée à obtenir la politique de mot de passe.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_password_policy()
    except Exception as error:
        print(
            "[bold red]Erreur[/bold red] Absence de jeton. Executer 'oc12_token' pour en obtenir un."
        )
