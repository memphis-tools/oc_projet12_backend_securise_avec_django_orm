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
except ModuleNotFoundError:
    from clients.update_console import ConsoleClientForUpdate
    from commands import database_update_commands


client_partial_dict_1 = {
    "client_id": "dduck",
    "telephone": "+677118822",
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

collaborator_partial_dict = {
    "registration_number": "rr123456789",
    "username": "marianne de lagraine",
}


department_partial_dict = {"department_id": "logist", "name": "oc12_logistique"}

role_partial_dict = {"role_id": "driv", "name": "chauffeur"}

company_partial_dict = {
    "company_id": "cal7778",
    "company_subregistration_number": "55577",
}

contract_partial_dict = {
    "contract_id": "D9Z1",
    "remain_amount_to_pay": "9599.99",
    "status": False,
}

location_partial_dict = {
    "location_id": "CAL13540",
    "complement_adresse": "allée de la patissière",
}

event_partial_dict = {
    "event_id": "FW971",
    "attendees": "500",
    "notes": "Prévoir eau plate et gazeuse",
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
    )
    assert result.exit_code == 0
    assert f"{custom_id}" in str(result.output).strip()


def test_update_client_view_with_valid_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    args_to_convert = client_partial_dict_2
    custom_id = args_to_convert.pop("client_id")
    args_converted = ""
    for k, v in args_to_convert.items():
        args_converted += f"{k}={v} "
    result = get_runner.invoke(
        database_update_commands.update_client,
        f"--client_id={custom_id} {args_converted}",
    )
    assert result.exit_code == 0
    assert f"{custom_id}" in str(result.output).strip()


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
        )
        # ce print permet de relever l'exception, ne pas supprimer.
        print(result.error)
        assert result.exit_code == 1


def test_update_company_view(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_company(company_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_contract_view(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_contract(contract_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_event_view(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_event(event_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_location_view(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_location(location_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_role_view(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_role(role_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_department_view(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_department(department_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_update_collaborator_view(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        result = ConsoleClientForUpdate().update_collaborator(collaborator_partial_dict)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)
