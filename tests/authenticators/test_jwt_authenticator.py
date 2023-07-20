"""
Description:
Test du authenticator type JWT de l'application.
"""
import os
import pytest
from time import sleep
from datetime import datetime, timedelta
import jwt

try:
    from src.controllers.authentication_controller import JwtController
    from src.commands import get_commands
    from src.settings import settings
except ModuleNotFoundError:
    from controllers.authentication_controller import JwtController
    from commands import get_commands
    from settings import settings


def test_get_token_with_unvalid_credentials(get_runner):
    """
    Description:
    Pour obtenir un token l'utilisateur doit fournir un "registration_number" valide.
    On tente de récupérer le jeton avec un un registration_number inexistant.
    """
    result = get_runner.invoke(get_commands.get_token, ["123456789AZ", "Gr@TStuff"])
    assert result.exit_code == 1
    assert f"{settings.PATH_APPLICATION_JWT_NAME}" not in os.environ


def test_get_token_with_valid_credentials(get_runner):
    """
    Description:
    Pour obtenir un token l'utilisateur doit fournir un "registration_number" valide.
    On tente de récupérer le jeton avec un un registration_number existant.
    """
    result = get_runner.invoke(get_commands.get_token, ["123456789A", "applepie94"])
    assert result.exit_code == 0
    assert os.environ[f"{settings.PATH_APPLICATION_JWT_NAME}"] != "None"


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
                "role": "itinérant",
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


def test_check_token_expiration_when_time_elapsed_valid(get_runner):
    """
    Description:
    Un token doit être révoqué après un délai spécifié dans le fichier settings.py.
    En deça du délai il doit être non révoqué.
    """
    result = get_runner.invoke(get_commands.get_token, ["123456789A", "applepie94"])
    jwt_controller = JwtController()
    revocation = jwt_controller.does_a_valid_token_exist()
    assert result.exit_code == 0
    assert revocation is True


def test_check_token_expiration_when_time_elapsed_not_valid(get_runner):
    """
    Description:
    Un token doit être révoqué après un délai spécifié dans le fichier settings.py.
    Au delà du délai il doit être non révoqué.
    """
    settings.PATH_APPLICATION_ENV_NAME = "TEST"
    settings.JWT_DURATION = 1
    settings.JWT_UNIT_DURATION = "seconds"

    result = get_runner.invoke(get_commands.get_token, ["123456789A", "applepie94"])
    sleep(2)
    jwt_controller = JwtController()
    revocation = jwt_controller.does_a_valid_token_exist()
    assert result.exit_code == 0
    assert revocation is False
