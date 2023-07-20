"""
Description: Client en mode console
"""
import sys
from functools import wraps
import maskpass
import jwt
import pyfiglet
from rich import print

try:
    from src.views.views import AppViews
    from srv.views.authentication_view import AuthenticationView
    from src.settings import settings
except ModuleNotFoundError:
    from views.views import AppViews
    from views.authentication_view import AuthenticationView
    from settings import settings


def permission_decorator(func):
    @wraps(func)
    def check_user_token(*args, **kwargs):
        try:
            if args[0].authentication_view.does_a_valid_token_exist():
                return func(*args, **kwargs)
            print("[bold red]Access forbidden without valid token[/bold red]")
            sys.exit(0)
        except jwt.exceptions.InvalidSignatureError:
            print("[bold red]Access forbidden without valid token[/bold red]")
            sys.exit(0)

    return check_user_token


class ConsoleClient:
    """
    Description: la classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        self.app_view = AppViews()
        self.authentication_view = AuthenticationView(self.app_view)
        print(pyfiglet.figlet_format(f"{settings.APP_FIGLET_TITLE}"))

    def init_db(self):
        """
        Description: vue dédiée à supprimer et recréer les tables de la base de données, à vide.
        """
        self.app_view.init_db()

    @permission_decorator
    def get_clients(self):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        return self.app_view.get_clients_view().get_clients()

    @permission_decorator
    def get_collaborators(self):
        """
        Description: vue dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        return self.app_view.get_collaborators_view().get_collaborators()

    @permission_decorator
    def get_contracts(self):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.app_view.get_contracts_view().get_contracts()

    @permission_decorator
    def get_departments(self):
        """
        Description: vue dédiée à obtenir les départements /services de l'entreprise.
        """
        return self.app_view.get_departments_view().get_departments()

    @permission_decorator
    def get_events(self):
        """
        Description: vue dédiée à obtenir les évènements de l'entreprise.
        """
        return self.app_view.get_events_view().get_events()

    @permission_decorator
    def get_locations(self):
        """
        Description: vue dédiée à obtenir les localisations des évènements de l'entreprise.
        """
        return self.app_view.get_locations_view().get_locations()

    @permission_decorator
    def get_roles(self):
        """
        Description: vue dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        return self.app_view.get_roles_view().get_roles()

    def get_token(self, registration_number="", password=""):
        """
        Description: vue dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
        """
        try:
            if registration_number == "" and password == "":
                registration_number = input("Matricule employé: ")
                password = maskpass.askpass()
            return self.authentication_view.get_token(registration_number, password)
        except Exception:
            print("[bold red]Wrong credentials[/bold red]")

    @permission_decorator
    def logout(self):
        """
        Description: vue dédiée à se désauthentifier sur l'application.
        """
        self.authentication_view.logout()
        print("[bold green]See you soon[/bold green]")
        print(
            f"""
            [cyan]
            Notice your token access has a {settings.JWT_DURATION} {settings.JWT_UNIT_DURATION} validity period.
            You can unset the {settings.PATH_APPLICATION_JWT_NAME} variable from your path if you want.
            [/cyan]
            """
        )
        sys.exit(0)
