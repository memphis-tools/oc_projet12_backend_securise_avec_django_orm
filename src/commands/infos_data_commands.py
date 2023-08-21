"""
Description:
Toutes les commandes pour obtenir des infos sur les formats ou données attendues.
"""
import click
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
def get_metiers():
    """
    Description:
        Dédiée à récupérer les métiers attendus pour un client.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_data_medium_window_for_metiers()
    except FileNotFoundError as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()["MISSING_FILE"])
    except Exception:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )


@click.command
def get_types_voies():
    """
    Description:
        Dédiée à récupérer les types de voirs attendus pour une adresse.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_data_medium_window_for_complement_adresse()
    except FileNotFoundError as error:
        printer.print_message("error", APP_DICT.get_appli_dictionnary()["MISSING_FILE"])
    except Exception:
        printer.print_message(
            "error", APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        )
