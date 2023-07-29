"""
Description: Toutes les commandes qui permettent les ajouts
"""
import click
from rich import print

try:
    from src.clients.create_console import ConsoleClientForCreate
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate


@click.command
def add_client():
    """
    Description: commande dédiée à ajouter un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_client())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_collaborator():
    """
    Description: commande dédiée à ajouter un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_collaborator())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_company():
    """
    Description: commande dédiée à ajouter une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_company())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_contract():
    """
    Description: commande dédiée à ajouter un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_contract())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_department():
    """
    Description: commande dédiée à ajouter un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_department())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_event():
    """
    Description: commande dédiée à ajouter un évènement organisés par l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_event())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_location():
    """
    Description: commande dédiée à ajouter un localisation des évènements.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_location())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def add_role():
    """
    Description: commande dédiée à ajouter un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_role())
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")
