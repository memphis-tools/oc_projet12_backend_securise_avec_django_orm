"""
Description:
Test du authenticator type JWT de l'application.
"""
import os
import pytest
import psycopg
from time import sleep
from datetime import datetime, timedelta
import jwt
from rich import print

try:
    from src.views.authentication_view import AuthenticationView
    from src.views.jwt_view import JwtView
    import src.controllers.jwt_controller
    from src.controllers.jwt_controller import JwtController
    from src.commands import authentication_commands
    from src.settings import settings
    from src.authenticators.jwt_authenticator import JwtAuthenticator
except ModuleNotFoundError:
    from views.authentication_view import AuthenticationView
    from views.jwt_view import JwtView
    import controllers.jwt_controller
    from controllers.jwt_controller import JwtController
    from commands import authentication_commands
    from settings import settings
    from authenticators.jwt_authenticator import JwtAuthenticator


def test_get_token_with_unvalid_credentials():
    """
    Description:
    Pour obtenir un token l'utilisateur doit fournir un "registration_number" valide.
    On tente de récupérer le jeton avec un un registration_number inexistant.
    """
    registration_number = "xx123456789"
    password = "Gr@TStuff"
    with pytest.raises(Exception):
        app_view = AuthenticationView(registration_number, password)
        jwt_view = JwtView(app_view)
        result = jwt_view.get_token(registration_number)
        assert "User or Department not found" in f"{Exception}"


def test_get_token_with_valid_credentials(get_runner):
    """
    Description:
    Pour obtenir un token l'utilisateur doit fournir un "registration_number" valide.
    On tente de récupérer le jeton avec un un registration_number existant.
    """
    registration_number = "aa123456789"
    password = "applepie94"
    app_view = AuthenticationView(registration_number, password)
    jwt_view = JwtView(app_view)
    jwt_view.get_token(registration_number)


def test_random_jwt_token_against_application_for_invalid_signature_error(
    get_runner, mocker
):
    """
    Description:
    On va créer un jwt token avec une clef secrète quelconque. Ensuite on vérifie si on peut la décoder.
    """

    class MockResponse:
        @staticmethod
        def get_decoded_token():
            now = datetime.now()
            expiration = now + timedelta(seconds=2)
            payload_data = {
                "registration_number": "99999999",
                "username": "john doe",
                "department": "itinérant",
                "expiration": f"{expiration}",
            }
            token = jwt.encode(
                payload=payload_data,
                key="super_secret_key",
                algorithm=f"{settings.HASH_ALGORITHM}",
            )
            os.environ[f"{settings.PATH_APPLICATION_JWT_NAME}"] = token

    mocker.patch(
        "src.authenticators.jwt_authenticator.JwtAuthenticator.get_decoded_token",
        return_value=MockResponse.get_decoded_token(),
    )
    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        jwt_controller = JwtController()
        revocation = jwt_controller.does_a_valid_token_exist()


def test_check_token_expiration_when_time_elapsed_valid(get_runner, mocker):
    """
    Description:
    Un token doit être révoqué après un délai spécifié dans le fichier settings.py.
    En deça du délai il doit être non révoqué.
    L'attribut expiration indique la date et heure auxquelles le jeton sera révoqué.
    """
    expiration = datetime.utcnow() + timedelta(days=1)
    dummy_payload_data = {
        "registration_number": 'aa123456789',
        "username": 'donald duck',
        "department": 'oc12_commercial',
        "expiration": f'{expiration}'
    }

    revocation = JwtController.is_token_revoked("", dummy_payload_data)
    assert revocation is False


def test_check_token_expiration_when_time_elapsed_not_valid():
    """
    Description:
    Un token doit être révoqué après un délai spécifié dans le fichier settings.py.
    Au delà du délai il doit être non révoqué.
    """
    dummy_payload_data = {
        "registration_number": 'aa123456789',
        "username": 'donald duck',
        "department": 'oc12_commercial',
        "expiration": '2023-07-23 11:57:57.081336'
    }

    jwt_controller = JwtController()
    revocation = JwtController.is_token_revoked("", dummy_payload_data)
    assert revocation is True
