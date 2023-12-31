"""
Description:
Test de la vue pour joindre les controleurs en mode lecture ("GET").
"""

try:
    from src.settings import settings
    from src.views.clients_view import ClientsView
    from src.views.collaborators_view import CollaboratorsView
    from src.views.contracts_view import ContractsView
    from src.controllers.database_read_controller import DatabaseReadController
    from src.views.events_view import EventsView
    from src.views.locations_view import LocationsView
    from src.views.roles_view import RolesView
    from src.views.crud_views.views import AppViews
    from src.controllers.jwt_controller import JwtController
    from src.controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )
except ModuleNotFoundError:
    from settings import settings
    from views.clients_view import ClientsView
    from views.collaborators_view import CollaboratorsView
    from views.contracts_view import ContractsView
    from controllers.database_read_controller import DatabaseReadController
    from views.events_view import EventsView
    from views.locations_view import LocationsView
    from views.roles_view import RolesView
    from views.crud_views.views import AppViews
    from controllers.jwt_controller import JwtController
    from controllers.database_initializer_controller import (
        DatabaseInitializerController,
    )


def test_get_clients_with_commercial_profile(
    get_valid_decoded_token_for_a_commercial_collaborator,
):
    result = JwtController().does_a_valid_token_exist()
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = ClientsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_clients(app_view.session)
    assert isinstance(result, list)


def test_get_clients_with_gestion_profile(
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    result = JwtController().does_a_valid_token_exist()
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = ClientsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_clients(app_view.session)
    assert isinstance(result, list)


def test_get_clients_with_support_profile(
    get_valid_decoded_token_for_a_support_collaborator,
):
    result = JwtController().does_a_valid_token_exist()
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = ClientsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_clients(app_view.session)
    assert isinstance(result, list)


def test_get_collaborators(
    mocker, get_valid_decoded_token_for_a_commercial_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    app_view = AppViews(db_name)
    db_initializer = DatabaseInitializerController(db_name)
    clients_view = CollaboratorsView(
        app_view.db_controller, db_initializer, app_view.session
    )
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_collaborators(app_view.session)
    assert isinstance(result, list)


def test_get_contracts(mocker, get_valid_decoded_token_for_a_commercial_collaborator):
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = ContractsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_contracts(app_view.session)
    assert isinstance(result, list)


def test_get_events(mocker, get_valid_decoded_token_for_a_commercial_collaborator):
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = EventsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_events(app_view.session)
    assert isinstance(result, list)


def test_get_locations(mocker, get_valid_decoded_token_for_a_commercial_collaborator):
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = LocationsView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_locations(app_view.session)
    assert isinstance(result, list)


def test_get_roles(mocker, get_valid_decoded_token_for_a_commercial_collaborator):
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients_view = RolesView(app_view.db_controller, app_view.session)
    database_get_controller = DatabaseReadController()
    result = database_get_controller.get_roles(app_view.session)
    assert isinstance(result, list)
