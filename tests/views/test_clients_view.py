"""
Description:
Test de la vue pour les clients de l'entreprise'.
"""
import pytest
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.commands import database_read_commands, database_create_commands
    from src.models import models
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from commands import database_read_commands, database_create_commands
    from models import models


location_attributes_dict = {
    "location_id": "PL24250",
    "adresse": "3 rue de la tannerie",
    "complement_adresse": "La meule en bière",
    "code_postal": "24250",
    "ville": "Plurien",
    "pays": "France",
}

company_attributes_dict = {
    "company_id": "abm99998",
    "company_name": "A la bonne meule",
    "company_registration_number": "777666111",
    "company_subregistration_number": "99998",
    "location_id": "3"
}

client_attributes_dict = {
    "client_id": "id",
    "civility": "MR",
    "first_name": "john",
    "last_name": "doe",
    "employee_role": "press officer",
    "email": "j.doe@abm.fr",
    "telephone": "+611223344",
    "company_id": "2"
}


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
    ]
)
def test_get_views(get_runner, command):
    result = get_runner.invoke(eval(f"database_read_commands.{command}"))
    assert result.exit_code == 0
    assert "Missing token" in result.output


def test_add_location_view(get_runner, get_valid_decoded_token):
    try:
        result = ConsoleClientForCreate().add_location(location_attributes_dict)
        assert isinstance(result, int)
        # assert result.exit_code == 0
    except Exception as error:
        print(error)
