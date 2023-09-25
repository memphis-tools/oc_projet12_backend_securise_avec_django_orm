"""
Description:
Client en mode console, pour la lecture de données.
"""
import logtail

try:
    from src.languages import language_bridge
    from src.views.crud_views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.utils import utils
    from src.exceptions import exceptions
    from src.printers import printer
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from views.crud_views.views import AppViews
    from views.jwt_view import JwtView
    from utils import utils
    from exceptions import exceptions
    from printers import printer
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class ConsoleClientForRead:
    """
    Description:
    Classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        On instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name=db_name)
        self.app_dict = language_bridge.LanguageBridge()
        self.app_view = AppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        self.decoded_token = self.jwt_view.get_decoded_token()
        self.user_service = str(self.decoded_token["department"]).upper()
        self.registration_number = str(self.decoded_token["registration_number"])
        self.allowed_crud_tables = eval(f"settings.{self.user_service}_CRUD_TABLES")
        utils.display_banner(registration_number=self.registration_number)

    @utils.authentication_permission_decorator
    def get_clients(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les clients de l'entreprise.
        """
        try:
            return self.app_view.get_clients_view().get_clients(user_query_filters_args)
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_collaborators(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        try:
            return self.app_view.get_collaborators_view().get_collaborators(
                user_query_filters_args
            )
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_companies(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les entreprises clientes.
        """
        try:
            return self.app_view.get_companies_view().get_companies(
                user_query_filters_args
            )
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_contracts(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les contrats de l'entreprise.
        """
        try:
            return self.app_view.get_contracts_view().get_contracts(
                user_query_filters_args
            )
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_departments(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les départements /services de l'entreprise.
        """
        try:
            return self.app_view.get_departments_view().get_departments(
                user_query_filters_args
            )
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
                raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_events(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les évènements de l'entreprise.
        """
        try:
            return self.app_view.get_events_view().get_events(user_query_filters_args)
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_locations(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les localisations des évènements de l'entreprise.
        """
        try:
            return self.app_view.get_locations_view().get_locations(
                user_query_filters_args
            )
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()

    @utils.authentication_permission_decorator
    def get_roles(self, user_query_filters_args=""):
        """
        Description:
        Dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        try:
            return self.app_view.get_roles_view().get_roles(user_query_filters_args)
        except exceptions.QueryFailureException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "user_query_filters_args": user_query_filters_args,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.QueryFailureException()
        except exceptions.CustomIdMatchNothingException:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.QueryStructureException:
            message = self.app_dict.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            raise exceptions.QueryFailureException()
