"""
Description: Toutes les commandes dédiées à l'authentification
"""
import click
from rich import print

try:
    from src.clients.authentication_console import AuthenticationConsoleClient
except ModuleNotFoundError:
    from clients.authentication_console import AuthenticationConsoleClient


@click.command
def get_token():
    """
    Description: commande dédiée à se connecter à l'application.
    Le "registration_number" le nom de l'utilisateur /du rôle, en base.
    Si utilisateur existe et mot de passe est correct, un token est crée et retourné en stdout du terminal en cours.
    """
    authentication_client = AuthenticationConsoleClient()


@click.command
def logout():
    """
    Description: commande dédiée à se déconnecter à l'application.
    """
    authentication_client = AuthenticationConsoleClient()
    print(authentication_client.logout())
