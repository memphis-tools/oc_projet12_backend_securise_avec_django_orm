"""
Description:
Test de la vue "create_views.py", on test l'ajout de données métier avec authentification (token valide).
Attention à l'ordre. Exemple on ne peut pas créer un client tant que l'entreprise /company correspondante
n'est pas encore créée.
Plus largement, les tests de suppression doivent venir après les créations ci-dessous.
"""

import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate


# différents dictionnaires correspondants aux modèles
# noter qu'on ne créé /supprime qu'avec des objets peuplés au préalable
location_attributes_dict_1 = {
    "location_id": "PL24250",
    "adresse": "3 rue de la tannerie",
    "complement_adresse": "La meule en bière",
    "code_postal": "24250",
    "ville": "Plurien",
    "pays": "France",
}

location_attributes_dict_2 = {
    "location_id": "CAL13540",
    "adresse": "8 avenue des rillettes",
    "complement_adresse": "Voie de l'amande",
    "code_postal": "13540",
    "ville": "Gardanne",
    "pays": "France",
}

company_attributes_dict_1 = {
    "company_id": "abm99998",
    "company_name": "A la bonne meule",
    "company_registration_number": "777666111",
    "company_subregistration_number": "99998",
    "location_id": "2"
}

company_attributes_dict_2 = {
    "company_id": "cal7778",
    "company_name": "Calisson d'Aix",
    "company_registration_number": "444111888",
    "company_subregistration_number": "22228",
    "location_id": "2"
}

client_attributes_dict_1 = {
    "client_id": "poabm",
    "civility": "MR",
    "first_name": "john",
    "last_name": "doe",
    "employee_role": "press officer",
    "email": "j.doe@abm.fr",
    "telephone": "+611223344",
    "company_id": "1",
    "commercial_contact": "2",
}

client_attributes_dict_2 = {
    "client_id": "dduck",
    "civility": "MRS",
    "first_name": "daisy",
    "last_name": "duck",
    "employee_role": "logistic officer",
    "email": "d.duck@abm.fr",
    "telephone": "+611223344",
    "company_id": "1",
    "commercial_contact": "2",
}

commercial_collaborator_attributes_dict_1 = {
    "registration_number":"ww123456789",
    "username": "dummy bigtooth",
    "department": "1",
    "role": "2",
}

commercial_collaborator_attributes_dict_2 = {
    "registration_number":"pp123456789",
    "username": "dummy bigfoot",
    "department": "1",
    "role": "2",
}

gestion_collaborator_attributes_dict_1 = {
    "registration_number":"xx123456789",
    "username": "dustin river",
    "department": "2",
    "role": "2",
}

gestion_collaborator_attributes_dict_2 = {
    "registration_number":"qq123456789",
    "username": "myriam lake",
    "department": "2",
    "role": "2",
}

support_collaborator_attributes_dict_1 = {
    "registration_number":"yy123456789",
    "username": "william summerland",
    "department": "3",
    "role": "2",
}

support_collaborator_attributes_dict_2 = {
    "registration_number":"rr123456789",
    "username": "marianne dupin",
    "department": "3",
    "role": "2",
}

contract_attributes_dict_1 = {
    "contract_id": "C9Z1",
    "full_amount_to_pay": "999.99",
    "remain_amount_to_pay": "999.99",
    "status": False,
    "client_id": "1",
    "collaborator_id": "2",
}

contract_attributes_dict_2 = {
    "contract_id": "D9Z1",
    "full_amount_to_pay": "9599.99",
    "remain_amount_to_pay": "932.44",
    "status": True,
    "client_id": "1",
    "collaborator_id": "2",
}

event_attributes_dict_1 = {
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

event_attributes_dict_2 = {
    "event_id": "FW971",
    "title": "Melody on night",
    "attendees": "1200",
    "notes": "Bla bla bla bla bla bla dummy bla. As expected anything but some more bla bla bla bla bla.",
    "event_start_date": "2023-07-23 19:30:00",
    "event_end_date": "2023-07-23 23:00:00",
    "client_id": "1",
    "contract_id": "1",
    "location_id": "2",
    "collaborator_id": "2"
}

department_attributes_dict_1 = {
    "department_id": "design",
    "name": "oc12_design"
}

department_attributes_dict_2 = {
    "department_id": "logist",
    "name": "oc12_logistic"
}

role_attributes_dict_1 = {
    "role_id": "sec",
    "name": "SECRETARY"
}

role_attributes_dict_2 = {
    "role_id": "driv",
    "name": "DRIVER"
}


@pytest.mark.parametrize(
    "custom_dict",
    [commercial_collaborator_attributes_dict_1, commercial_collaborator_attributes_dict_2]
)
def test_add_commercial_collaborator_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_collaborator(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [gestion_collaborator_attributes_dict_1, gestion_collaborator_attributes_dict_2]
)
def test_add_gestion_collaborator_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_collaborator(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [support_collaborator_attributes_dict_1, support_collaborator_attributes_dict_2]
)
def test_add_support_collaborator_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_collaborator(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [location_attributes_dict_1, location_attributes_dict_2]
)
def test_add_location_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_location(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [company_attributes_dict_1, company_attributes_dict_2]
)
def test_add_company_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_company(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [contract_attributes_dict_1, contract_attributes_dict_2]
)
def test_add_contract_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_contract(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [event_attributes_dict_1, event_attributes_dict_2]
)
def test_add_event_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_event(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [role_attributes_dict_1, role_attributes_dict_2]
)
def test_add_role_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_role(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [department_attributes_dict_1, department_attributes_dict_2]
)
def test_add_department_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_department(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict",
    [client_attributes_dict_1, client_attributes_dict_2]
)
def test_add_client_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict):
    try:
        result = ConsoleClientForCreate().add_client(custom_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)
