"""
Description:
On fournit uniquement dédiée à une connexion initiale et direct de/par l'utilisateur.
"""
try:
    from src.controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )
    from src.controllers.database_read_controller import DatabaseReadController
    from src.settings import settings
except ModuleNotFoundError:
    from controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )
    from controllers.database_read_controller import DatabaseReadController
    from settings import settings


class AuthenticationView:
    """
    Description: une classe dédiée à servir les vues de l'application.
    """

    def __init__(self, user_login, user_pwd, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à la première connexion de l'utilisateur pour obtenir un token.
        Une fois qu'il aura obtenu le token, la session ouverte avec le SGBD sera basée sur le "ROLE".
        Le "ROLE" aura un mot de passe prévu par défaut.
        Toutes les opérations autres que "lecture, GET, etc" imposeront à l'utilisateur de saisir son mot de passe.
        """
        self.db_controller = DatabaseReadController()
        self.db_initializer = DatabaseInitializerController(db_name)
        self.engine, self.session = self.db_initializer.return_engine_and_session(
            user_login, user_pwd, "", db_name=db_name
        )

    def init_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: Dédié à aider au développement. On détruit et recrée les tables de la base de données.
        """
        self.db_initializer.init_db(self.engine)

    def reset_db(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: Dédié à aider au développement. On détruit les tables de la base de données.
        """
        self.db_initializer.reset_db(self.engine, db_name=db_name)

    def database_postinstall_tasks(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à mettre à jour les tables de la base de données après initialisation de l'application.
        """
        self.db_initializer.database_postinstall_tasks(db_name=db_name)

    def database_postinstall_alter_tables(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à forcer la mise à jour de valeurs par défaut de tables.
        """
        self.db_initializer.database_postinstall_alter_tables(db_name=db_name)

    def database_postinstall_add_default_collaborators(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Dédiée à créer des employés par défaut, utilisables sur chaque base.
        """
        self.db_initializer.database_postinstall_add_default_collaborators(db_name=db_name)
