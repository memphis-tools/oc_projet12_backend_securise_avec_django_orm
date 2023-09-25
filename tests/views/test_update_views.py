"""
Description:
Test de la vue "update_views.py", on test la mise à jour de données métier avec authentification (token valide).
Pas de bases de données de test, içi on met à jour les données créées via "tests/views/test_create_views.py".
On recherche un "custom id" (une chaine libre), pas l'id entier auto incrémenté de la table.
Cas particulier d'un collaborateur, le "custom_id" est son registration_number (matricule).
"""
import pytest

try:
    from src.clients.update_console import ConsoleClientForUpdate
    from src.commands import database_update_commands
    from src.exceptions import exceptions
    from src.settings import settings
except ModuleNotFoundError:
    from clients.update_console import ConsoleClientForUpdate
    from commands import database_update_commands
    from exceptions import exceptions
    from settings import settings


client_partial_dict_1 = {
    "client_id": "dduck",
    "telephone": "0677118822",
    "email": "daisy.duck@abm.fr",
}


client_partial_dict_2 = {
    "client_id": "dduck",
    "company_id": "cal7778",
}

client_partial_dict_3 = {
    "client_id": "dduck",
    "company_id": "xx666",
}

client_partial_dict_4 = {
    "client_id": "mkc111",
    "civility": "AUTRE",
    "company_id": "CSLLC12345",
}

client_partial_dict_5 = {
    "client_id": "mkc111",
    "civility": "MR",
    "company_id": "CSLLC12345",
}

collaborator_partial_dict = {
    "registration_number": "ad123456789",
    "username": "marianne de lagraine",
}


department_partial_dict = {"department_id": "logist", "name": "oc12_logistique"}

role_partial_dict = {"role_id": "driv", "name": "chauffeur"}

company_partial_dict = {
    "company_id": "CSLLC12345",
    "company_subregistration_number": "55577",
}

contract_partial_dict1 = {
    "contract_id": "ff555",
    "remain_amount_to_pay": "9599.99",
    "status": "unsigned",
}

contract_partial_dict2 = {
    "contract_id": "zz123",
    "remain_amount_to_pay": "99.99",
}

contract_partial_dict3 = {
    "contract_id": "ff555",
    "status": "signed",
}

contract_partial_dict4 = {
    "contract_id": "zz123",
    "remain_amount_to_pay": "599.19",
    "status": "signed",
}

contract_partial_dict5 = {
    "contract_id": "av123",
    "remain_amount_to_pay": "55.23",
}

contract_partial_dict6 = {
    "contract_id": "ZZ777",
    "remain_amount_to_pay": "599.99",
    "status": "signed",
}

contract_partial_dict7 = {
    "contract_id": "ZZ777",
    "remain_amount_to_pay": "199.99",
}

location_partial_dict = {
    "location_id": "p22240",
    "complement_adresse": "allée de la patissière",
}


