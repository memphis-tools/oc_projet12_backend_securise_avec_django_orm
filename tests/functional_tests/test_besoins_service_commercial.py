"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Commercial
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


def test_client_creation_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Commercial doit pouvoir créer des clients (le client leur sera automatiquement associé).
    """
    pass


def test_client_update_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Commercial doit pouvoir mettre à jour les clients dont il est responsable.
    """
    pass


def test_contract_update_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Commercial doit pouvoir mettre à jour les contrats des clients dont il est responsable.
    """
    pass


def test_contract_display_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Commercial doit pouvoir filtrer l’affichage des contrats, par exemple :
    afficher tous les contrats qui ne sont pas encore signés, ou qui ne sont pas encore entièrement payés.
    """
    pass


def test_event_creation_manipulation(
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    ):
    """
    Description:
    Un membre du service Commercial doit pouvoir créer un événement pour un de leurs clients qui a signé un contrat.
    """
    pass
