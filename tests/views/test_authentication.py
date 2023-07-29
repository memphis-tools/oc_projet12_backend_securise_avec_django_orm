"""
Description:
Test de la vue pour l'authentification.
"""
import pytest
import jwt
import sqlalchemy

try:
    from src.settings import settings
    from src.views.views import AppViews
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
except ModuleNotFoundError:
    from settings import settings
    from views.views import AppViews
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView


def test_authentication_with_wrong_credentials():
    user_login = "ZZ123456789"
    user_pwd = "dummyOne"
    with pytest.raises(sqlalchemy.exc.OperationalError):
        authentication_view = AuthenticationView(user_login, user_pwd).init_db()
        assert "User or Department not found" in sqlalchemy.exc.ProgrammingError


def test_authentication_with_valid_credentials(get_runner, mocker):
    dummy_payload_data = {
        "registration_number": 'aa123456789',
        "username": 'donald duck',
        "department": 'oc12_commercial',
        "expiration": '2023-07-25 11:57:57.081336'
    }
    mocker.patch.object(JwtView, 'get_decoded_token', return_value=dummy_payload_data)
    auth_view = AppViews()
    clients = auth_view.get_clients_view().get_clients()
    assert len(clients) > 0


def test_db_initialization_with_nonadmin_credentials():
    user_login = "aa123456789"
    user_pwd = "applepie94"
    with pytest.raises(sqlalchemy.exc.ProgrammingError):
        authentication_view = AuthenticationView(user_login, user_pwd).init_db()
        assert "psycopg.errors.InsufficientPrivilege" in sqlalchemy.exc.ProgrammingError