"""
Description:
Test de la vue "create_views.py", on test l'ajout de données métier avec authentification (token valide).
Attention à l'ordre. Exemple on ne peut pas créer un client tant que l'entreprise /company correspondante
n'est pas encore créée.
Plus largement, les tests de suppression doivent venir après les créations ci-dessous.
"""

import pytest
from datetime import datetime
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from exceptions import exceptions
    from settings import settings


# différents dictionnaires correspondants aux modèles
# noter qu'on ne créé /supprime qu'avec des objets peuplés au préalable
location_attributes_dict_1 = {
    "location_id": "PL24250",
    "adresse": "3 rue de la tannerie",
    "complement_adresse": "Voie de la bière",
    "code_postal": "24250",
    "cedex": "5",
    "ville": "Plurien",
    "pays": "France",
    "creation_date": f"{datetime.now()}",
}

location_attributes_dict_2 = {
    "location_id": "CAL13540",
    "adresse": "8 avenue des rillettes",
    "complement_adresse": "mur nord",
    "code_postal": "13540",
    "cedex": "0",
    "ville": "Gardanne",
    "pays": "France",
    "creation_date": f"{datetime.now()}",
}

location_attributes_dict_3 = {
    "location_id": "CAL13540",
    "adresse": "3 rue des rossignols",
    "complement_adresse": "Bourg de la reine",
    "code_postal": "78646",
    "cedex": "18",
    "ville": "Versailles",
    "pays": "France",
    "creation_date": f"{datetime.now()}",
}

company_attributes_dict_1 = {
    "company_id": "abm99998",
    "company_registration_number": "777666111",
    "company_subregistration_number": "99998",
    "company_name": "A la bonne meule",
    "activite_principale": "",
    "location_id": "2",
    "creation_date": f"{datetime.now()}",
}

company_attributes_dict_2 = {
    "company_id": "cal7778",
    "company_registration_number": "444111888",
    "company_subregistration_number": "22228",
    "company_name": "Calisson d'Aix",
    "activite_principale": "8230Z",
    "location_id": "1",
    "creation_date": f"{datetime.now()}",
}

company_attributes_dict_3 = {
    "company_id": "db45785",
    "company_registration_number": "462136723",
    "company_subregistration_number": "41237",
    "company_name": "Distributeurs Auto de Bretagne",
    "activite_principale": "5320Z",
    "location_id": "2",
    "creation_date": f"{datetime.now()}",
}

client_attributes_dict_1 = {
    "client_id": "poabm",
    "civility": "MR",
    "first_name": "john",
    "last_name": "doe",
    "employee_role": "press officer",
    "email": "j.doe@abm.fr",
    "telephone": "0611223344",
    "company_id": "1",
    "commercial_contact": "2",
    "creation_date": f"{datetime.now()}",
}

client_attributes_dict_2 = {
    "client_id": "dduck",
    "civility": "MME",
    "first_name": "daisy",
    "last_name": "duck",
    "employee_role": "logistic officer",
    "email": "d.duck@abm.fr",
    "telephone": "0655228844",
    "company_id": "1",
    "commercial_contact": "2",
    "creation_date": f"{datetime.now()}",
}

