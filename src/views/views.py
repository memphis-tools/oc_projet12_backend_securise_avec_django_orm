"""
On fournit une vue dédiée à controler l'authentification et une autre qui permet d'atteindre les modèles.
"""
try:
    from src.controllers.initializer_controller import DatabaseInitializerController
    from src.controllers.get_controllers import DatabaseGETController
    from src.views.authentication_view import AuthenticationView
    from src.views.clients_view import ClientsView
    from src.views.collaborators_view import CollaboratorsView
    from src.views.contracts_view import ContractsView
    from src.views.departments_view import DepartmentsView
    from src.views.events_view import EventsView
    from src.views.locations_view import LocationsView
    from src.views.roles_view import RolesView
except ModuleNotFoundError:
    from controllers.initializer_controller import DatabaseInitializerController
    from controllers.get_controllers import DatabaseGETController
    from views.authentication_view import AuthenticationView
    from views.clients_view import ClientsView
    from views.collaborators_view import CollaboratorsView
    from views.contracts_view import ContractsView
    from views.departments_view import DepartmentsView
    from views.events_view import EventsView
    from views.locations_view import LocationsView
    from views.roles_view import RolesView


class AppViews:
    """
    Description: une classe dédiée à servir les vues de l'application.
    """

    def __init__(self):
        """
        Description: vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.db_controller = DatabaseGETController()
        self.db_initializer = DatabaseInitializerController()
        self.engine, self.session = self.db_initializer.return_engine_and_session()

    def init_db(self):
        """
        Description: on va purger la base de données de tout enregistrement, puis la repeupler.
        Une fois la phase POC terminée on arretera le drop_all, et le create_all ne sera effectif qu'une fois.
        """
        self.db_initializer.init_db(self.engine)

    def get_clients_view(self):
        """
        Description: obtention de la vue dédiée à gestion clients de l'entreprise.
        """
        clients_view = ClientsView(self.db_controller, self.session)
        return clients_view

    def get_collaborators_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les utilisateurs /collaborateurs de l'entreprise.
        """
        collaborators_view = CollaboratorsView(self.db_controller, self.session)
        return collaborators_view

    def get_contracts_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les contrats de l'entreprise.
        """
        contracts_view = ContractsView(self.db_controller, self.session)
        return contracts_view

    def get_departments_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les départements (directions) de l'entreprise.
        """
        departments_view = DepartmentsView(self.db_controller, self.session)
        return departments_view

    def get_locations_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les localisations des évènements.
        """
        locations_view = LocationsView(self.db_controller, self.session)
        return locations_view

    def get_events_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les évènements de l'entreprise.
        """
        events_view = EventsView(self.db_controller, self.session)
        return events_view

    def get_roles_view(self):
        """
        Description: vue dédiée à obtenir la vue sur les rôles prévus pour les collaborateurs de l'entreprise.
        """
        roles_view = RolesView(self.db_controller, self.session)
        return roles_view

    def get_authentication_view(self):
        """
        Description: vue dédiée à obtenir la vue sur pour les commandes d'authentification.
        """
        roles_view = AuthenticationView(self.db_controller, self.session)
        return roles_view
