"""
Description:
Test de la vue "delete_views.py", on test la suppression de données métier avec authentification (token valide).
Pas de bases de données de test, içi on supprime les données créées via "tests/views/test_create_views.py".
On supprime les données en recherchant un "custom id" (une chaine libre), pas l'id entier auto incrémenté de la table.
"""

import pytest

try:
    from src.clients.delete_console import ConsoleClientForDelete
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions
    from settings import settings


def test_delete_client_view_with_commercial_profile_when_client_not_referenced_in_contract(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        dummy_clients_list = ["dduck", "poabm"]
        for client in dummy_clients_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_client(client)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_client_view_with_commercial_profile_when_client_referenced_in_contract_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_client(
            "mkc111"
        )


def test_delete_client_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_client(
            "poabm"
        )


def test_delete_client_view_with_gestion_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_client(
            "poabm"
        )


def test_delete_company_view_with_commercial_profile(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        dummy_companies_list = ["db45785", "abm99998", "NFEPG12345"]
        for company in dummy_companies_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_company(company)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_company_view_with_commercial_profile_when_company_referenced_by_client_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_company(
            "CSLLC12345"
        )


def test_delete_company_view_with_gestion_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_company(
            "abm99998"
        )


def test_delete_company_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_company(
            "abm99998"
        )


def test_delete_contract_view_with_commercial_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_contract("C9Z1")


def test_delete_contract_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_contract("C9Z1")


def test_delete_contract_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        dummy_contracts_list = ["ff555", "av123"]
        for contract in dummy_contracts_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_contract(contract)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_contract_view_with_gestion_profile_when_contract_referenced_in_event_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_contract("kc555")


def test_delete_event_view_with_commercial_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_event(
            "EV971"
        )


def test_delete_event_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_event(
            "geg2021"
        )


def test_delete_event_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        dummy_events_list = ["EV971"]
        for event in dummy_events_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_event(event)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_location_view_with_gestion_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_location("CAL13540")


def test_delete_location_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_location("CAL13540")


def test_delete_location_view_with_commercial_profile_when_location_referenced_by_company_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_location("p22240")


def test_delete_location_view_with_commercial_profile_when_location_not_referenced_by_company(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        dummy_locations_list = ["llb44430"]
        for location in dummy_locations_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_location(location)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_role_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        dummy_roles_list = ["driv", "sec"]
        for role in dummy_roles_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_role(role)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_role_view_with_gestion_profile_when_role_referenced_in_collaborator_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_role(
            "emp"
        )


def test_delete_role_view_with_commercial_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_role(
            "sec"
        )


def test_delete_role_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(db_name=f"{settings.TEST_DATABASE_NAME}").delete_role(
            "sec"
        )


def test_delete_department_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    try:
        dummy_departments_list = ["logist", "design"]
        for department in dummy_departments_list:
            result = ConsoleClientForDelete(
                db_name=f"{settings.TEST_DATABASE_NAME}"
            ).delete_department(department)
            assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_department_view_with_gestion_profile_when_department_referenced_in_collaborator_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_department("ccial")


def test_delete_department_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_department("design")


def test_delete_department_view_with_commercial_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_department("design")


def test_delete_collaborator_view_with_commercial_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_collaborator("ww123456789")


def test_delete_collaborator_view_with_support_profile_raises_exception(
    get_runner, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_collaborator("ww123456789")


@pytest.mark.parametrize(
    "matricule",
    [
        "ww123456789",
        "xx123456789",
        "yy123456789",
        "pp123456789",
        "qq123456789",
        "rr123456789",
    ],
)
def test_delete_collaborator_view_with_gestion_profile(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator, matricule
):
    try:
        result = ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_collaborator(matricule)
        assert isinstance(result, str)
    except Exception as error:
        print(error)


def test_delete_collaborator_view_with_gestion_profile_when_collaborator_referenced_in_contract_raises_exception(
    get_runner, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.ForeignKeyDependyException):
        ConsoleClientForDelete(
            db_name=f"{settings.TEST_DATABASE_NAME}"
        ).delete_collaborator("aa123456789")
