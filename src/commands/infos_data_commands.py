"""
Description:
Toutes les commandes pour obtenir des infos sur les formats ou données attendues.
"""
import click
try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.info_console import InformationConsoleClient
    from src.settings import logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.info_console import InformationConsoleClient
    from settings import logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


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
        message = APP_DICT.get_appli_dictionnary()["MISSING_FILE"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)


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
        message = APP_DICT.get_appli_dictionnary()["MISSING_FILE"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error",message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        	LOGGER.error(message)
