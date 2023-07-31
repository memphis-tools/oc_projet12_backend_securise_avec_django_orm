"""
Description: Toutes les commandes qui permettent les suppressions
"""
import click
from rich import print

try:
    from src.clients.delete_console import ConsoleClientForDelete
    from src.exceptions import exceptions
except ModuleNotFoundError:
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions


@click.command
def delete_client():
    """
    Description: commande dédiée à supprimer un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_client())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Client utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_collaborator():
    """
    Description: commande dédiée à supprimer un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_collaborator())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Collaborateur utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_company():
    """
    Description: commande dédiée à supprimer une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_company())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Entreprise utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_contract():
    """
    Description: commande dédiée à supprimer un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_contract())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Contrat utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_department():
    """
    Description: commande dédiée à supprimer un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_department())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Service utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_event():
    """
    Description: commande dédiée à supprimer un évènement organisé par l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_event())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Evenement utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def delete_location():
    """
    Description: commande dédiée à supprimer une localité.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_location())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Locatité utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def delete_role():
    """
    Description: commande dédiée à supprimer un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_role())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Role utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")
