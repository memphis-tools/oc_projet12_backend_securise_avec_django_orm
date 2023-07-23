"""
Description:
Test de la vue pour joindre les controleurs en mode lecture ("GET").
"""
try:
    from src.views.clients_view import ClientsView
    from src.views.collaborators_view import CollaboratorsView
    from src.views.contracts_view import ContractsView
    from src.controllers.database_read_controller import DatabaseReadController
    from src.views.events_view import EventsView
    from src.views.locations_view import LocationsView
    from src.views.roles_view import RolesView
    from src.views.views import AppViews
except ModuleNotFoundError:
    from views.clients_view import ClientsView
    from views.collaborators_view import CollaboratorsView
    from views.contracts_view import ContractsView
    from controllers.database_read_controller import DatabaseReadController
    from views.events_view import EventsView
    from views.locations_view import LocationsView
    from views.roles_view import RolesView
    from views.views import AppViews


def test_get_clients():
    app_view = AppViews()
    clients_view = ClientsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_clients(app_view.session)
    assert type(result) == list


def test_get_collaborators():
    app_view = AppViews()
    clients_view = CollaboratorsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_collaborators(app_view.session)
    assert type(result) == list


def test_get_contracts():
    app_view = AppViews()
    clients_view = ContractsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_contracts(app_view.session)
    assert type(result) == list


def test_get_events():
    app_view = AppViews()
    clients_view = EventsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_events(app_view.session)
    assert type(result) == list


def test_get_locations():
    app_view = AppViews()
    clients_view = LocationsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_locations(app_view.session)
    assert type(result) == list


def test_get_roles():
    app_view = AppViews()
    clients_view = RolesView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_roles(app_view.session)
    assert type(result) == list
