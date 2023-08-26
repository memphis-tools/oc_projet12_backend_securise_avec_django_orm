"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Support
"""
import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.clients.delete_console import ConsoleClientForDelete
    from src.clients.update_console import ConsoleClientForUpdate
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from clients.delete_console import ConsoleClientForDelete
    from clients.update_console import ConsoleClientForUpdate
    from exceptions import exceptions
    from settings import settings


def test_event_display_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Support doit pouvoir Filtrer l’affichage des événements, par exemple :
    afficher uniquement les événements qui lui sont attribués.
    """
    pass


def test_event_update_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Support doit pouvoir Mettre à jour les événements dont il est responsable.
    """
    pass
