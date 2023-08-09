"""
Description: Client en mode console dédié à l'admin de l'application.
"""

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

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        self.app_view = AuthenticationView(
            user_login=f"{settings.ADMIN_LOGIN}",
            user_pwd=f"{settings.ADMIN_PASSWORD}",
            db_name=db_name
        )
        self.jwt_view = JwtView(self.app_view)

    def init_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: vue dédiée à supprimer et recréer les tables de la base de données, à vide.
        """
        self.app_view.init_db()

    def flush_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: vue dédiée à supprimer les tables de la base de données.
        """
        self.app_view.flush_db()
