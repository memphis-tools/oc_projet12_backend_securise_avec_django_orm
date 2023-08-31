"""
Description:
Test de la vue "views.py", on test d'avoir la liste des données métier sans s'authentifier (sans token).
"""
import pytest

try:
    from src.clients.read_console import ConsoleClientForRead
    from src.commands import database_read_commands
    from src.settings import settings
    from src.exceptions import exceptions
    from src.views.crud_views.views import AppViews
except ModuleNotFoundError:
    from clients.read_console import ConsoleClientForRead
    from commands import database_read_commands
    from settings import settings
    from exceptions import exceptions
    from views.crud_views.views import AppViews


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
    get_runner,
    set_a_test_env,
    command,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Toutes les données métier doivent être accessibles en lecture seule par tout collaborateur de l'entreprise.
    Içi on vérifie que les 'vues' seront accessibles.
    """
    UNUSED_APP_DICT = database_read_commands.APP_DICT
    result = get_runner.invoke(eval(f"database_read_commands.{command}"))
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "db_model",
    ["clients", "companies", "contracts", "departments", "roles", "locations"],
)
def test_get_items(
    set_a_test_env, db_model, get_valid_decoded_token_for_a_gestion_collaborator
):
    """
    Description:
    Toutes les données métier doivent être accessibles en lecture seule par tout collaborateur de l'entreprise.
    Içi on vérifie que les 'vues' renvoient du contenu.
    """
    app_view = AppViews(db_name=f"{settings.TEST_DATABASE_NAME}")
    db_model_view = eval(f"app_view.get_{db_model}_view().get_{db_model}()")
    assert len(db_model) > 0


def test_get_client(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un client.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_clients(("client_id=SRODAP37",))
    assert isinstance(result, list)


def test_get_role(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un role.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_roles(("role_id=emp",))
    assert isinstance(result, list)


def test_get_role_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un role.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.QueryFailureException):
        ConsoleClientForRead(db_name).get_roles(("role_id=man et some_id=something",))


def test_get_department(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un service /department.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_departments(("department_id=ccial",))
    assert isinstance(result, list)


def test_get_department_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un service.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.QueryFailureException):
        ConsoleClientForRead(db_name).get_roles(
            ("department_id=ccial et some_id=something",)
        )


def test_get_location(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'une localité.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_locations(("location_id=p22240",))
    assert isinstance(result, list)


def test_get_location_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'une localité.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.QueryFailureException):
        ConsoleClientForRead(db_name).get_roles(
            ("location_id=p22240 et some_id=something",)
        )


def test_get_company(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'une entreprise.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_companies(("company_id=CSLLC12345",))
    assert isinstance(result, list)


def test_get_company_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'une entreprise.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.QueryFailureException):
        ConsoleClientForRead(db_name).get_roles(
            ("company_id=CSLLC12345 et some_id=something",)
        )


def test_get_contract(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un contrat.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_contracts(("contract_id=kc555",))
    assert isinstance(result, list)


def test_get_contract_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'une entreprise.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.QueryFailureException):
        ConsoleClientForRead(db_name).get_roles(
            ("contract_id=kc555 et some_id=something",)
        )


def test_get_event(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un évènement.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_events(("event_id=hob2023",))
    assert isinstance(result, list)


def test_get_event_with_invalid_attributes_raise_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
):
    """
    Description:
    Vérifier le filtre d'un évènement.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.CustomIdMatchNothingException):
        ConsoleClientForRead(db_name).get_events(("attendees>50 et some_id=something",))
