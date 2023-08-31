"""
Description:
Toutes les commandes pour générer des échantillons de données à importer.
"""
import click

try:
    from src.clients import init_console
    from src.printers import printer
    from src.languages import language_bridge
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from clients import init_console
    from printers import printer
    from languages import language_bridge
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


@click.command
def generate_companies_sample():
    """
    Description:
    Commande dédiée à générer un fichier d'entreprises Françaises lambda.
    On exploite le retour en créeant les localités et les entreprises.
    """
    app_init_console = init_console.InitAppliConsole()
    if settings.INTERNET_CONNECTION is False:
        app_init_console.try_to_parse_a_possible_csv_file_for_companies
    else:
        try:
            app_init_console.generate_companies_file()
        except Exception:
            message = APP_DICT.get_appli_dictionnary()[
                "API_QUERY_ACCESS_OR_QUERY_FAILED"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
