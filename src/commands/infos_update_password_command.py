"""
Description: Toutes les commandes pour obtenir des infos sur les formats ou donnés attendues.
"""
import click
from rich import print
try:
    from src.controllers import infos_update_password_controller
except ModuleNotFoundError:
    from controllers import infos_update_password_controller


@click.command
def get_password_policy():
    """
    Description: commande dédiée à obtenir la politique de mot de passe.
    """
    try:
        infos_update_password_controller.display_info_password_policy()
    except Exception as error:
        print(f"[bold red]Problème avec la page d'aide[/bold red]: {error}")
