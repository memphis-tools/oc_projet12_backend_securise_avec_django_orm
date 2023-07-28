import pytest
from click.testing import CliRunner
try:
    from src.settings import settings
    from src.views.jwt_view import JwtView
    from src.controllers.jwt_controller import JwtController
except ModuleNotFoundError:
    from settings import settings
    from views.jwt_view import JwtView
    from controllers.jwt_controller import JwtController


@pytest.fixture
def get_runner():
    settings.PATH_APPLICATION_ENV_NAME = "TEST"
    settings.JWT_DURATION = 1
    settings.JWT_UNIT_DURATION = "seconds"
    return CliRunner()


@pytest.fixture
def get_valid_decoded_token(mocker):
    dummy_payload_data = {
        "registration_number": 'aa123456789',
        "username": 'donald duck',
        "department": 'oc12_commercial',
        "expiration": '2023-07-28 18:57:57.081336'
    }
    mocker.patch('controllers.jwt_controller.JwtController.get_decoded_token', return_value=dummy_payload_data)
    mocker.patch.object(JwtController, 'does_a_valid_token_exist', return_value=True)
    mocker.patch.object(JwtView, 'get_decoded_token', return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_unvalid_decoded_token(mocker):
    dummy_payload_data = {
        "registration_number": 'Zaa123456789',
        "username": 'donald duck',
        "department": 'oc12_commercial',
        "expiration": '2018-07-25 11:57:57.081336'
    }
    mocker.patch('views.jwt_view.JwtView.get_decoded_token', return_value=dummy_payload_data)
    mocker.patch('controllers.jwt_controller.JwtController.get_decoded_token', return_value=dummy_payload_data)
    mocker.patch('authenticators.jwt_authenticator.JwtAuthenticator.get_decoded_token', return_value=dummy_payload_data))
    return dummy_payload_data
