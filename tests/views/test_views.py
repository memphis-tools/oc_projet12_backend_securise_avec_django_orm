"""
Description:
Test de la vue "views.py", on test d'avoir la liste des données métier sans s'authentifier (sans token).
"""

import pytest

try:
    from src.commands import database_read_commands
    from src.exceptions import exceptions
    from src.settings import settings
    from src.views.views import AppViews
except ModuleNotFoundError:
    from commands import database_read_commands
    from exceptions import exceptions
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
def test_get_views(get_runner, command, get_valid_decoded_token_for_a_gestion_collaborator):
    database_read_commands
    result = get_runner.invoke(eval(f"database_read_commands.{command}"))
    assert result.exit_code == 0


@pytest.mark.parametrize("db_model", ["clients", "companies", "contracts", "departments", "roles", "locations"])
def test_get_client(db_model, get_valid_decoded_token_for_a_gestion_collaborator):
    app_view = AppViews(db_name = f"{settings.TEST_DATABASE_NAME}")
    db_model_view = eval(f"app_view.get_{db_model}_view().get_{db_model}()")
    assert len(db_model) > 0
