"""
Description: console dédiée aux commandes infos
"""
from rich import print

try:
    from src.controllers.infos_update_password_controller import (
        display_info_password_policy,
    )
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
except ModuleNotFoundError:
    from controllers.infos_update_password_controller import (
        display_info_password_policy,
    )
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner
    from views.views import AppViews
    from views.jwt_view import JwtView


class InformationConsoleClient:
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
    def display_info_password_policy(self):
        """
        Description:
        Retourner la politique de mot de passe
        """
        try:
            display_info_password_policy()
        except Exception as error:
            print(
                "[bold red]Erreur[/bold red] Absence de jeton."
            )
