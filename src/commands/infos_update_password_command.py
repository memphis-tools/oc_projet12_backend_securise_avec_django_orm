"""
Description:
Toutes les commandes pour obtenir des infos sur les formats ou donnés attendues.
"""
import click
from rich import print

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.info_console import InformationConsoleClient
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.info_console import InformationConsoleClient


APP_DICT = language_bridge.LanguageBridge()


@click.command
def get_password_policy():
    """
    Description:
    Dédiée à obtenir la politique de mot de passe.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_password_policy()
    except Exception as error:
        printer.print_message("success", APP_DICT.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])
