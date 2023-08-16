"""
Description: Toutes les commandes pour obtenir des infos sur les formats ou donnés attendues.
"""
import click
from rich import print
try:
    from src.controllers import infos_data_controller
except ModuleNotFoundError:
    from controllers import infos_data_controller


@click.command
def get_metiers():
    """
    Description: commande dédiée à récupérer les métiers attendus pour un client.
    """
    try:
        infos_data_controller.display_info_data_medium_window("metiers")
    except Exception as error:
        print(f"[bold red]Problème avec le fichier[/bold red]: {error}")


@click.command
def get_types_voies():
    """
    Description: commande dédiée à récupérer les types de voirs attendus pour une adresse.
    """
    try:
        infos_data_controller.display_info_data_thin_window("types_voies")
    except Exception as error:
        print(f"[bold red]Problème avec le fichier[/bold red]: {error}")
