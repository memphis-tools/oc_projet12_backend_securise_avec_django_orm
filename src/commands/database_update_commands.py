"""
Description:
Toutes les commandes qui permettent les mises à jour
"""
import click
from rich import print
from termcolor import colored, cprint

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.read_console import ConsoleClientForRead
    from src.clients.update_console import ConsoleClientForUpdate
    from src.exceptions import exceptions
    from src.validators.data_syntax.fr import validators
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.read_console import ConsoleClientForRead
    from clients.update_console import ConsoleClientForUpdate
    from exceptions import exceptions
    from validators.data_syntax.fr import validators
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


def display_option(options):
    for option in options:
        cprint(colored(option), "yellow")


def check_if_partial_dict_valid(partial_dict):
    for key, value in partial_dict.items():
        try:
            if value != None:
                eval(f"validators.is_{key}_valid")(value)
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["VALUE_UNEXPECTED"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            break
    return True


@click.command()
@click.option("--client_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_client(client_id, args):
    """
    Description:
    Dédiée à mettre à jour un client de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    civility: expected 'MR, MME, MLE, AUTRE'\n
    first_name\n
    last_name\n
    employee_role\n
    email\n
    telephone\n
    company_id: expected is custom id you set (free chars string)\n
    commercial_contact: expected is registration_number\n
    Exemple usage:
    'oc12_update_client --client_id az123456789 first_name="john" last_name="doe"'
    """
    client_dict = {}
    try:
        client_dict["client_id"] = f"{client_id}"
        for arg in args:
            k, v = arg.split("=")
            if k == "company_id":
                expected_company = (
                    ConsoleClientForUpdate(custom_id="")
                    .app_view.get_companies_view()
                    .get_company(v)
                )
                expected_company_id = expected_company.get_dict()["id"]
                client_dict[k] = str(expected_company_id)
            else:
                client_dict[k] = str(v)
        if len(client_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(client_dict)
        console_client_return = ConsoleClientForUpdate().update_client(client_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()["COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--registration_number", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_collaborator(registration_number, args):
    """
    Description:
    Dédiée à mettre à jour un collaborateur de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
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
        check_if_partial_dict_valid(collaborator_dict)
        console_client_return = ConsoleClientForUpdate().update_collaborator(
            collaborator_dict
        )
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COLLABORATOR_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
def update_collaborator_password():
    """
    Description:
    Dédiée à mettre à jour le mot de passe d'un collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForUpdate()
        if console_client.update_collaborator_password():
            printer.print_message(
                "success", APP_DICT.get_appli_dictionnary()["PASSWORD_UPDATED"]
            )
    except exceptions.NewPasswordIsNotValidException:
        message = APP_DICT.get_appli_dictionnary()["NEW_PASSWORD_INVALID"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)

@click.command
@click.option("--company_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_company(company_id, args):
    """
    Description:
    Dédiée à mettre à jour une entreprise avec 1 ou plusieurs options ci-dessous:\n
    company_name\n
    company_registration_number\n
    company_subregistration_number\n
    location_id: expected is custom id you set (free chars string)\n
    Exemple usage:
    oc12_update_company --company_id mtcx55124 company_subregistration_number='77785'
    """
    company_dict = {}
    try:
        company_dict["company_id"] = f"{company_id}"
        for arg in args:
            k, v = arg.split("=")
            if k == "location_id":
                expected_location = (
                    ConsoleClientForUpdate()
                    .app_view.get_locations_view()
                    .get_location(v)
                )
                expected_location_id = expected_location.get_dict()["id"]
                company_dict[k] = str(expected_location_id)
            else:
                company_dict[k] = str(v)
        if len(company_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(company_dict)
        console_client_return = ConsoleClientForUpdate().update_company(company_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COMPANY_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--contract_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_contract(contract_id, args):
    """
    Description:
    Dédiée à mettre à jour un contrat de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
    full_amount_to_pay\n
    remain_amount_to_pay\n
    creation_date\n
    status\n
    client_id: expected is custom id you set (free chars string)\n
    collaborator_id: expected is registration_number\n
    Exemple usage:
    'oc12_update_contract --contract_id c20z38 remain_amount_to_pay="66.55"
    """
    contract_dict = {}
    console = ConsoleClientForRead()
    try:
        contract_dict["contract_id"] = f"{contract_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
            except:
                # exception avec le seul 'et' par exemple
                pass

            if k == "client_id":
                expected_client = (
                    console.app_view.get_clients_view().get_client(v)
                )
                expected_client_id = expected_client.get_dict()["id"]
                contract_dict[k] = str(expected_client_id)
            elif k == "collaborator_id":
                expected_collaborator = (
                    ConsoleClientForUpdate()
                    .app_view.get_collaborators_view()
                    .get_collaborator(v)
                )
                expected_collaborator_id = expected_collaborator.get_dict()["id"]
                contract_dict[k] = str(expected_collaborator_id)
            elif k == "remain_amount_to_pay":
                contract = (
                    console.app_view.get_contracts_view().get_contract(contract_id)
                )
                contract_dict["full_amount_to_pay"] = contract.full_amount_to_pay
            else:
                contract_dict[k] = str(v)
        if len(contract_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(contract_dict)
        console_client_return = ConsoleClientForUpdate().update_contract(contract_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()["COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--department_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_department(department_id, args):
    """
    Description:
    Dédiée à mettre à jour un département /service de l'entreprise avec 1 ou plusieurs options ci-dessous:\n
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
        check_if_partial_dict_valid(department_dict)
        console_client_return = ConsoleClientForUpdate().update_department(
            department_dict
        )
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_DEPARTMENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--event_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_event(event_id, args):
    """
    Description:
    Dédiée à mettre à jour un évènement avec 1 ou plusieurs options ci-dessous:\n
    title\n
    contract_id: expected is custom id you set (free chars string)\n
    client_id: expected is custom id you set (free chars string)\n
    collaborator_id: expected is registration_number\n
    location_id: expected is custom id you set (free chars string)\n
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
            try:
                k, v = arg.split("=")
            except:
                # exception avec le seul 'et' par exemple
                pass

            if k == "client_id":
                expected_client = (
                    ConsoleClientForUpdate().app_view.get_clients_view().get_client(v)
                )
                expected_client_id = expected_client.get_dict()["id"]
                event_dict[k] = str(expected_client_id)
            elif k == "collaborator_id":
                if v == 'None':
                    event_dict[k] = None
                else:
                    expected_collaborator = (
                        ConsoleClientForUpdate()
                        .app_view.get_collaborators_view()
                        .get_collaborator(v)
                    )
                    expected_collaborator_id = expected_collaborator.get_dict()["id"]
                    event_dict[k] = str(expected_collaborator_id)
            elif k == "contract_id":
                expected_contract = (
                    ConsoleClientForUpdate()
                    .app_view.get_contracts_view()
                    .get_contract(v)
                )
                expected_contract_id = expected_contract.get_dict()["id"]
                event_dict[k] = str(expected_contract_id)
            elif k == "location_id":
                expected_location = (
                    ConsoleClientForUpdate()
                    .app_view.get_locations_view()
                    .get_location(v)
                )
                expected_location_id = expected_location.get_dict()["id"]
                event_dict[k] = str(expected_location_id)
            else:
                event_dict[k] = str(v)

        if len(event_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(event_dict)
        console_client_return = ConsoleClientForUpdate().update_event(event_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_EVENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--location_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_location(location_id, args):
    """
    Description:
    Dédiée à mettre à jour une localité avec 1 ou plusieurs options ci-dessous:\n
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
        location_dict["location_id"] = f"{location_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
                location_dict[k] = v
            except:
                # exception avec le seul 'et' par exemple
                pass
        if len(location_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(location_dict)
        console_client_return = ConsoleClientForUpdate().update_location(location_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_LOCATION_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
@click.option("--role_id", prompt=True, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def update_role(role_id, args):
    """
    Description:
    Dédiée à mettre à jour un roles pour les collaborateurs de l'entreprise
    avec 1 ou plusieurs options ci-dessous:\n
    name\n
    Exemple usage:
    'oc12_update_department --role_id driv name="OC12_DRIVER"
    """
    role_dict = {}
    try:
        role_dict["role_id"] = f"{role_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
                role_dict[k] = v
            except:
                # exception avec le seul 'et' par exemple
                pass
        if len(role_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(role_dict)
        console_client_return = ConsoleClientForUpdate().update_role(role_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_ROLE_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
