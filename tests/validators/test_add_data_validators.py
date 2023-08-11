"""
test des validateurs qui controlent les ajouts de données
"""
import pytest
try:
    from src.validators import add_data_validators
except ModuleNotFoundError:
    from validators import add_data_validators


def test_data_is_dict_with_dict_data():
    ret = add_data_validators.data_is_dict({"name": "dummy",})
    assert ret is True


@pytest.mark.parametrize('not_a_dict', ([], (), ""))
def test_data_is_dict_without_dict_data(not_a_dict):
    ret = add_data_validators.data_is_dict(not_a_dict)
    assert ret is False


def test_add_client_data_is_valid_with_all_expeted_data(dummy_client_data):
    ret = add_data_validators.add_client_data_is_valid(dummy_client_data)
    assert ret is True


def test_add_collaborator_data_is_valid_with_all_expeted_data(dummy_collaborator_data):
    ret = add_data_validators.add_collaborator_data_is_valid(dummy_collaborator_data)
    assert ret is True


def test_add_collaborator_department_data_is_valid_with_all_expeted_data(dummy_collaborator_department_data):
    ret = add_data_validators.add_department_data_is_valid(dummy_collaborator_department_data)
    assert ret is True


def test_add_collaborator_role_data_is_valid_with_all_expeted_data(dummy_collaborator_role_data):
    ret = add_data_validators.add_role_data_is_valid(dummy_collaborator_role_data)
    assert ret is True


def test_add_contract_data_is_valid_with_all_expeted_data(dummy_contract_data):
    ret = add_data_validators.add_contract_data_is_valid(dummy_contract_data)
    assert ret is True


def test_add_event_data_is_valid_with_all_expeted_data(dummy_event_data):
    ret = add_data_validators.add_event_data_is_valid(dummy_event_data)
    assert ret is True


def test_add_location_data_is_valid_with_all_expeted_data(dummy_location_data):
    ret = add_data_validators.add_location_data_is_valid(dummy_location_data)
    assert ret is True


def test_add_client_data_is_valid_without_all_expeted_data(dummy_client_data):
    dummy_client_data.pop("company_id")
    ret = add_data_validators.add_client_data_is_valid(dummy_client_data)
    assert ret is False


def test_add_collaborator_data_is_valid_without_all_expeted_data(dummy_collaborator_data):
    dummy_collaborator_data.pop("username")
    ret = add_data_validators.add_collaborator_data_is_valid(dummy_collaborator_data)
    assert ret is False


def test_add_collaborator_department_data_is_valid_without_all_expeted_data(dummy_collaborator_department_data):
    dummy_collaborator_department_data.pop("department_id")
    ret = add_data_validators.add_department_data_is_valid(dummy_collaborator_department_data)
    assert ret is False


def test_add_collaborator_role_data_is_valid_without_all_expeted_data(dummy_collaborator_role_data):
    dummy_collaborator_role_data.pop("role_id")
    ret = add_data_validators.add_role_data_is_valid(dummy_collaborator_role_data)
    assert ret is False


def test_add_contract_data_is_valid_without_all_expeted_data(dummy_contract_data):
    dummy_contract_data.pop("contract_id")
    ret = add_data_validators.add_contract_data_is_valid(dummy_contract_data)
    assert ret is False


def test_add_event_data_is_valid_without_all_expeted_data(dummy_event_data):
    dummy_event_data.pop("event_id")
    ret = add_data_validators.add_event_data_is_valid(dummy_event_data)
    assert ret is False


def test_add_location_data_is_valid_without_all_expeted_data(dummy_location_data):
    dummy_location_data.pop("location_id")
    ret = add_data_validators.add_location_data_is_valid(dummy_location_data)
    assert ret is False
