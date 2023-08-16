"""
Description: Toutes les commandes de lecture seule (de visualisation, "GET", etc)
"""
import click
from rich import print

try:
    from src.clients.read_console import ConsoleClientForRead
except ModuleNotFoundError:
    from clients.read_console import ConsoleClientForRead


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
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_clients(args):
    """
    Description: commande dédiée à récupérer les clients de l'entreprise.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_clients(user_query_filters_args)
    except Exception as error:
        print(f"[bold red]Missing token[/bold red] {error}")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_collaborators(args):
    """
    Description: commande dédiée à récupérer les utilisateurs /collaborateurs de l'entreprise.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_collaborators(user_query_filters_args)
    except Exception:
        print("[bold red]Missing token[/bold red]")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_companies(args):
    """
    Description: commande dédiée à récupérer les entreprises clientes.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_companies(user_query_filters_args)
    except Exception as error:
        print(f"[bold red]Missing token[/bold red] {error}")


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
    [bright_white]status[/bright_white]: filtre pour statut. Valeurs possibles: signed, unsigned, canceled
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
        console_client = ConsoleClientForRead()
        console_client.get_contracts(user_query_filters_args)
    except Exception as error:
        print(f"[bold red]Missing token[/bold red] {error}")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_departments(args):
    """
    Description: commande dédiée à récupérer les départements /services de l'entreprise.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_departments(user_query_filters_args)
    except Exception:
        print("[bold red]Missing token[/bold red]")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_events(args):
    """
    [bold cyan]Description:[/bold cyan]
    Commande dédiée à récupérer les évènements organisés par l'entreprise.
    En l'absence d'arguments, l'ensemble des contrats est renvoyé.

    [bold cyan]Arguments possibles:[/bold cyan]
    [bright_white]event_id[/bright_white]: on filtre par evenementt id (le custom id).
    [bright_white]event_start_date[/bright_white]: on filtre par date de début.
    [bright_white]event_end_date[/bright_white]: on filtre par date de fin.
    [bright_white]location_id[/bright_white]: on filtre par localité id (le custom id).
    [bright_white]attendees[/bright_white]: on filtre par nombre de personnes attendues.
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]client_id[/bright_white]: on filtre par client id (le custom id).
    [bright_white]contract_id[/bright_white]: on filtre par contrat id (le custom id).
    [bright_white]collaborator_id[/bright_white]: on filtre par collaborateur id (le registration_number).

    [bold cyan]Exemples d'usage:[/bold cyan]
    [white]oc12_events "creation_date>15-07-2023"[/white]
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_events(user_query_filters_args)
    except Exception as error:
        print(f"[bold red]Missing token[/bold red] {error}")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_locations(args):
    """
    Description: commande dédiée à récupérer les localisations des évènements.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_locations(user_query_filters_args)
    except Exception:
        print("[bold red]Missing token[/bold red]")


@click.command
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_roles(args):
    """
    Description: commande dédiée à récupérer les roles des utilisateurs /collaborateurs de l'entreprise.
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_roles(user_query_filters_args)
    except Exception:
        print("[bold red]Missing token[/bold red]")
