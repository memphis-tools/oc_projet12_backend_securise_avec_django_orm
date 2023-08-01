"""
Description: Toutes les commandes qui permettent les suppressions
"""
import click
from rich import print
from termcolor import colored, cprint
try:
    from src.clients.update_console import ConsoleClientForUpdate
    from src.exceptions import exceptions
    from src.models import models
    from src.utils import utils
except ModuleNotFoundError:
    from clients.update_console import ConsoleClientForUpdate
    from exceptions import exceptions
    from models import models
    from utils import utils


def display_option(options):
    for option in options:
        cprint(colored(option), "yellow")


@click.command()
@click.option("--client_id", prompt=True, help=click.secho('client_id: Id du client (votre id customisé)', bg='blue', fg='white'))
# @click.option("--client_id", prompt=True, help=cprint(colored("client_id: Id du client (votre id customisé)"), "yellow"))
@click.argument('args',
    nargs=-1,
    type=str,
)
def update_client(client_id, args):
    """
    Description: commande dédiée à mettre à jour un client de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    civility: expected 'MR, MRS, MISS, OTHER'\n
    first_name\n
    last_name\n
    employee_role\n
    email\n
    telephone\n
    company_id: expected is custom id you set\n
    commercial_contact: expected is registration_number\n
    Exemple usage:
    'oc12_update_client --client_id az123456789 first_name="john" last_name="doe"'
    """
    client_dict = {}
    try:
        client_dict["client_id"] = f"{client_id}"
        for arg in args:
            k, v = arg.split("=")
            client_dict[k] = v
        if len(client_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client = ConsoleClientForUpdate().update_client(client_dict)
        # print(console_client.update_client())
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Client utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--registration_number", prompt=True, help="Matricule du collaborateur")
@click.argument('args',
    nargs=-1,
    type=str,
)
def update_collaborator():
    """
    Description:
    Commande dédiée à mettre à jour un collaborateur de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    username\n
    department\n
    role\n
    Exemple usage:
    'oc12_update_collaborator --registration_number ab123456789 role="DESIGNER"
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_collaborator())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Collaborateur utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def update_company():
    """
    Description:
    Commande dédiée à mettre à jour une entreprise avec 1 ou plusieurs options ci-dessous:\n
    company_name\n
    company_registration_number\n
    company_subregistration_number\n
    location_id\n
    Exemple usage:
    'oc12_update_company --company_id mtcx55124 company_subregistration_number="77785"
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_company())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Entreprise utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def update_contract():
    """
    Description:
    Commande dédiée à mettre à jour un contrat de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    full_amount_to_pay\n
    remain_amount_to_pay\n
    creation_date\n
    status\n
    client_id\n
    collaborator_id\n
    Exemple usage:
    'oc12_update_contract --contract_id c20z38 remain_amount_to_pay="66.55"
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_contract())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Contrat utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def update_department():
    """
    Description:
    Commande dédiée à mettre à jour un département /service de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    name\n
    Exemple usage:
    'oc12_update_department --department_id zz94 name="La boucle sur yvette"
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_department())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Service utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def update_event():
    """
    Description:
    Commande dédiée à mettre à jour un évènement avec 1 ou plusieurs options ci-dessous:\n
    title\n
    contract_id\n
    client_id\n
    collaborator_id\n
    location_id\n
    event_start_date\n
    event_end_date\n
    attendees\n
    notes\n
    Exemple usage:
    'oc12_update_event --event_id a89pz15 notes="Attention à la météo."
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_event())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Evenement utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
def update_location():
    """
    Description:
    Commande dédiée à mettre à jour une localité avec 1 ou plusieurs options ci-dessous:\n
    adresse\n
    complement_adresse\n
    code_postal\n
    ville\n
    pays\n
    Exemple usage:
    'oc12_update_location --location_id zp44250 complement_adresse="Allée du champ."
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_location())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Locatité utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")

@click.command
def update_role():
    """
    Description:
    Commande dédiée à mettre à jour un roles pour les collaborateurs de l'entreprise
    avec 1 ou plusieurs options ci-dessous:\n
    """
    try:
        console_client = ConsoleClientForUpdate()
        print(console_client.update_role())
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Role utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")
