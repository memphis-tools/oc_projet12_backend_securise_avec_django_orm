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
def delete_client():
    """
    Description:
    Dédiée à supprimer un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_client()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
def delete_collaborator():
    """
    Description:
    Dédiée à supprimer un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_collaborator()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COLLABORATOR_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


@click.command
def delete_company():
    """
    Description:
    Dédiée à supprimer une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_company()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COMPANY_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)



@click.command
def delete_contract():
    """
    Description:
    Dédiée à supprimer un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_contract()}")
    except exceptions.ForeignKeyDependyException:
        pass
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)



@click.command
def delete_department():
    """
    Description:
    Dédiée à supprimer un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_department()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_DEPARTMENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)



@click.command
def delete_event():
    """
    Description:
    Dédiée à supprimer un évènement organisé par l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_event()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_EVENT_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)



@click.command
def delete_location():
    """
    Description:
    Dédiée à supprimer une localité.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(f"Suppression: {console_client.delete_location()}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_LOCATION_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)



@click.command
def delete_role():
    """
    Description:
    Dédiée à supprimer un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        message = f"Suppression: {console_client.delete_role()}"
        print(message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            with logtail.context(company={ 'company_id': company_attributes_dict['company_id'] }):
                LOGGER.info(f"Company creation success: {company.company_id}")
    except exceptions.ForeignKeyDependyException as error:
        message = APP_DICT.get_appli_dictionnary()["FOREIGNKEY_ROLE_CAN_NOT_BE_DROP"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception as error:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
