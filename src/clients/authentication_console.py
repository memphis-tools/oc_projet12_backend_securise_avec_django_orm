"""
Description:
Console dédiée aux seules opérations de login et logout
"""
import sys
import maskpass
from rich import print
from rich.prompt import Prompt

try:
    from src.exceptions import exceptions
    from src.printers import printer
    from src.languages import language_bridge
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from exceptions import exceptions
    from printers import printer
    from languages import language_bridge
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView
    from settings import settings
    from utils import utils


class AuthenticationConsoleClient:
    """
    Description:
    Dédiée à l'usage d'un client en mode console.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        On instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        self.app_dict = language_bridge.LanguageBridge()
        utils.display_banner()
        try:
            registration_number = Prompt.ask("Matricule employé: ")
            password = maskpass.askpass(prompt="Mot de passe: ")
            self.app_view = AuthenticationView(registration_number, password, db_name)
            self.jwt_view = JwtView(self.app_view)
            return self.jwt_view.get_token(registration_number)
        except exceptions.AuthenticationCredentialsFailed:
            printer.print_message("error", self.app_dict.get_appli_dictionnary()['INVALID_CREDENTIALS_ERROR'])
        except Exception:
            printer.print_message("error", self.app_dict.get_appli_dictionnary()['MISSING_TOKEN_ERROR'])

    @utils.authentication_permission_decorator
    @staticmethod
    def logout(self):
        """
        Description:
        Dédiée à se désauthentifier sur l'application.
        """
        self.jwt_view.logout()
        printer.print_message("success", self.app_dict.get_appli_dictionnary()['LOGOUT_PROMPT_MESSAGE'])
        for i in range(4):
            to_prompt = f"LOGOUT_PROMPT_INFO_{i+1}"
            printer.print_message("info", self.app_dict.get_appli_dictionnary()[to_prompt])
            i += 1
        sys.exit(0)
