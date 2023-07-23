"""
On fournit uniquement dédiée à une connexion initiale et direct de/par l'utilisateur.
"""
try:
    from src.controllers.database_initializer_controller import DatabaseInitializerController
    from src.controllers.database_read_controller import DatabaseReadController
except ModuleNotFoundError:
    from controllers.database_initializer_controller import DatabaseInitializerController
    from controllers.database_read_controller import DatabaseReadController


class AuthenticationView:
    """
    Description: une classe dédiée à servir les vues de l'application.
    """

    def __init__(self, user_login, user_pwd):
        """
        Description:
        Dédiée à la première connexion de l'utilisateur pour obtenir un token.
        Une fois qu'il aura obtenu le token, la session ouverte avec le SGBD sera basée sur le "ROLE".
        Le "ROLE" aura un mot de passe prévu par défaut.
        Toutes les opérations autres que "lecture, GET, etc" imposeront à l'utilisateur de saisir son mot de passe.
        """
        self.db_controller = DatabaseReadController()
        self.db_initializer = DatabaseInitializerController()
        self.engine, self.session = self.db_initializer.return_engine_and_session(user_login, user_pwd)

    def init_db(self):
        """
        Description: on va purger la base de données de tout enregistrement, puis la repeupler.
        Une fois la phase POC terminée on arretera le drop_all, et le create_all ne sera effectif qu'une fois.
        """
        self.db_initializer.init_db(self.engine)
