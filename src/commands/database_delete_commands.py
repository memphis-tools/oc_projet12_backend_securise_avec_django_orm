"""
Description:
Toutes les commandes qui permettent les suppressions
"""
import click
from rich import print

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.delete_console import ConsoleClientForDelete
    from src.exceptions import exceptions
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


@click.command
@click.option("--client_id", prompt=True, help="")
def delete_client():
    """
    Description:
    Dédiée à supprimer un client de l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_clients().delete_client(
            client_id
        )
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
@click.option("--collaborator_id", prompt=True, help="")
def delete_collaborator():
    """
    Description:
    Dédiée à supprimer un utilisateur /collaborateur de l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_collaborators().delete_collaborator(
            collaborator_id
        )
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
@click.option("--company_id", prompt=True, help="")
def delete_company():
    """
    Description:
    Dédiée à supprimer une entreprise sans client, mais avec une localité nécessaire.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_companies().delete_company(
            company_id
        )
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
@click.option("--contract_id", prompt=True, help="")
def delete_contract(contract_id):
    """
    Description:
    Dédiée à supprimer un contrat de l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_contracts_view().delete_contract(
            contract_id
        )
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
def delete_department():
    """
    Description:
    Dédiée à supprimer un département /service de l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_departments().delete_department(
            department_id
        )
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
@click.option("--event_id", prompt=True, help="")
def delete_event():
    """
    Description:
    Dédiée à supprimer un évènement organisé par l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_events().delete_event(
            department_id
        )
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
@click.option("--location_id", prompt=True, help="")
def delete_location():
    """
    Description:
    Dédiée à supprimer une localité.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_locations().delete_location(
            location_id
        )
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
@click.option("--role_id", prompt=True, help="")
def delete_role():
    """
    Description:
    Dédiée à supprimer un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_app_view.get_roles().delete_role(
            role_id
        )
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
