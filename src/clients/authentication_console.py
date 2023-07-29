"""
Description: console dédiée aux seules opérations de login et logout
"""
import sys
import maskpass
from rich import print
from rich.prompt import Prompt

try:
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator
except ModuleNotFoundError:
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner


class AuthenticationConsoleClient:
    """
    Description: la classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        try:
            registration_number = Prompt.ask("Matricule employé: ")
            password = maskpass.askpass(prompt="Mot de passe: ")
            self.app_view = AuthenticationView(registration_number, password)
            self.jwt_view = JwtView(self.app_view)
            return self.jwt_view.get_token(registration_number)
        except Exception:
            print("[bold red]Wrong credentials[/bold red]")

    @authentication_permission_decorator
    def logout(self):
        """
        Description: vue dédiée à se désauthentifier sur l'application.
        """
        self.jwt_view.logout()
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
