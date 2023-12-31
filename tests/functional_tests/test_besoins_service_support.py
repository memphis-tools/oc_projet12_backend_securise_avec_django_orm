"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Support
"""
import pytest

try:
    from src.clients.read_console import ConsoleClientForRead
    from src.clients.update_console import ConsoleClientForUpdate
    from src.settings import settings
except ModuleNotFoundError:
    from clients.read_console import ConsoleClientForRead
    from clients.update_console import ConsoleClientForUpdate
    from settings import settings


def test_event_display_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_support_collaborator,
    dummy_event_partial_data_4,
):
    """
    Description:
    Un membre du service Support doit pouvoir Filtrer l’affichage des événements, par exemple :
    afficher uniquement les événements qui lui sont attribués.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    collaborator_id = dummy_event_partial_data_4["collaborator_id"]
    console_client = ConsoleClientForRead(db_name=db_name)
    result = console_client.get_events((f"collaborator_id={collaborator_id}",))
    assert isinstance(result, list)


@pytest.mark.parametrize(
    "events_id",
    [
        "dkap520",
        "ay322",
    ],
)
def test_event_update_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_support_collaborator_with_id_8,
    events_id,
):
    """
    Description:
    Un membre du service Support doit pouvoir Mettre à jour les événements dont il est responsable.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    notes = "Some weird notes to test the event update from support collaborator sir."
    console_client = ConsoleClientForUpdate(db_name=db_name)
    custom_partial_dict = {"event_id": events_id, "notes": notes}
    result = console_client.update_event(custom_partial_dict=custom_partial_dict)
    assert isinstance(result, str)
