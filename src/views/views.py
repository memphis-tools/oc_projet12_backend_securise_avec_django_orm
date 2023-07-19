"""
Une vue qui sera l'interface des fonctionnalités de l'application pour le "client" (par défaut en mode console).
"""


class AppViews:
    """
    Description: une classe dédiée à servir les vues de l'application.
    """

    def __init__(self, db_controller, db_initializer):
        """
        Description: vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.db_controller = db_controller
        self.db_initializer = db_initializer
        self.engine, self.session = db_initializer.return_engine_and_session()

    def init_db(self):
        """
        Description: on va purger la base de données de tout enregistrement, puis la repeupler.
        Une fois la phase POC terminée on arretera le drop_all, et le create_all ne sera effectif qu'une fois.
        """
        self.db_initializer.init_db(self.engine)

    def get_clients(self):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        return self.db_controller.get_clients(self.session)

    def get_collaborators(self):
        """
        Description: vue dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        return self.db_controller.get_collaborators(self.session)

    def get_contracts(self):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.db_controller.get_contracts(self.session)

    def get_departments(self):
        """
        Description: vue dédiée à obtenir les départements (directions) de l'entreprise.
        """
        return self.db_controller.get_departments(self.session)

    def get_locations(self):
        """
        Description: vue dédiée à obtenir les localisations des évènements.
        """
        return self.db_controller.get_locations(self.session)

    def get_events(self):
        """
        Description: vue dédiée à obtenir les évènements de l'entreprise.
        """
        return self.db_controller.get_events(self.session)

    def get_roles(self):
        """
        Description: vue dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        return self.db_controller.get_roles(self.session)
