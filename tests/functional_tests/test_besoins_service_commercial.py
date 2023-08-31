"""
Description:
Tests fonctionnels pour les besoins spécifiques de l'équipe Commercial
"""
try:
    from src.clients.create_console import ConsoleClientForCreate
    from src.clients.read_console import ConsoleClientForRead
    from src.clients.update_console import ConsoleClientForUpdate
    from src.settings import settings
except ModuleNotFoundError:
    from clients.create_console import ConsoleClientForCreate
    from clients.read_console import ConsoleClientForRead
    from clients.update_console import ConsoleClientForUpdate
    from settings import settings


def test_client_creation_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    dummy_client_data_2,
):
    """
    Description:
    Un membre du service Commercial doit pouvoir créer des clients (le client leur sera automatiquement associé).
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForCreate(db_name).add_client(dummy_client_data_2)
    assert isinstance(result, str)

    current_commercial_user = get_valid_decoded_token_for_a_commercial_collaborator[
        "registration_number"
    ]
    collaborators = ConsoleClientForRead(db_name).get_collaborators()
    id_current_commercial_user = ""
    for collaborator in collaborators:
        if collaborator.registration_number == current_commercial_user:
            id_current_commercial_user = collaborator.id
            break

    clients = ConsoleClientForRead(db_name).get_clients(("client_id=bduck",))
    id_commercial_contact = ""
    for client in clients:
        if client.client_id == "bduck":
            id_commercial_contact = client.commercial_contact
            break
    assert id_current_commercial_user == id_commercial_contact


def test_client_update_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    dummy_client_partial_data,
):
    """
    Description:
    Un membre du service Commercial doit pouvoir mettre à jour les clients dont il est responsable.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForUpdate(db_name).update_client(dummy_client_partial_data)
    assert isinstance(result, str)

    clients = ConsoleClientForRead(db_name).get_clients(("client_id=bduck",))
    client_updated = ""
    for client in clients:
        if client.client_id == "bduck":
            client_updated = client
            break
    assert client_updated.telephone == dummy_client_partial_data["telephone"]
    assert client_updated.first_name == dummy_client_partial_data["first_name"]


def test_contract_update_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
    dummy_contract_partial_data_2,
):
    """
    Description:
    Un membre du service Commercial doit pouvoir mettre à jour les contrats des clients dont il est responsable.
    """
    id_updated_contract = dummy_contract_partial_data_2["contract_id"]
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = ConsoleClientForRead(db_name).get_contracts()
    assert isinstance(result, list)

    result = ConsoleClientForUpdate(db_name).update_contract(
        dummy_contract_partial_data_2
    )
    assert isinstance(result, str)

    contracts = ConsoleClientForRead(db_name).get_contracts(
        (f"contract_id={id_updated_contract}",)
    )
    contract_updated = ""
    for contract in contracts:
        if contract.contract_id == f"{id_updated_contract}":
            contract_updated = contract
            break
    assert float(contract_updated.remain_amount_to_pay) == float(
        dummy_contract_partial_data_2["remain_amount_to_pay"]
    )
    assert contract_updated.status == dummy_contract_partial_data_2["status"]


def test_contract_display_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
):
    """
    Description:
    Un membre du service Commercial doit pouvoir filtrer l’affichage des contrats, par exemple :
    afficher tous les contrats qui ne sont pas encore signés, ou qui ne sont pas encore entièrement payés.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    unsigned_contracts = ConsoleClientForRead(db_name).get_contracts(
        ("status=unsigned",)
    )
    assert isinstance(unsigned_contracts, list)

    unpaid_contracts = ConsoleClientForRead(db_name).get_contracts(
        ("remain_amount_to_pay>0",)
    )
    assert isinstance(unpaid_contracts, list)


def test_event_creation_manipulation(
    set_a_test_env,
    get_runner,
    get_valid_decoded_token_for_a_commercial_collaborator,
):
    """
    Description:
    Un membre du service Commercial doit pouvoir créer un événement pour un de leurs clients qui a signé un contrat.
    """
    db_name = f"{settings.TEST_DATABASE_NAME}"
    event_dict = {
        "creation_date": "2023-07-14 09:05:10",
        "event_id": "fvc4440",
        "title": "Faites vous cuisiner",
        "attendees": "325",
        "notes": "Prévoir au moins 3 type de plats /cuisines. Rester dans l'esprit de l'évènement.",
        "event_start_date": "2024-02-15 18:00:00",
        "event_end_date": "2024-02-15 23:00:00",
        "client_id": "",
        "contract_id": "",
        "location_id": "2",
        "collaborator_id": None,
    }
    clients = ConsoleClientForRead(db_name).get_clients(("client_id=bduck",))
    client_for_event = ""
    for client in clients:
        if client.client_id == "bduck":
            client_for_event = client
            break
    event_dict["client_id"] = client_for_event.id
    contracts = ConsoleClientForRead(db_name).get_contracts()
    contract_for_event = ""
    for contract in contracts:
        if contract.contract_id == "av123":
            contract_for_event = contract
            break
    event_dict["contract_id"] = contract_for_event.id
    result = ConsoleClientForCreate(db_name).add_event(event_dict)
    assert isinstance(result, str)