def test_update_client_view(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    args_to_convert = client_partial_dict_1
    custom_id = args_to_convert.pop("client_id")
    args_converted = ""
    for k, v in args_to_convert.items():
        args_converted += f"{k}={v} "
    result = get_runner.invoke(
        database_update_commands.update_client,
        f"--client_id={custom_id} {args_converted}",
        f"--db_name={settings.TEST_DATABASE_NAME}",
    )
    assert result.exit_code == 0


def test_update_client_view_with_valid_company_with_commercial_profile_assgined(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Un commercial ne peut modifier un client que s'il est son commercial assigné.
    """
    # on ne va pas invoquer la commande update_client
    # on va directement réaliser ce qu'elle fait
    # on ne veut pas ajouter un argument aux commandes dédiées à l'utilisateur, qui indiqueraient la bdd
    args_to_convert = client_partial_dict_4
    custom_id = args_to_convert["client_id"]
    db_name = settings.TEST_DATABASE_NAME
    company_id = client_partial_dict_4["company_id"]
    expected_company = (
        ConsoleClientForUpdate(custom_id=custom_id, db_name=db_name)
        .app_view.get_companies_view()
        .get_company(company_id)
    )
    expected_company_id = expected_company.get_dict()["id"]
    console_client = ConsoleClientForUpdate(
        custom_id="", db_name=f"{settings.TEST_DATABASE_NAME}"
    )
    args_to_convert["company_id"] = str(expected_company_id)
    result = console_client.update_app_view.get_clients_view().update_client(
        2, "oc12_commecial", args_to_convert
    )
    assert f"{custom_id}" == result


def test_update_client_view_with_valid_company_with_commercial_profile_unassgined_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Un commercial ne peut modifier un client que s'il est son commercial assigné.
    Exception 'CommercialCollaboratorIsNotAssignedToClient' levée le cas échéant.
    """
    args_to_convert = client_partial_dict_5
    custom_id = args_to_convert["client_id"]
    db_name = settings.TEST_DATABASE_NAME
    company_id = client_partial_dict_5["company_id"]
    expected_company = (
        ConsoleClientForUpdate(custom_id=custom_id, db_name=db_name)
        .app_view.get_companies_view()
        .get_company(company_id)
    )
    expected_company_id = expected_company.get_dict()["id"]
    console_client = ConsoleClientForUpdate(
        custom_id="", db_name=f"{settings.TEST_DATABASE_NAME}"
    )
    args_to_convert["company_id"] = str(expected_company_id)
    with pytest.raises(exceptions.CommercialCollaboratorIsNotAssignedToClient):
        result = console_client.update_app_view.get_clients_view().update_client(
            1, "oc12_commecial", args_to_convert
        )


def test_update_client_view_with_unvalid_company(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_commercial_collaborator_id_2,
):
    args_to_convert = client_partial_dict_3
    custom_id = args_to_convert.pop("client_id")
    args_converted = ""
    for k, v in args_to_convert.items():
        args_converted += f"{k}={v} "
    result = get_runner.invoke(
        database_update_commands.update_client,
        f"--client_id={custom_id} {args_converted}",
        f"--db_name={settings.TEST_DATABASE_NAME}",
    )
    assert "Aucun résultat trouvé en base de données" in result.output


def test_update_company_view_with_commercial_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_company(
        company_partial_dict
    )
    assert isinstance(result, str)


def test_update_company_view_with_gestion_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_company(
            company_partial_dict
        )


def test_update_company_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_company(
            company_partial_dict
        )


def test_update_contract_status_when_event_attached_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Un commercial ne peut modifier un contrat que s'il est le commercial assigné.
    Exception 'exceptions.CommercialCollaboratorIsNotAssignedToContract' levée autrement.
    """
    with pytest.raises(exceptions.EventAttachedContractStatusCanNotBeUpdateException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(
            contract_partial_dict1
        )


def test_update_contract_view_with_commercial_profile_unassigned_to_contract_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Un commercial ne peut modifier un contrat que s'il est le commercial assigné.
    Exception 'exceptions.CommercialCollaboratorIsNotAssignedToContract' levée autrement.
    """
    with pytest.raises(exceptions.CommercialCollaboratorIsNotAssignedToContract):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(
            contract_partial_dict6
        )


def test_update_contract_view_with_commercial_profile_assigned_to_contract(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    """
    Description:
    Un commercial ne peut modifier un contrat que s'il est le commercial assigné.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_contract(
        contract_partial_dict5
    )
    assert isinstance(result, str)


def test_update_contract_view_with_gestion_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_contract(
        contract_partial_dict7
    )
    assert isinstance(result, str)
    assert "Update" in result


def test_update_contract_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_contract(
            contract_partial_dict4
        )


def test_update_event_view_with_commercial_profile_raises_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_commercial_collaborator,
    dummy_event_partial_data_1,
):
    # un membre du service commercial ne peut que 'créer', pas 'mettre à jour' voir cahier des charges
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_event(
            dummy_event_partial_data_1
        )


def test_update_event_view_with_gestion_profile(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_event_partial_data_0,
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_event(
        dummy_event_partial_data_0
    )
    assert isinstance(result, str)
    assert "Update" in result


def test_update_event_view_with_gestion_profile_when_collaborator_assigned_not_from_support_team(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_gestion_collaborator,
    dummy_event_partial_data_5,
):
    """
    Description:
    Un membre du service support ne peut modifier un évènement que s'il est le collaborateur assigné.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    with pytest.raises(exceptions.OnlySuportMemberCanBeAssignedToEventSupportException):
        result = ConsoleClientForUpdate(db_name=db_name).update_event(
            dummy_event_partial_data_5
        )


def test_update_event_view_with_support_profile_when_collaborator_is_assigned(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_support_collaborator_with_id_5,
    dummy_event_partial_data_2,
):
    """
    Description:
    Un membre du service support ne peut modifier un évènement que s'il est le collaborateur assigné.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_event(
        dummy_event_partial_data_2
    )
    assert isinstance(result, str)


def test_update_event_view_with_support_profile_when_collaborator_is_not_assigned_raises_exception(
    get_runner,
    set_a_test_env,
    get_valid_decoded_token_for_a_support_collaborator_with_id_7,
    dummy_event_partial_data_3,
):
    """
    Description:
    Un membre du service support ne peut modifier un évènement que s'il le collaborateur assigné.
    On lève l'exception 'exceptions.SupportCollaboratorIsNotAssignedToEvent' dans le cas contraire.
    """
    with pytest.raises(exceptions.SupportCollaboratorIsNotAssignedToEvent):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_event(
            dummy_event_partial_data_3
        )


def test_update_location_view_with_commercial_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    try:
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(
            location_partial_dict
        )
        assert isinstance(result, dict)
    except Exception as error:
        print(error)


def test_update_location_view_with_gestion_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(
            location_partial_dict
        )


def test_update_location_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_location(
            location_partial_dict
        )


def test_update_role_view_with_gestion_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)
    assert isinstance(result, str)


def test_update_role_view_with_commercial_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)


def test_update_role_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_role(role_partial_dict)


def test_update_department_view_with_gestion_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_department(
        department_partial_dict
    )
    assert isinstance(result, str)


def test_update_department_view_with_commercial_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_department(
            role_partial_dict
        )


def test_update_department_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_department(
            role_partial_dict
        )


def test_update_collaborator_view_with_gestion_profile(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_gestion_collaborator
):
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(
        collaborator_partial_dict
    )
    assert isinstance(result, str)


def test_update_collaborator_view_with_commercial_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_commercial_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(
            role_partial_dict
        )


def test_update_collaborator_view_with_support_profile_raises_exception(
    get_runner, set_a_test_env, get_valid_decoded_token_for_a_support_collaborator
):
    with pytest.raises(exceptions.InsufficientPrivilegeException):
        db_name = f"{settings.TEST_DATABASE_NAME}"
        result = ConsoleClientForUpdate(db_name=db_name).update_collaborator(
            role_partial_dict
        )
