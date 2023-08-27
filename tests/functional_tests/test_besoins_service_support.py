"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Support
"""
import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.clients.delete_console import ConsoleClientForDelete
    from src.clients.read_console import ConsoleClientForRead
    from src.clients.update_console import ConsoleClientForUpdate
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from clients.delete_console import ConsoleClientForDelete
    from clients.read_console import ConsoleClientForRead
    from clients.update_console import ConsoleClientForUpdate
    from exceptions import exceptions
    from settings import settings


def test_event_display_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_support_collaborator,
    dummy_event_partial_data_4
    ):
    """
    Description:
    Un membre du service Support doit pouvoir Filtrer l’affichage des événements, par exemple :
    afficher uniquement les événements qui lui sont attribués.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    collaborator_id = dummy_event_partial_data_4["collaborator_id"]
    console_client = ConsoleClientForRead(db_name=db_name)
    result = console_client.get_events((f'collaborator_id={collaborator_id}',))
    assert isinstance(result, list)


@pytest.mark.parametrize(
    "events_id",
    [
        "geg2022",
        "zawx235",
    ]
)
def test_event_update_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_support_collaborator_with_id_7,
    events_id
    ):
    """
    Description:
    Un membre du service Support doit pouvoir Mettre à jour les événements dont il est responsable.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    notes = "Some weird notes to test the event update from support collaborator sir."
    console_client = ConsoleClientForUpdate(db_name=db_name)
    custom_partial_dict = {
        "event_id": events_id,
        "notes": notes
    }
    result = console_client.update_event(custom_partial_dict=custom_partial_dict)
    assert isinstance(result, str)
