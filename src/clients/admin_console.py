"""
Description:
Client en mode console dédié à l'administrateur de l'application.
"""
import os
try:
    from src.printers import printer
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from printers import printer
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView
    from settings import settings
    from utils import utils


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
        db_name = utils.set_dev_database_as_default(db_name)
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
        self.app_view.init_db()

    def reset_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à supprimer les tables de la base de données.
        """
        db_name = utils.set_dev_database_as_default(db_name)
        self.app_view.reset_db(db_name=db_name)

    def database_postinstall_tasks(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à mettre à jour les tables de la base de données après initialisation de l'application.
        """
        db_name = utils.set_dev_database_as_default(db_name)
        self.app_view.database_postinstall_tasks(db_name=db_name)

    def database_postinstall_alter_tables(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à forcer la mise à jour de valeurs par défaut de tables.
        """
        db_name = utils.set_dev_database_as_default(db_name)
        self.app_view.database_postinstall_alter_tables(db_name=db_name)
