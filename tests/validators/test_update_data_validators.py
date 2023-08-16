"""
test des validateurs qui controlent les mises à jour de données
"""
import pytest

try:
    from src.validators import update_data_validators
except ModuleNotFoundError:
    from validators import update_data_validators


def test_new_collaborator_password_is_valid_with_valid_new_password():
    """
    Description:
    Tester la politique de mot de passe
    """
    ret = update_data_validators.new_collaborator_password_is_valid("@zertzy123")
    assert ret is True


@pytest.mark.parametrize("new_password", ("123", "azerty", "azerty123"))
def test_new_collaborator_password_is_valid_with_unvalid_new_password(new_password):
    """
    Description:
    Tester la politique de mot de passe
    """
    with pytest.raises(Exception):
        ret = update_data_validators.new_collaborator_password_is_valid(new_password)
