"""
Description:
Toutes les commandes pour obtenir des infos sur les formats ou donnés attendues.
"""
import click

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.info_console import InformationConsoleClient
    from src.settings import logtail_handler, settings
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.info_console import InformationConsoleClient
    from settings import logtail_handler, settings


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


@click.command
def get_password_policy():
    """
    Description:
    Dédiée à obtenir la politique de mot de passe.
    """
    try:
        console_client = InformationConsoleClient()
        console_client.display_info_password_policy()
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
