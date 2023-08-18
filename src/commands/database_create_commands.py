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
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.create_console import ConsoleClientForCreate
    from exceptions import exceptions


APP_DICT = language_bridge.LanguageBridge()


@click.command
def add_client():
    """
    Description:
	Dédiée à ajouter un client de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_client())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_collaborator():
    """
    Description: 
	Dédiée à ajouter un utilisateur /collaborateur de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_collaborator())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_company():
    """
    Description:
	Dédiée à ajouter une entreprise sans client, mais avec une localité nécessaire.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_company())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_contract():
    """
    Description:
	Dédiée à ajouter un contrat de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_contract())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_department():
    """
    Description:
	Dédiée à ajouter un département /service de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_department())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_event():
    """
    Description:
	Dédiée à ajouter un évènement organisés par l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_event())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_location():
    """
    Description:
	Dédiée à ajouter un localisation des évènements.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_location())
    except exceptions.LocationCustomIdAlReadyExists:
        pass
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])


@click.command
def add_role():
    """
    Description:
	Dédiée à ajouter un roles pour les utilisateurs /collaborateurs de l'entreprise.
    """
    try:
        console_client = ConsoleClientForCreate()
        print(console_client.add_role())
    except Exception as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])
