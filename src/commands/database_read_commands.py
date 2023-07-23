"""
Description: Toutes les commandes de lecture seule (de visualisation, "GET", etc)
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
    try:
        console_client = ConsoleClient()
        print(console_client.get_clients())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_collaborators():
    """
    Description: commande dédiée à récupérer les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_collaborators())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_contracts():
    """
    Description: commande dédiée à récupérer les contrats de l'entreprise.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_contracts())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_departments():
    """
    Description: commande dédiée à récupérer les départements /services de l'entreprise.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_departments())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_events():
    """
    Description: commande dédiée à récupérer les évènements organisés par l'entreprise.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_events())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_locations():
    """
    Description: commande dédiée à récupérer les localisations des évènements.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_locations())
    except Exception:
        print("[bold red]Missing token[/bold red]")

@click.command
def get_roles():
    """
    Description: commande dédiée à récupérer les roles des utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_roles())
    except Exception:
        print("[bold red]Missing token[/bold red]")
