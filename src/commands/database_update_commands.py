"""
Description:
Toutes les commandes qui permettent les mises à jour
"""
import click
from termcolor import colored, cprint

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.update_console import ConsoleClientForUpdate
    from src.exceptions import exceptions
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.update_console import ConsoleClientForUpdate
    from exceptions import exceptions
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


def display_option(options):
    for option in options:
        cprint(colored(option), "yellow")


def check_if_partial_dict_valid(partial_dict):
    for key, value in partial_dict.items():
        try:
            if value is not None:
                eval(f"validators.is_{key}_valid")(value)
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["VALUE_UNEXPECTED"]
            printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]

    Dédiée à mettre à jour un client de l'entreprise avec 1 ou plusieurs options ci-dessous:

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]civility[/bright_white]: expected 'MR, MME, MLE, AUTRE'
    [bright_white]first_name[/bright_white]:
    [bright_white]last_name[/bright_white]:
    [bright_white]employee_role[/bright_white]:
    [bright_white]email[/bright_white]:
    [bright_white]telephone[/bright_white]:
    [bright_white]company_id[/bright_white]: expected is custom id you set (free chars string)
    [bright_white]commercial_contact[/bright_white]: expected is registration_number

    [bold cyan]Usage examples:[/bold cyan]
    Exemple usage:
    oc12_update_client --client_id=SRODAP37 telephone=0611882244
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
                if not expected_company or expected_company is None:
                    raise exceptions.CustomIdMatchNothingException()
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
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour un collaborateur de l'entreprise avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]username[/bright_white]:
    [bright_white]department[/bright_white]:
    [bright_white]role[/bright_white]:

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_collaborator --registration_number=ae123456789 username="Louloute Duck"
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
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def update_collaborator_password():
    """
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour le mot de passe d'un collaborateur de l'entreprise.
    Pas d'arguments attendus.
    La politique de mot de passe peut être consultée avec: oc12_info_collaborator_password.
    """
    try:
        console_client = ConsoleClientForUpdate()
        if console_client.update_collaborator_password():
            printer.print_message(
                "success", APP_DICT.get_appli_dictionnary()["PASSWORD_UPDATED"]
            )
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour une entreprise avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: filtre pour date de création (dans le système).
    [bright_white]date_debut_activite[/bright_white]: filtre pour date début activité.
    [bright_white]company_name[/bright_white]: filtre pour nom entreprise.
    [bright_white]company_registration_number[/bright_white]: filtre pour SIREN entreprise.
    [bright_white]company_subregistration_number[/bright_white]: filtre pour NIC entreprise.
    [bright_white]location_id[/bright_white]: filtre pour localité entreprise.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_company --company_id=660316COE company_name=ELORES
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
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour un contrat de l'entreprise avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]full_amount_to_pay[/bright_white]: filtre pour total à payer.
    [bright_white]remain_amount_to_pay[/bright_white]: filtre pour restant à payer.
    [bright_white]creation_date[/bright_white]: filtre pour date de création.
    [bright_white]status[/bright_white]: filtre pour statut.
    [bright_white]client_id[/bright_white]: filtre pour id client.
    [bright_white]collaborator_id[/bright_white]: filtre pour id collaborateur commercial.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_contract --contract_id=ax312 status=canceled
    """
    contract_dict = {}
    console = ConsoleClientForUpdate()
    try:
        contract_dict["contract_id"] = f"{contract_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
            except Exception:
                # exception avec le seul 'et' par exemple
                pass

            if k == "client_id":
                expected_client = console.app_view.get_clients_view().get_client(v)
                expected_client_id = expected_client.get_dict()["id"]
                contract_dict[k] = str(expected_client_id)
            elif k == "collaborator_id":
                expected_collaborator = (
                    console.app_view.get_collaborators_view().get_collaborator(v)
                )
                expected_collaborator_id = expected_collaborator.get_dict()["id"]
                contract_dict[k] = str(expected_collaborator_id)
            elif k == "remain_amount_to_pay":
                contract = console.app_view.get_contracts_view().get_contract(
                    contract_id
                )
                contract_dict["full_amount_to_pay"] = contract.full_amount_to_pay
            else:
                contract_dict[k] = str(v)
        if len(contract_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(contract_dict)
        console_client_return = console.update_contract(contract_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour un département /service de l'entreprise avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]name[/bright_white]: filtre pour nom département /service.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_department --department_id=DEVX name=OC12_DEVOPS
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
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour un évènement avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]title[/bright_white]: filtre pour titre.
    [bright_white]contract_id[/bright_white]: expected is custom id you set (free chars string)
    [bright_white]client_id[/bright_white]: expected is custom id you set (free chars string)
    [bright_white]collaborator_id[/bright_white]: expected is registration_number
    [bright_white]location_id[/bright_white]: expected is custom id you set (free chars string)
    [bright_white]event_start_date[/bright_white]: filtre pour date début évènement.
    [bright_white]event_end_date[/bright_white]: filtre pour date fin évènement.
    [bright_white]attendees[/bright_white]: filtre pour le nombre de participants attendus.
    [bright_white]notes[/bright_white]: filtre pour notes évènement.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_event --event_id=dkap520 notes="Penser à des batteries de secours."
    oc12_update_event --event_id=geg2021 collaborator_id=af123456789
    """
    console = ConsoleClientForUpdate()
    event_dict = {}
    try:
        event_dict["event_id"] = f"{event_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
            except Exception:
                # exception avec le seul 'et' par exemple
                pass

            if k == "client_id":
                expected_client = console.app_view.get_clients_view().get_client(v)
                expected_client_id = expected_client.get_dict()["id"]
                event_dict[k] = str(expected_client_id)
            elif k == "collaborator_id":
                if v == "None":
                    event_dict[k] = None
                else:
                    expected_collaborator = (
                        console.app_view.get_collaborators_view().get_collaborator(v)
                    )
                    expected_collaborator_id = expected_collaborator.get_dict()["id"]
                    event_dict[k] = str(expected_collaborator_id)
            elif k == "contract_id":
                expected_contract = console.app_view.get_contracts_view().get_contract(
                    v
                )
                expected_contract_id = expected_contract.get_dict()["id"]
                event_dict[k] = str(expected_contract_id)
            elif k == "location_id":
                expected_location = console.app_view.get_locations_view().get_location(
                    v
                )
                expected_location_id = expected_location.get_dict()["id"]
                event_dict[k] = str(expected_location_id)
            else:
                event_dict[k] = str(v)

        if len(event_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(event_dict)
        console_client_return = console.update_event(event_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.OnlySuportMemberCanBeAssignedToEventSupportException:
        message = APP_DICT.get_appli_dictionnary()[
            "ONLY_SUPPORT_SERVICE_MEMBER_CAN_BE_ASSIGNED_TO_EVENT_SUPPORT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour une localité avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]adresse[/bright_white]: filtre pour adresse
    [bright_white]complement_adresse[/bright_white]: filtre pour complément adresse
    [bright_white]code_postal[/bright_white]: filtre pour code_postal
    [bright_white]cedex[/bright_white]: filtre pour cedex
    [bright_white]ville[/bright_white]: filtre pour ville
    [bright_white]region[/bright_white]: filtre pour région
    [bright_white]pays[/bright_white]: filtre pour pays

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_location --location_id=csb41120 "complement_adresse=Allée du champ."
    """
    location_dict = {}
    try:
        location_dict["location_id"] = f"{location_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
                location_dict[k] = v
            except Exception:
                # exception avec le seul 'et' par exemple
                pass
        if len(location_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(location_dict)
        console_client_return = ConsoleClientForUpdate().update_location(location_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
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
    [bold cyan]Description:[/bold cyan]
    Dédiée à mettre à jour un roles pour les collaborateurs de l'entreprise
    avec 1 ou plusieurs options ci-dessous.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]name[/bright_white]: filtre pour nom du role

    [bold cyan]Usage examples:[/bold cyan]
    oc12_update_role --role_id=emp name=Employé
    """
    role_dict = {}
    try:
        role_dict["role_id"] = f"{role_id}"
        for arg in args:
            try:
                k, v = arg.split("=")
                role_dict[k] = v
            except Exception:
                # exception avec le seul 'et' par exemple
                pass
        if len(role_dict) == 1:
            raise exceptions.MissingUpdateParamException()
        check_if_partial_dict_valid(role_dict)
        console_client_return = ConsoleClientForUpdate().update_role(role_dict)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except NameError:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToClient:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CLIENT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
