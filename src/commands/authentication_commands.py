"""
Description: Toutes les commandes dédiées à l'authentification
"""
import click
from rich import print

try:
    from src.clients.console import ConsoleClient
except ModuleNotFoundError:
    from clients.console import ConsoleClient


@click.command
def get_token():
    """
    Description: commande dédiée à se connecter à l'application.
    Le "registration_number" (un "matricule de l'employé") de l'utilisateur est recherché en base.
    S'il existe, un token est crée et est retourné en stdout du terminal en cours.
    """
    console_client = ConsoleClient()
    console_client.get_token()


@click.command
def logout():
    """
    Description: commande dédiée à se déconnecter à l'application.
    """
    console_client = ConsoleClient()
    print(console_client.logout())
