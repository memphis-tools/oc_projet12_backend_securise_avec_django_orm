from src.clients import console


def test_get_clients(get_runner):
    result = get_runner.invoke(console.get_clients)
    assert result.exit_code == 0


def test_get_collaborators(get_runner):
    result = get_runner.invoke(console.get_collaborators)
    assert result.exit_code == 0


def test_get_contracts(get_runner):
    result = get_runner.invoke(console.get_contracts)
    assert result.exit_code == 0


def test_get_departments(get_runner):
    result = get_runner.invoke(console.get_departments)
    assert result.exit_code == 0


def test_get_events(get_runner):
    result = get_runner.invoke(console.get_events)
    assert result.exit_code == 0


def test_get_locations(get_runner):
    result = get_runner.invoke(console.get_locations)
    assert result.exit_code == 0


def test_get_roles(get_runner):
    result = get_runner.invoke(console.get_roles)
    assert result.exit_code == 0
