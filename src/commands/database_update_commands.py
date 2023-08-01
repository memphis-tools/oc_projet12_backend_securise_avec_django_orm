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
@click.option("--client_id", prompt=True, help="")
# @click.option("--client_id", prompt=True, help=click.secho('client_id: Id du client (votre id customisé)', bg='blue', fg='white'))
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
        console_client_return = ConsoleClientForUpdate().update_client(client_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Client utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--registration_number", prompt=True, help="")
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
    collaborator_dict = {}
    try:
        collaborator_dict["registration_number"] = f"{registration_number}"
        for arg in args:
            k, v = arg.split("=")
            collaborator_dict[k] = v
        if len(collaborator_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_collaborator(collaborator_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Collaborateur utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--company_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
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
    company_dict = {}
    try:
        company_dict["company_id"] = f"{company_id}"
        for arg in args:
            k, v = arg.split("=")
            company_dict[k] = v
        if len(company_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_company(company_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Entreprise utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--contract_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
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
    contract_dict = {}
    try:
        contract_dict["contract_id"] = f"{contract_id}"
        for arg in args:
            k, v = arg.split("=")
            contract_dict[k] = v
        if len(contract_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_contract(contract_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Contrat utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--department_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
def update_department():
    """
    Description:
    Commande dédiée à mettre à jour un département /service de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    name\n
    Exemple usage:
    'oc12_update_department --department_id zz94 name="La boucle sur yvette"
    """
    department_dict = {}
    try:
        department_dict["department_id"] = f"{department_id}"
        for arg in args:
            k, v = arg.split("=")
            department_dict[k] = v
        if len(department_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_department(department_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Service utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--event_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
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
    event_dict = {}
    try:
        event_dict["event_id"] = f"{event_id}"
        for arg in args:
            k, v = arg.split("=")
            event_dict[k] = v
        if len(event_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_event(event_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Evenement utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--location_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
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
    location_dict = {}
    try:
        location_dict["event_id"] = f"{location_id}"
        for arg in args:
            k, v = arg.split("=")
            location_dict[k] = v
        if len(location_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_location(location_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Locatité utilisée[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")


@click.command
@click.option("--role_id", prompt=True, help="")
@click.argument('args',
    nargs=-1,
    type=str,
)
def update_role():
    """
    Description:
    Commande dédiée à mettre à jour un roles pour les collaborateurs de l'entreprise
    avec 1 ou plusieurs options ci-dessous:\n
    """
    role_dict = {}
    try:
        role_dict["event_id"] = f"{role_id}"
        for arg in args:
            k, v = arg.split("=")
            role_dict[k] = v
        if len(role_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        console_client_return = ConsoleClientForUpdate().update_role(role_dict)
        click.secho(console_client_return, bg='blue', fg='white')
    except exceptions.MissingUpdateParamException:
        print(f"[bold red]Aucuns arguments fournis[/bold red]")
    except exceptions.ForeignKeyDependyException as error:
        print(f"[bold red]Role utilisé[/bold red]: {error}")
    except Exception as error:
        print(f"[bold red]Missing token[/bold red]: {error}")
