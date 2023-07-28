"""
Description: Client en mode console
"""
import sys
from functools import wraps
import maskpass
import jwt
import pyfiglet
from rich import print
import pkg_resources

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

    def __init__(self):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews()
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
    def get_contracts(self):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.app_view.get_contracts_view().get_contracts()

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
