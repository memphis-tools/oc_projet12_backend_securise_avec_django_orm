"""
Description:
Nous sommes dans un contexte de développement, sans bdd dédiée à l'environnement.
On purge tout enregistrement crée pendant la phase de test.
"""
import pytest
try:
    from src.clients.delete_console import ConsoleClientForDelete
except ModuleNotFoundError:
    from clients.delete_console import ConsoleClientForDelete


def test_delete_client_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForDelete().delete_client("dduck")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_company_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForDelete().delete_company("cal7778")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_contract_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForDelete().delete_contract("D9Z1")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_event_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForDelete().delete_event("FW971")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_location_view(get_runner, get_valid_decoded_token_for_a_commercial_collaborator):
    try:
        result = ConsoleClientForDelete().delete_location("CAL13540")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_role_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator):
    try:
        result = ConsoleClientForDelete().delete_role("driv")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_department_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator):
    try:
        result = ConsoleClientForDelete().delete_department("logist")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize("matricule", ["pp123456789", "qq123456789", "rr123456789"])
def test_delete_collaborator_view(get_runner, get_valid_decoded_token_for_a_gestion_collaborator, matricule):
    try:
        result = ConsoleClientForDelete().delete_collaborator(matricule)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)
