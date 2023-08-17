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
def get_metiers():
    """
    Description: commande dédiée à récupérer les métiers attendus pour un client.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_data_medium_window_for_metiers()
    except FileNotFoundError as error:
        print(f"[bold red]Problème avec le fichier[/bold red]: {error}")
    except Exception:
        print(
            "[bold red]Erreur[/bold red] Absence de jeton. Executer 'oc12_token' pour en obtenir un."
        )


@click.command
def get_types_voies():
    """
    Description: commande dédiée à récupérer les types de voirs attendus pour une adresse.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_data_medium_window_for_complement_adresse()
    except FileNotFoundError as error:
        print(f"[bold red]Problème avec le fichier[/bold red]: {error}")
    except Exception:
        print(
            "[bold red]Erreur[/bold red] Absence de jeton. Executer 'oc12_token' pour en obtenir un."
        )
