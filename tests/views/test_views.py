"""
Description:
Test de la vue "views.py", on test d'avoir la liste des données métier sans s'authentifier (sans token).
"""

import pytest

try:
    from src.commands import database_read_commands
    from src.settings import settings
    from src.views.views import AppViews
except ModuleNotFoundError:
    from commands import database_read_commands
    from settings import settings
    from views.views import AppViews


@pytest.mark.parametrize(
    "command",
    [
        "get_clients",
        "get_companies",
        "get_contracts",
        "get_departments",
        "get_events",
        "get_locations",
        "get_roles",
    ],
)
def test_get_views(
    get_runner, set_a_test_env, command, get_valid_decoded_token_for_a_gestion_collaborator
):
    """
    Description:
    Toutes les données métier doivent être accessibles en lecture seule par tout collaborateur de l'entreprise.
    Içi on vérifie que les 'vues' seront accessibles.
    """
    result = get_runner.invoke(eval(f"database_read_commands.{command}"))
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "db_model",
    ["clients", "companies", "contracts", "departments", "roles", "locations"],
)
def test_get_client(db_model, get_valid_decoded_token_for_a_gestion_collaborator):
    """
    Description:
    Toutes les données métier doivent être accessibles en lecture seule par tout collaborateur de l'entreprise.
    Içi on vérifie que les 'vues' renvoient du contenu.
    """
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    db_model_view = eval(f"app_view.get_{db_model}_view().get_{db_model}()")
    assert len(db_model) > 0
