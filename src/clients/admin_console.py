"""
Description: Client en mode console dédié à l'admin de l'application.
"""
import jwt

try:
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
    from src.settings import settings
except ModuleNotFoundError:
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView
    from settings import settings


class AdminConsoleClient:
    """
    Description: la classe dédiée à l'usage d'un client en mode console pour l'administrateur de l'application.
    """

    def __init__(self):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        self.app_view = AuthenticationView(user_login=f"{settings.ADMIN_LOGIN}", user_pwd=f"{settings.ADMIN_PASSWORD}")
        self.jwt_view = JwtView(self.app_view)

    def init_db(self):
        """
        Description: vue dédiée à supprimer et recréer les tables de la base de données, à vide.
        """
        self.app_view.init_db()
