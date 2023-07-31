"""
Description:
Test de la vue "create_views.py", on test l'ajout de données métier avec authentification (token calide).
"""

import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate


location_attributes_dict = {
    "location_id": "PL24250",
    "adresse": "3 rue de la tannerie",
    "complement_adresse": "La meule en bière",
    "code_postal": "24250",
    "ville": "Plurien",
    "pays": "France",
}

company_attributes_dict = {
    "company_id": "abm99998",
    "company_name": "A la bonne meule",
    "company_registration_number": "777666111",
    "company_subregistration_number": "99998",
    "location_id": "1"
}

client_attributes_dict = {
    "client_id": "id",
    "civility": "MR",
    "first_name": "john",
    "last_name": "doe",
    "employee_role": "press officer",
    "email": "j.doe@abm.fr",
    "telephone": "+611223344",
    "company_id": "2"
}

commercial_collaborator_attributes_dict = {
    "registration_number":"ww123456789",
    "username": "dummy bigtooth",
    "department": "1",
    "role": "2",
}

gestion_collaborator_attributes_dict = {
    "registration_number":"xx123456789",
    "username": "dustin river",
    "department": "2",
    "role": "2",
}

support_collaborator_attributes_dict = {
    "registration_number":"yy123456789",
    "username": "william summerland",
    "department": "3",
    "role": "2",
}

contract_attributes_dict = {
    "contract_id": "C9Z1",
    "full_amount_to_pay": "999.99",
    "remain_amount_to_pay": "999.99",
    "status": False,
    "client_id": "1",
    "collaborator_id": "2",
}

event_attributes_dict = {
    "event_id": "EV971",
    "title": "What a Swing",
    "attendees": "2500",
    "notes": "Bla bla bla bla bla bla dummy bla. As expected anything bu a bla.",
    "event_start_date": "2023-07-15 20:00:00",
    "event_end_date": "2023-07-15 22:00:00",
    "client_id": "1",
    "contract_id": "1",
    "location_id": "2",
    "collaborator_id": "2"
}

role_attributes_dict = {
    "role_id": "sec",
    "name": "SECRETARY"
}


def test_add_collaborator_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator):
    try:
        result = ConsoleClientForCreate().add_collaborator(gestion_collaborator_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_client_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForCreate().add_client(client_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_company_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForCreate().add_company(company_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_contract_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForCreate().add_contract(contract_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_event_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForCreate().add_event(event_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_location_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForCreate().add_location(location_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_add_role_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator):
    try:
        result = ConsoleClientForCreate().add_role(role_attributes_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)
