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
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions


APP_DICT = language_bridge.LanguageBridge()


@click.command
def delete_client():
    """
    Description:
    Dédiée à supprimer un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_client())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CLIENT_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_collaborator():
    """
    Description:
    Dédiée à supprimer un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_collaborator())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COLLABORATOR_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_company():
    """
    Description:
    Dédiée à supprimer une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_company())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_COMPANY_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_contract():
    """
    Description:
    Dédiée à supprimer un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_contract())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_department():
    """
    Description:
    Dédiée à supprimer un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_department())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_DEPARTMENT_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_event():
    """
    Description:
    Dédiée à supprimer un évènement organisé par l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_event())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_EVENT_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_location():
    """
    Description:
    Dédiée à supprimer une localité.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_location())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error",
            APP_DICT.get_appli_dictionnary()["FOREIGNKEY_LOCATION_CAN_NOT_BE_DROP"],
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def delete_role():
    """
    Description:
    Dédiée à supprimer un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForDelete()
        print(console_client.delete_role())
    except exceptions.ForeignKeyDependyException as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["FOREIGNKEY_ROLE_CAN_NOT_BE_DROP"]
        )
    except Exception as error:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )
