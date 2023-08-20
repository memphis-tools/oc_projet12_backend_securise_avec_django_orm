"""
Description:
Toutes les commandes pour générer des échantillons de données à importer.
"""
import os
from os import path
import sys
import click
from rich import print

try:
    from src.clients import init_console
    from src.exceptions import exceptions
    from src.printers import printer
    from src.languages import language_bridge
    from src.settings import settings
except ModuleNotFoundError:
    from clients import init_console
    from exceptions import exceptions
    from printers import printer
    from languages import language_bridge
    from settings import settings


APP_DICT = language_bridge.LanguageBridge()


@click.command
def generate_companies_sample():
    """
    Description:
    Commande dédiée à générer un fichier d'entreprises Françaises lambda.
    On exploite le retour en créeant les localités et les entreprises.
    """
    app_init_console = init_console.InitAppliConsole()
    if settings.INTERNET_CONNECTION == False:
        app_init_console.try_to_parse_a_possible_csv_file_for_companies
    else:
        try:
            app_init_console.generate_companies_file()
        except Exception:
            printer.print_message("error", APP_DICT.get_appli_dictionnary()['API_QUERY_ACCESS_OR_QUERY_FAILED'])
