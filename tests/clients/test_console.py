"""
Description:
Test du client en mode console de l'application.
"""

try:
    from src.commands import database_read_commands
except ModuleNotFoundError:
    from commands import database_read_commands


def test_get_clients(get_runner):
    result = get_runner.invoke(database_read_commands.get_clients)
    assert result.exit_code == 0


def test_get_collaborators(get_runner):
    result = get_runner.invoke(database_read_commands.get_collaborators)
    assert result.exit_code == 0


def test_get_contracts(get_runner):
    result = get_runner.invoke(database_read_commands.get_contracts)
    assert result.exit_code == 0


def test_get_departments(get_runner):
    result = get_runner.invoke(database_read_commands.get_departments)
    assert result.exit_code == 0


def test_get_events(get_runner):
    result = get_runner.invoke(database_read_commands.get_events)
    assert result.exit_code == 0


def test_get_locations(get_runner):
    result = get_runner.invoke(database_read_commands.get_locations)
    assert result.exit_code == 0


def test_get_roles(get_runner):
    result = get_runner.invoke(database_read_commands.get_roles)
    assert result.exit_code == 0
