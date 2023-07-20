"""
Description: Toutes les commandes "GET" /de visualisation
"""
import click
from rich import print

try:
    from src.clients.console import ConsoleClient
except ModuleNotFoundError:
    from clients.console import ConsoleClient


@click.command
def get_clients():
    """
    Description: commande dédiée à récupérer les clients de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_clients())


@click.command
def get_collaborators():
    """
    Description: commande dédiée à récupérer les utilisateurs /collaborateurs de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_collaborators())


@click.command
def get_contracts():
    """
    Description: commande dédiée à récupérer les contrats de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_contracts())


@click.command
def get_departments():
    """
    Description: commande dédiée à récupérer les départements /services de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_departments())


@click.command
def get_events():
    """
    Description: commande dédiée à récupérer les évènements organisés par l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_events())


@click.command
def get_locations():
    """
    Description: commande dédiée à récupérer les localisations des évènements.
    """
    console_client = ConsoleClient()
    print(console_client.get_locations())


@click.command
def get_roles():
    """
    Description: commande dédiée à récupérer les roles des utilisateurs /collaborateurs de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.get_roles())


@click.command
@click.argument("registration_number")
@click.argument("password")
def get_token(registration_number, password):
    """
    Description: commande dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
    """
    console_client = ConsoleClient()
    token = console_client.authentication_view.get_token(registration_number, password)
