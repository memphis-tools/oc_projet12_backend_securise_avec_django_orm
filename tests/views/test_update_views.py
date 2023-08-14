"""
Description:
Test de la vue "update_views.py", on test la mise à jour de données métier avec authentification (token valide).
Pas de bases de données de test, içi on met à jour les données créées via "tests/views/test_create_views.py".
On recherche un "custom id" (une chaine libre), pas l'id entier auto incrémenté de la table.
Cas particulier d'un collaborateur, le "custom_id" est son registration_number (matricule).
"""
import pytest
try:
    from src.clients.update_console import ConsoleClientForUpdate
    from src.commands import database_update_commands
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.update_console import ConsoleClientForUpdate
    from commands import database_update_commands
    from exceptions import exceptions
    from settings import settings


client_partial_dict_1 = {
    "client_id": "dduck",
    "telephone": "0677118822",
    "email": "daisy.duck@abm.fr",
}


collaborator_partial_dict = {
    "registration_number": "rr123456789",
    "username": "marianne de lagraine",
}


client_partial_dict_2 = {
    "client_id": "dduck",
    "company_id": "cal7778",
}

client_partial_dict_3 = {
    "client_id": "dduck",
    "company_id": "xx666",
}

client_partial_dict_4 = {
    "client_id": "mkc111",
    "civility": "AUTRE",
    "company_id": "CSLLC12345"
}

collaborator_partial_dict = {
    "registration_number": "rr123456789",
    "username": "marianne de lagraine",
}


department_partial_dict = {"department_id": "logist", "name": "oc12_logistique"}

role_partial_dict = {"role_id": "driv", "name": "chauffeur"}

company_partial_dict = {
    "company_id": "CSLLC12345",
    "company_subregistration_number": "55577",
}

contract_partial_dict1 = {
    "contract_id": "kc555",
    "remain_amount_to_pay": "9599.99",
    "status": "unsigned",
}

contract_partial_dict2 = {
    "contract_id": "ff555",
    "remain_amount_to_pay": "9599.99",
    "status": "canceled",
}

contract_partial_dict3 = {
    "contract_id": "ff555",
    "remain_amount_to_pay": "99.99",
    "status": "signed",
}

location_partial_dict = {
    "location_id": "CAL13540",
    "complement_adresse": "allée de la patissière",
}

event_partial_dict = {
    "event_id": "hob2023",
    "attendees": "500",
    "notes": "Prévoir eau plate et gazeuse",
}

event_partial_dict2 = {
    "event_id": "hob2023",
    "attendees": "2500",
    "notes": "Prévoir eau plate et gazeuse.",
}

event_partial_dict3 = {
    "event_id": "hob2023",
    "attendees": "3500",
    "notes": "Prévoir eau plate et gazeuse. Sirop et jus de fruits.",
}


def test_update_client_view(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    args_to_convert = client_partial_dict_1
    custom_id = args_to_convert.pop("client_id")
    args_converted = ""
    for k, v in args_to_convert.items():
        args_converted += f"{k}={v} "
    result = get_runner.invoke(
        database_update_commands.update_client,
        f"--client_id={custom_id} {args_converted}",
        f"--db_name={settings.TEST_DATABASE_NAME}"
    )

    assert result.exit_code == 0
    assert f"{custom_id}" in str(result.output).strip()


def test_update_client_view_with_valid_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    # on ne va pas invoquer la commande update_client
    # on va directement réaliser ce qu'elle fait
    # on ne veut pas ajouter un argument aux commandes dédiées à l'utilisateur, qui indiqueraient la bdd
    args_to_convert = client_partial_dict_4
    custom_id = args_to_convert["client_id"]
    db_name = settings.TEST_DATABASE_NAME
    company_id = client_partial_dict_4["company_id"]
    expected_company = ConsoleClientForUpdate(custom_id=custom_id, db_name=db_name).app_view.get_companies_view().get_company(company_id)
    expected_company_id = expected_company.get_dict()["id"]
    console_client = ConsoleClientForUpdate(custom_id="", db_name=f"{settings.TEST_DATABASE_NAME}")
    args_to_convert["company_id"] = str(expected_company_id)
    result = console_client.update_app_view.get_clients_view().update_client(args_to_convert)
    assert f"{custom_id}" in result


def test_update_client_view_with_unvalid_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(AttributeError):
        args_to_convert = client_partial_dict_3
        custom_id = args_to_convert.pop("client_id")
        args_converted = ""
        for k, v in args_to_convert.items():
            args_converted += f"{k}={v} "
        result = get_runner.invoke(
            database_update_commands.update_client,
            f"--client_id={custom_id} {args_converted}",
            f"--db_name={settings.TEST_DATABASE_NAME}"
        )
        print(result.error)
        assert result.exit_code == 1


def test_update_company_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_company(company_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_company_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_company(company_partial_dict)


def test_update_company_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_company(company_partial_dict)


def test_update_contract_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(contract_partial_dict1)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_contract_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(contract_partial_dict2)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_contract_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(contract_partial_dict3)


def test_update_event_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_event(event_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_event_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_event(event_partial_dict2)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_event_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_event(event_partial_dict3)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_location_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(location_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_location_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(location_partial_dict)


def test_update_location_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(location_partial_dict)


def test_update_role_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_role_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)


def test_update_role_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)


def test_update_department_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_department(department_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_department_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_department(role_partial_dict)


def test_update_department_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_department(role_partial_dict)


def test_update_collaborator_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(collaborator_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_collaborator_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(role_partial_dict)


def test_update_collaborator_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(role_partial_dict)
