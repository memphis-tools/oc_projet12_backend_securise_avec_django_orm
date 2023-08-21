"""
Description:
Client en mode console, pour la lecture de données.
"""
try:
    from src.languages import language_bridge
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils import utils


class ConsoleClientForRead:
    """
    Description:
    Classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name)
        self.app_dict = language_bridge.LanguageBridge()
        utils.display_banner()
        self.app_view = AppViews(db_name)
        self.jwt_view = JwtView(self.app_view)

    @utils.authentication_permission_decorator
    def get_clients(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        return self.app_view.get_clients_view().get_clients(user_query_filters_args)

    @utils.authentication_permission_decorator
    def get_collaborators(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        return self.app_view.get_collaborators_view().get_collaborators(
            user_query_filters_args
        )

    @utils.authentication_permission_decorator
    def get_companies(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les entreprises clientes.
        """
        return self.app_view.get_companies_view().get_companies(user_query_filters_args)

    @utils.authentication_permission_decorator
    def get_contracts(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.app_view.get_contracts_view().get_contracts(user_query_filters_args)

    @utils.authentication_permission_decorator
    def get_departments(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les départements /services de l'entreprise.
        """
        return self.app_view.get_departments_view().get_departments(
            user_query_filters_args
        )

    @utils.authentication_permission_decorator
    def get_events(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les évènements de l'entreprise.
        """
        return self.app_view.get_events_view().get_events(user_query_filters_args)

    @utils.authentication_permission_decorator
    def get_locations(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les localisations des évènements de l'entreprise.
        """
        return self.app_view.get_locations_view().get_locations(user_query_filters_args)

    @utils.authentication_permission_decorator
    def get_roles(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        return self.app_view.get_roles_view().get_roles(user_query_filters_args)
