"""
Description: Toutes les commandes de lecture seule (de visualisation, "GET", etc)
"""
import re
import click
import json
from functools import wraps
from rich import print

try:
    from src.clients.console import ConsoleClient
except ModuleNotFoundError:
    from clients.console import ConsoleClient


class ApplicationHelpFormatter(click.HelpFormatter):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.indent_increment = 4
        self.max_width = None

    def write_heading(self, heading):
        print(f"{heading.strip()}")

    def write_text(self, text):
        print(f"{text.strip()}")

    def write(self, text):
        print(f"{text}")

click.Context.formatter_class = ApplicationHelpFormatter


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
def get_companies():
    """
    Description: commande dédiée à récupérer les entreprises clientes.
    """
    try:
        console_client = ConsoleClient()
        print(console_client.get_companies())
    except Exception:
        print("[bold red]Missing token[/bold red]")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_contracts(args):
    """
    [bold cyan]Description:[/bold cyan]
    Commande dédiée à récupérer les contrats de l'entreprise.
    En l'absence d'arguments, l'ensemble des contrats est renvoyé.

    [bold cyan]Arguments possibles:[/bold cyan]
    [bright_white]status[/bright_white]: on filtre les contrats payés ou non. Valeurs possibles: signed, unsigned, canceled
    [bright_white]full_amount_to_pay[/bright_white]: on filtre par montant à payer.
    [bright_white]remain_amount_to_pay[/bright_white]: on filtre par montant restant à payer.
    [bright_white]creation_date[/bright_white]: on filtre par date de création.

    [bold cyan]Exemples d'usage:[/bold cyan]
    [white]oc12_contracts status=signed[/white]
    [white]oc12_contracts remain_amount_to_pay=>0[/white]
    [white]oc12_contracts "status=signed et remain_amount_to_pay =>0"[/white]
    [white]oc12_contracts "creation_date>15-07-2023"[/white]
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClient()
        contracts = console_client.get_contracts(user_query_filters_args)
        if len(contracts) > 0:
            for element in contracts:
                print(element.get_dict())
            print("Pas d'autres contrats")
        else:
            print("Pas de contrats trouvés")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red] {error}")


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
