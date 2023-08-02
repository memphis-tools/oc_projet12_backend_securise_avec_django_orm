"""
Description:
Test de la vue "views.py", on test d'avoir la liste des données métier sans s'authentifier (sans token).
"""

import pytest

try:
    from src.commands import database_read_commands
except ModuleNotFoundError:
    from commands import database_read_commands


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
def test_get_views(get_runner, command):
    database_read_commands
    result = get_runner.invoke(eval(f"database_read_commands.{command}"))
    assert result.exit_code == 0
    assert "Missing token" in result.output
