import pytest
from datetime import datetime, timedelta
from click.testing import CliRunner

try:
    from src.controllers.jwt_controller import JwtController
    from src.settings import settings
    from src.views.jwt_view import JwtView
except ModuleNotFoundError:
    from controllers.jwt_controller import JwtController
    from settings import settings
    from views.jwt_view import JwtView


@pytest.fixture
def get_runner():
    settings.PATH_APPLICATION_ENV_NAME = "TEST"
    settings.JWT_DURATION = 1
    settings.JWT_UNIT_DURATION = "seconds"
    return CliRunner()


@pytest.fixture
def get_valid_decoded_token_for_a_commercial_collaborator(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "aa123456789",
        "username": "donald duck",
        "department": "oc12_commercial",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_valid_decoded_token_for_a_commercial_collaborator_id_2(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "ab123456789",
        "username": "some duck",
        "department": "oc12_commercial",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_valid_decoded_token_for_a_gestion_collaborator(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "ac123456789",
        "username": "daisy duck",
        "department": "oc12_gestion",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_valid_decoded_token_for_a_support_collaborator(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "ae123456789",
        "username": "louloute duck",
        "department": "oc12_support",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_valid_decoded_token_for_a_support_collaborator_with_id_5(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "ae123456789",
        "username": "Aliénor Vichum",
        "department": "oc12_support",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_valid_decoded_token_for_a_support_collaborator_with_id_7(mocker):
    expiration = datetime.utcnow() + timedelta(minutes=1)
    dummy_payload_data = {
        "registration_number": "af123456789",
        "username": "Aliénor Vichum",
        "department": "oc12_support",
        "expiration": f'{expiration.strftime("%Y-%m-%d %H:%M:%S")}',
    }
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch.object(JwtController, "does_a_valid_token_exist", return_value=True)
    mocker.patch.object(JwtView, "get_decoded_token", return_value=dummy_payload_data)
    return dummy_payload_data


@pytest.fixture
def get_unvalid_decoded_token(mocker):
    dummy_payload_data = {
        "registration_number": "Zaa123456789",
        "username": "donald duck",
        "department": "oc12_commercial",
        "expiration": "2023-07-25 11:57:57.081336",
    }
    mocker.patch(
        "views.jwt_view.JwtView.get_decoded_token", return_value=dummy_payload_data
    )
    mocker.patch(
        "controllers.jwt_controller.JwtController.get_decoded_token",
        return_value=dummy_payload_data,
    )
    mocker.patch(
        "authenticators.jwt_authenticator.JwtAuthenticator.get_decoded_token",
        return_value=dummy_payload_data,
    )
    return dummy_payload_data


@pytest.fixture(scope="session", autouse=True)
def dummy_client_data(request):
    client = {
        "creation_date": "2023-07-14 09:05:10",
        "client_id": "dduck",
        "civility": "MME",
        "first_name": "daisy",
        "last_name": "duck",
        "employee_role": "logistic officer",
        "email": "d.duck@abm.fr",
        "telephone": "0655228844",
        "company_id": "1",
        "commercial_contact": "2",
    }
    return client


@pytest.fixture(scope="session", autouse=True)
def dummy_collaborator_data(request):
    collaborator = {
        "creation_date": "2023-07-14 09:05:10",
        "registration_number": "oo123456789",
        "username": "loulou duck",
        "department": "1",
        "role": "1",
    }
    return collaborator


@pytest.fixture(scope="session", autouse=True)
def dummy_collaborator_department_data(request):
    collaborator_department = {
        "creation_date": "2023-07-14 09:05:10",
        "department_id": "design",
        "name": "oc12_design",
    }
    return collaborator_department


@pytest.fixture(scope="session", autouse=True)
def dummy_collaborator_role_data(request):
    collaborator_role = {
        "creation_date": "2023-07-14 09:05:10",
        "role_id": "sec",
        "name": "SECRETARY",
    }
    return collaborator_role


@pytest.fixture(scope="session", autouse=True)
def dummy_company_data(request):
    company = {
        "creation_date": "2023-07-14 09:05:10",
        "company_id": "abm99998",
        "company_name": "A la bonne meule",
        "company_registration_number": "777666111",
        "company_subregistration_number": "99998",
        "location_id": "2",
    }
    return company


@pytest.fixture(scope="session", autouse=True)
def dummy_contract_data(request):
    contract = {
        "creation_date": "2023-07-14 09:05:10",
        "contract_id": "C9Z1",
        "full_amount_to_pay": "999.99",
        "remain_amount_to_pay": "999.99",
        "status": "unsigned",
        "client_id": "1",
        "collaborator_id": "2",
    }
    return contract


@pytest.fixture(scope="session", autouse=True)
def dummy_event_data(request):
    event = {
        "creation_date": "2023-07-14 09:05:10",
        "event_id": "EV971",
        "title": "What a Swing",
        "attendees": "2500",
        "notes": "Bla bla bla bla bla bla dummy bla. As expected anything bu a bla.",
        "event_start_date": "2023-07-15 20:00:00",
        "event_end_date": "2023-07-15 22:00:00",
        "client_id": "1",
        "contract_id": "1",
        "location_id": "2",
        "collaborator_id": "2",
    }
    return event


@pytest.fixture(scope="session", autouse=True)
def dummy_event_partial_data_1(request):
    event_partial_dict = {"event_id": "hob2023", "collaborator_id": 5}
    return event_partial_dict


@pytest.fixture(scope="session", autouse=True)
def dummy_event_partial_data_2(request):
    event_partial_dict = {
        "event_id": "hob2023",
        "attendees": "3500",
        "notes": "Prévoir eau plate et gazeuse. Sirop et jus de fruits.",
    }
    return event_partial_dict


@pytest.fixture(scope="session", autouse=True)
def dummy_event_partial_data_3(request):
    event_partial_dict = {
        "event_id": "geg2021",
        "attendees": "2500",
        "notes": "Prévoir eau plate et gazeuse.",
    }
    return event_partial_dict


@pytest.fixture(scope="session", autouse=True)
def dummy_location_data(request):
    location = {
        "creation_date": "2023-07-14 09:05:10",
        "location_id": "PL24250",
        "adresse": "3 rue de la tannerie",
        "complement_adresse": "La meule en bière",
        "code_postal": "24250",
        "ville": "Plurien",
        "pays": "France",
    }
    return location