commercial_collaborator_attributes_dict_1 = {
    "registration_number": "ww123456789",
    "username": "dummy bigtooth",
    "department_id": "1",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

commercial_collaborator_attributes_dict_2 = {
    "registration_number": "pp123456789",
    "username": "dummy bigfoot",
    "department_id": "1",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

gestion_collaborator_attributes_dict_1 = {
    "registration_number": "xx123456789",
    "username": "dustin river",
    "department_id": "2",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

gestion_collaborator_attributes_dict_2 = {
    "registration_number": "qq123456789",
    "username": "myriam lake",
    "department_id": "2",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

support_collaborator_attributes_dict_1 = {
    "registration_number": "yy123456789",
    "username": "william summerland",
    "department_id": "3",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

support_collaborator_attributes_dict_2 = {
    "registration_number": "rr123456789",
    "username": "marianne dupin",
    "department_id": "3",
    "role_id": "2",
    "creation_date": f"{datetime.now()}",
}

contract_attributes_dict_1 = {
    "contract_id": "C9Z1",
    "full_amount_to_pay": "999.99",
    "remain_amount_to_pay": "999.99",
    "status": "unsigned",
    "client_id": "1",
    "creation_date": f"{datetime.now()}",
}

contract_attributes_dict_2 = {
    "contract_id": "D9Z1",
    "full_amount_to_pay": "9599.99",
    "remain_amount_to_pay": "932.44",
    "status": "signed",
    "client_id": "1",
    "creation_date": f"{datetime.now()}",
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
    "collaborator_id": "1",
    "creation_date": f"{datetime.now()}",
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
    "collaborator_id": "2",
    "creation_date": f"{datetime.now()}",
}

dpmt_attributes_dict_1 = {
    "department_id": "design",
    "name": "oc12_design",
    "creation_date": f"{datetime.now()}",
}

dpmt_attributes_dict_2 = {
    "department_id": "logist",
    "name": "oc12_logistic",
    "creation_date": f"{datetime.now()}",
}

role_attributes_dict_1 = {
    "role_id": "sec",
    "name": "SECRETARY",
    "creation_date": f"{datetime.now()}",
}

role_attributes_dict_2 = {
    "role_id": "driv",
    "name": "DRIVER",
    "creation_date": f"{datetime.now()}",
}


@pytest.mark.parametrize(
    "custom_dict",
    [
        commercial_collaborator_attributes_dict_1,
        gestion_collaborator_attributes_dict_2,
        support_collaborator_attributes_dict_1,
    ],
)
def test_add_collaborator_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict
):
    """
    Vérifier si un membre du service commercial peut ajouter un collaborateur.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_collaborator(custom_dict)


@pytest.mark.parametrize(
    "custom_dict",
    [
        commercial_collaborator_attributes_dict_1,
        gestion_collaborator_attributes_dict_2,
        support_collaborator_attributes_dict_1,
    ],
)
def test_add_collaborator_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter un collaborateur.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_collaborator(custom_dict)


@pytest.mark.parametrize(
    "custom_dict",
    [
        commercial_collaborator_attributes_dict_1,
        commercial_collaborator_attributes_dict_2,
        gestion_collaborator_attributes_dict_1,
        gestion_collaborator_attributes_dict_2,
        support_collaborator_attributes_dict_1,
        support_collaborator_attributes_dict_2,
    ],
)
def test_add_collaborator_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un collaborateur.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_collaborator(custom_dict)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_add_valid_location_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Vérifier si un membre du service commercial peut ajouter une localité valide.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_location(
            location_attributes_dict_1
        )
        assert isinstance(result, str)

    except Exception as error:
        print(error)


def test_add_unvalid_location_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Vérifier si un membre du service commercial peut ajouter une localité invalide.
    """
    with pytest.raises(exceptions.SuppliedDataNotMatchModel):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_location(
            location_attributes_dict_2
        )


@pytest.mark.parametrize(
    "custom_dict", [location_attributes_dict_1, location_attributes_dict_2]
)
def test_add_location_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter une localité.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_location(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [location_attributes_dict_1, location_attributes_dict_2]
)
def test_add_location_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter une localité.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_location(custom_dict)


def test_add_company_id_1_view_with_commercial_profile_with_valid_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Vérifier si un membre du service commercial peut ajouter une entreprise.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_company(company_attributes_dict_1)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_add_company_id_3_view_with_commercial_profile_with_valid_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Vérifier si un membre du service commercial peut ajouter une entreprise.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_company(company_attributes_dict_3)
        assert isinstance(result, str)

    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [company_attributes_dict_1, company_attributes_dict_2]
)
def test_add_company_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter une entreprise.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_company(custom_dict)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [company_attributes_dict_1, company_attributes_dict_2]
)
def test_add_company_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter une entreprise.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_company(custom_dict)
        assert isinstance(result, str)

    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [contract_attributes_dict_1, contract_attributes_dict_2]
)
def test_add_contract_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict
):
    """
    Vérifier si un membre du service commercial peut ajouter un contrat.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_collaborator(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [contract_attributes_dict_1, contract_attributes_dict_2]
)
def test_add_contract_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un contrat.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForCreate(db_name).add_contract(custom_dict)
    assert isinstance(result, str)


@pytest.mark.parametrize(
    "custom_dict", [contract_attributes_dict_1, contract_attributes_dict_2]
)
def test_add_contract_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter un contrat.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_contract(custom_dict)


def test_add_event_view_with_commercial_profile_when_assigned_contract(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Vérifier si un membre du service commercial peut ajouter un évènement.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_event(event_attributes_dict_1)
        assert isinstance(result, str)

    except Exception as error:
        print(error)


def test_add_event_view_with_commercial_profile_when_unassigned_contract(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Vérifier si un membre du service commercial peut ajouter un évènement
    Il ne peut pas créer un évènement pour un contrat qu'il n'a pas signé
    """
    with pytest.raises(exceptions.SupportCollaboratorIsNotAssignedToEvent):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_event(event_attributes_dict_2)


@pytest.mark.parametrize(
    "custom_dict", [event_attributes_dict_1, event_attributes_dict_2]
)
def test_add_event_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un évènement.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_event(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [event_attributes_dict_1, event_attributes_dict_2]
)
def test_add_event_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter un évènement.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_event(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [role_attributes_dict_1, role_attributes_dict_2]
)
def test_add_role_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un role.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_role(custom_dict)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [dpmt_attributes_dict_1, dpmt_attributes_dict_2]
)
def test_add_department_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un departement (service).
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_department(custom_dict)
        assert isinstance(result, str)

    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [dpmt_attributes_dict_1, dpmt_attributes_dict_2]
)
def test_add_department_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict
):
    """
    Vérifier si un membre du service commercial peut ajouter un departement (service).
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_department(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [client_attributes_dict_1, client_attributes_dict_2]
)
def test_add_client_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator, custom_dict
):
    """
    Vérifier si un membre du service commercial peut ajouter un client.
    """
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_client(custom_dict)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


@pytest.mark.parametrize(
    "custom_dict", [client_attributes_dict_1, client_attributes_dict_2]
)
def test_add_client_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, custom_dict
):
    """
    Vérifier si un membre du service gestion peut ajouter un client.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_client(custom_dict)


@pytest.mark.parametrize(
    "custom_dict", [client_attributes_dict_1, client_attributes_dict_2]
)
def test_add_client_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, custom_dict
):
    """
    Vérifier si un membre du service support peut ajouter un client.
    """
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForCreate(db_name).add_client(custom_dict)
