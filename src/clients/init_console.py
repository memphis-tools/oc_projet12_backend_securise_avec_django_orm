"""
Description:
Console dédiée aux initialisations (pas utilisée par utilisateur de l'application).
"""
import os
from rich import print

try:
    from src.external_datas import make_external_api_call_for_french_companies_sample
    from src.exceptions import exceptions
    from src.languages import language_bridge
    from src.printers import printer
    from src.settings import settings, logtail_handler
    from src.views.init_views import InitAppViews
except ModuleNotFoundError:
    from external_datas import make_external_api_call_for_french_companies_sample
    from exceptions import exceptions
    from languages import language_bridge
    from printers import printer
    from settings import settings, logtail_handler
    from views.init_views import InitAppViews


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


class InitAppliConsole:
    """
    Description:
    Classe dédiée à l'interfaçage entre les 'src/commands/generate_sample_commands.py' et un backend.
    """

    def __init__(self):
        """
        Description:
        On instancie la classe pour servir des méthodes en lién avec l'initialisation.
        """
        self.app_init_view = InitAppViews()

    def generate_companies_file(self):
        """
        Description:
        Dédiée à exécuter une requête à une API externe, içi des entreprises Françaises.
        La fonction appelée (generate_companies_file va renvoyer un booléen.
        """
        return (
            make_external_api_call_for_french_companies_sample.generate_companies_file()
        )

    def create_locations_based_on_compay_import(self, csv_filename):
        """
        Description:
        Appel de la méthode dédiée à lire un fichier .csv obtenu d'une API externe.
        L'API utilisée est celle rappelée en settings FR_COMPANIES_API_URL.
        Les données du fichier vont être assemblées de sorte à créér au tant de Localité que d'entreprises.
        On ne crée pas de doublons si une Localité existe déjà.
        """
        self.app_init_view.read_a_csv_file_and_return_data_as_json(csv_filename)
        return True

    def import_data_from_externals_api(self):
        """
        Description:
        Méthode appelée depuis 'src/commands/init_commands.py' après instanciation de la classe InitAppliConsole.
        """
        print(
            "External_API [bold yellow]recherche-entreprises.api.gouv.fr [/bold yellow]",
            end="",
        )
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["API_QUERYING_DATA"]
        )
        try:
            self.generate_companies_file()
            # puisque le fichier csv des entreprises est recrée, on va crée les localités, puis les entreprises
            self.create_locations_based_on_compay_import(
                csv_filename=settings.COMPANIES_EXPORT_FILE_PATH
            )
        except exceptions.ApiQueryFailedException:
            message = self.app_dict.get_appli_dictionnary()["API_QUERY_ACCESS_OR_QUERY_FAILED"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False
        print(
            "External_API [bold yellow]recherche-entreprises.api.gouv.fr [/bold yellow]",
            end="",
        )
        printer.print_message(
            "info",
            APP_DICT.get_appli_dictionnary()["API_QUERY_ACCESS_OR_QUERY_SUCCEEDED"],
        )
        return True

    def try_to_parse_a_possible_csv_file_for_companies(self):
        """
        Description:
        Appelée depuis 'src/commands/generate_sample_commands.py' après instanciation de la classe InitAppliConsole.
        """
        printer.print_message(
            "info",
            APP_DICT.get_appli_dictionnary()["SETTINGS_INTERNET_CONNECTION_DOWN"],
        )
        filename = settings.COMPANIES_EXPORT_FILE_PATH
        csv_file_exists = os.path.isfile(filename)
        csv_file_is_empty = bool(os.path.getsize(filename) == 0)
        csv_headers_list = settings.COMPANIES_CSV_HEADERS
        csv_headers_nb_chars = 0
        csv_headers_nb_commas = 0
        for header in csv_headers_list:
            csv_headers_nb_commas += 1
            for csv_header in header:
                csv_headers_nb_chars += 1
        try:
            csv_file_has_only_headers = bool(
                os.path.getsize(filename) == csv_headers_nb_chars + csv_headers_nb_commas
            )
            if not csv_file_exists or (
                csv_file_exists and (csv_file_is_empty or csv_file_has_only_headers)
            ):
                raise exceptions.MissingApiStaticFileException()
            return True
        except exceptions.MissingApiStaticFileException:
            settings_key = "SETTINGS_INTERNET_CONNECTION_DOWN_NO_FILES_TO_PARSE"
            message = self.app_dict.get_appli_dictionnary()[f"{settings_key}"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        return False
