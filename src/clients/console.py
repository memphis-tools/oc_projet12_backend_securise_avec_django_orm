"""
Description: Client en mode console
"""

try:
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
except ModuleNotFoundError:
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner


class ConsoleClient:
    """
    Description: la classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews(db_name)
        self.jwt_view = JwtView(self.app_view)

    @authentication_permission_decorator
    def get_clients(self):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        return self.app_view.get_clients_view().get_clients()

    @authentication_permission_decorator
    def get_collaborators(self):
        """
        Description: vue dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        return self.app_view.get_collaborators_view().get_collaborators()

    @authentication_permission_decorator
    def get_companies(self):
        """
        Description: vue dédiée à obtenir les entreprises clientes.
        """
        return self.app_view.get_companies_view().get_companies()

    @authentication_permission_decorator
    def get_contracts(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.app_view.get_contracts_view().get_contracts(user_query_filters_args)

    @authentication_permission_decorator
    def get_departments(self):
        """
        Description: vue dédiée à obtenir les départements /services de l'entreprise.
        """
        return self.app_view.get_departments_view().get_departments()

    @authentication_permission_decorator
    def get_events(self):
        """
        Description: vue dédiée à obtenir les évènements de l'entreprise.
        """
        return self.app_view.get_events_view().get_events()

    @authentication_permission_decorator
    def get_locations(self):
        """
        Description: vue dédiée à obtenir les localisations des évènements de l'entreprise.
        """
        return self.app_view.get_locations_view().get_locations()

    @authentication_permission_decorator
    def get_roles(self):
        """
        Description: vue dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        return self.app_view.get_roles_view().get_roles()
