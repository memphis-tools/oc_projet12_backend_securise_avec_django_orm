"""
Description:
Test de la vue pour l'authentification.
"""
import os
import pytest
import sqlalchemy
try:
    from src.views.views import AppViews
    from src.views.authentication_view import AuthenticationView
    from src.settings import settings
except ModuleNotFoundError:
    from views.views import AppViews
    from views.authentication_view import AuthenticationView
    from settings import settings


os.environ[f"{settings.PATH_APPLICATION_ENV_NAME}"] = "TEST"


def test_authentication_with_wrong_credentials():
    user_login = "ZZ123456789"
    user_pwd = "dummyOne"
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(sqlalchemy.exc.OperationalError):
        authentication_view = AuthenticationView(
            user_login, user_pwd, db_name
        ).init_db()
        assert "Collaborator or Department not found" in sqlalchemy.exc.ProgrammingError


def test_authentication_with_valid_credentials(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    dummy_payload_data = {
        "registration_number": "aa123456789",
        "username": "donald duck",
        "department": "oc12_commercial",
        "expiration": "2023-08-14 19:57:57.081336",
    }
    auth_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    clients = auth_view.get_clients_view().get_clients()
    assert len(clients) > 0


def test_db_initialization_with_nonadmin_credentials():
    user_login = "aa123456789"
    user_pwd = f"{settings.DEFAULT_NEW_COLLABORATOR_PASSWORD}"
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(sqlalchemy.exc.ProgrammingError):
        authentication_view = AuthenticationView(
            user_login, user_pwd, db_name
        ).init_db()
        assert "psycopg.errors.InsufficientPrivilege" in sqlalchemy.exc.ProgrammingError
