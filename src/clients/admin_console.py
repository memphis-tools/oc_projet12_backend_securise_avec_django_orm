"""
Description:
Client en mode console dédié à l'administrateur de l'application.
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
    Description:
    Dédiée à l'usage d'un client en mode console pour l'administrateur de l'application.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        self.app_view = AuthenticationView(
            user_login=f"{settings.ADMIN_LOGIN}",
            user_pwd=f"{settings.ADMIN_PASSWORD}",
            db_name=db_name,
        )
        self.jwt_view = JwtView(self.app_view)

    def init_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à supprimer et recréer les tables de la base de données, à vide.
        """
        app_view = AuthenticationView(
            user_login=f"{settings.ADMIN_LOGIN}",
            user_pwd=f"{settings.ADMIN_PASSWORD}",
            db_name=db_name,
        )
        app_view.init_db(db_name=db_name)

    def reset_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à supprimer les tables de la base de données.
        """
        self.app_view.reset_db(db_name=db_name)

    def database_postinstall_tasks(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à mettre à jour les tables de la base de données après initialisation de l'application.
        """
        self.app_view.database_postinstall_tasks(db_name=db_name)

    def database_postinstall_alter_tables(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à forcer la mise à jour de valeurs par défaut de tables.
        """
        self.app_view.database_postinstall_alter_tables(db_name=db_name)

    def database_postinstall_add_default_collaborators(
        self, db_name=f"{settings.DATABASE_NAME}"
    ):
        """
        Description:
        Dédiée à créer des employés par défaut, utilisables sur chaque base.
        """
        self.app_view.database_postinstall_add_default_collaborators(db_name=db_name)
