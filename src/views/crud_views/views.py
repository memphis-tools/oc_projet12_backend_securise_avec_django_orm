"""
On fournit une vue dédiée d'atteindre les modèles métier.
"""

try:
    from src.controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )
    from src.controllers.database_read_controller import DatabaseReadController
    from src.views.jwt_view import JwtView
    from src.views.clients_view import ClientsView
    from src.views.collaborators_view import CollaboratorsView
    from src.views.companies_view import CompaniesView
    from src.views.contracts_view import ContractsView
    from src.views.departments_view import DepartmentsView
    from src.views.events_view import EventsView
    from src.views.locations_view import LocationsView
    from src.views.roles_view import RolesView
    from src.settings import settings
except ModuleNotFoundError:
    from controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )
    from controllers.database_read_controller import DatabaseReadController
    from views.jwt_view import JwtView
    from views.clients_view import ClientsView
    from views.collaborators_view import CollaboratorsView
    from views.companies_view import CompaniesView
    from views.contracts_view import ContractsView
    from views.departments_view import DepartmentsView
    from views.events_view import EventsView
    from views.locations_view import LocationsView
    from views.roles_view import RolesView
    from settings import settings


class AppViews:
    """
    Description:
    Classe dédiée à servir les vues de l'application.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        Vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.db_controller = DatabaseReadController()
        self.db_initializer = DatabaseInitializerController(db_name=db_name)
        self.jwt_view = JwtView(self)
        decoded_token = self.jwt_view.get_decoded_token()
        # il faut charger le token de l'utilisateur, le décoder et le transmettre en clair
        # le "role" (exemple oc12_commercial) dans le token servira à créer la connexion à la bdd
        # il porte les permissions et chaque "department" (services, équipes) aura ses permissions.
        self.session = self.db_initializer.return_session(
            decoded_token=decoded_token, db_name=db_name
        )

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
        collaborators_view = CollaboratorsView(
            self.db_controller, self.db_initializer, self.session
        )
        return collaborators_view

    def get_companies_view(self):
        """
        Description: obtention de la vue dédiée à gestion des entreprises clientes de l'entreprise.
        """
        companies_view = CompaniesView(self.db_controller, self.session)
        return companies_view

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

    def get_jwt_view(self):
        """
        Description: vue dédiée à obtenir la vue sur pour les commandes liée au JWT token.
        """
        return self.jwt_view
