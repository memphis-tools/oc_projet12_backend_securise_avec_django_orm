"""
Description: Toutes les commandes qui permettent les ajouts
"""
import click
from rich import print

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.create_console import ConsoleClientForCreate
    from src.exceptions import exceptions
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.create_console import ConsoleClientForCreate
    from exceptions import exceptions
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


@click.command
def add_client():
    """
    Description:
    Dédiée à ajouter un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_client(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_collaborator():
    """
    Description:
    Dédiée à ajouter un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_collaborator(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CollaboratorAlreadyExistException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_ALREADY_EXISTS_"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_company():
    """
    Description:
    Dédiée à ajouter une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_company(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_contract():
    """
    Description:
    Dédiée à ajouter un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_contract(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ContractAlreadyExistException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_department():
    """
    Description:
    Dédiée à ajouter un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_department(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_event():
    """
    Description:
    Dédiée à ajouter un évènement organisés par l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_event(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        pass
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_location():
    """
    Description:
    Dédiée à ajouter un localisation des évènements.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_location(), bg="blue", fg="white")
    except exceptions.LocationCustomIdAlReadyExists:
        pass
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
def add_role():
    """
    Description:
    Dédiée à ajouter un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        click.secho(console_client.add_role(), bg="blue", fg="white")
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
