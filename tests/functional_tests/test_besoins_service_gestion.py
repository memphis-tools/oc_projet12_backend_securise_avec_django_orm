"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Gestion
"""
import os
import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.clients.delete_console import ConsoleClientForDelete
    from src.clients.read_console import ConsoleClientForRead
    from src.clients.update_console import ConsoleClientForUpdate
    from src.commands import database_read_commands
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from clients.delete_console import ConsoleClientForDelete
    from src.clients.read_console import ConsoleClientForRead
    from clients.update_console import ConsoleClientForUpdate
    from commands import database_read_commands
    from exceptions import exceptions
    from settings import settings


os.environ[f"{settings.PATH_APPLICATION_ENV_NAME}"] = "TEST"


def test_collaborator_manipulation(
    get_runner, set_a_test_env,
    dummy_collaborator_data_2,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_collaborator_partial_data
    ):
    """
    Description:
    Un membre du service Gestion doit pouvoir créer, mettre à jour et supprimer des collaborateurs dans le système CRM.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForCreate(db_name).add_collaborator(collaborator_attributes_dict=dummy_collaborator_data_2)
    print(result)
    assert isinstance(result, str)

    result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(custom_partial_dict=dummy_collaborator_partial_data)
    print(result)
    assert isinstance(result, str)

    matricule = dummy_collaborator_data_2["registration_number"]
    result = ConsoleClientForDelete(db_name=db_name).delete_collaborator(collaborator_custom_id=matricule)
    print(result)
    assert isinstance(result, str)


def test_contract_manipulation(
    get_runner, set_a_test_env,
    dummy_contract_data_2,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_contract_partial_data
    ):
    """
    Description:
    Un membre du service Gestion doit pouvoir créer et modifier tous les contrats.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    contract_custom_id = dummy_contract_data_2["contract_id"]

    result = ConsoleClientForCreate(db_name).add_contract(dummy_contract_data_2)
    assert isinstance(result, str)
    assert "Creation contract" in result

    result = ConsoleClientForUpdate(db_name=db_name).update_contract(custom_partial_dict=dummy_contract_partial_data)
    assert isinstance(result, str)
    assert "Update" in result

    result = ConsoleClientForDelete(db_name=db_name).delete_contract(contract_custom_id=contract_custom_id)
    assert isinstance(result, str)
    assert "Suppression" in result


def test_event_display_manipulation(
    get_runner, set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_event_partial_data_4
    ):
    """
    Description:
    Un membre du service Gestion doit pouvoir filtrer l’affichage des événements,
    par exemple : afficher tous les événements qui n’ont pas de « support » associé.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    console_client = ConsoleClientForRead(db_name=db_name)
    result = console_client.get_events(('collaborator_id=None',))
    assert isinstance(result, list)


def test_event_update_manipulation(
    get_runner, set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_event_partial_data_1,
    ):
    """
    Description:
    Un membre du service Gestion doit pouvoir modifier des événements (pour associer un collaborateur support à
    l’événement).
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_event(dummy_event_partial_data_1)
    assert isinstance(result, str)
    assert "Update" in result
