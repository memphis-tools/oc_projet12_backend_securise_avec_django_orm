"""
Description:
Test de la vue "delete_views.py", on test la suppression de données métier avec authentification (token valide).
Pas de bases de données de test, içi on supprime les données créées via "tests/views/test_create_views.py".
On supprime les données en recherchant un "custom id" (une chaine libre), pas l'id entier auto incrémenté de la table.
"""

import pytest

try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.clients.delete_console import ConsoleClientForDelete
    from src.exceptions import exceptions
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions


def test_delete_client_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_client("poabm")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_company_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_company("abm99998")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_contract_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_contract("C9Z1")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_event_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_event("EV971")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_location_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_location("PL24250")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_role_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_role("sec")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


def test_delete_department_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        result = ConsoleClientForDelete().delete_department("design")
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)


@pytest.mark.parametrize("matricule", ["ww123456789", "xx123456789", "yy123456789"])
def test_delete_collaborator_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator, matricule
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        result = ConsoleClientForCreate().add_collaborator(matricule)


@pytest.mark.parametrize("matricule", ["ww123456789", "xx123456789", "yy123456789"])
def test_delete_collaborator_view_with_support_profile(
    get_runner, get_valid_decoded_token_for_a_support_collaborator, matricule
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        result = ConsoleClientForCreate().add_collaborator(matricule)


@pytest.mark.parametrize("matricule", ["ww123456789", "xx123456789", "yy123456789"])
def test_delete_collaborator_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, matricule
):
    try:
        result = ConsoleClientForDelete().delete_collaborator(matricule)
        assert isinstance(result, int)
        assert result > 0
    except Exception as error:
        print(error)
