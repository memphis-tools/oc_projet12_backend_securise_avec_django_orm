"""
Description:
Test du controleur pour l'authentification. Classe JwtController
"""
import os
import jwt
import pytest
from datetime import datetime, timedelta

try:
    from src.controllers.jwt_controller import JwtController
except ModuleNotFoundError:
    from controllers.jwt_controller import JwtController


dummy_token_data = {
    "registration_number": "aa123456789",
    "username": "donald duck",
    "department": "oc12_commercial",
    "expiration": f"{datetime.utcnow() + timedelta(hours=12)}",
}


def test_get_token():
    """
    Description:
    Vérifier qu'on obtient un token avec les arguments attendus.
    """
    jwt_controller = JwtController()
    dummy_data = list(dummy_token_data.values())[0:3]
    token = jwt_controller.get_token(
        dummy_data[0],
        dummy_data[1],
        dummy_data[2],
    )
    assert isinstance(token, str)


def test_is_token_revoked_with_unrevoked_token():
    """
    Description:
    Vérifier qu'un token non révoqué est bien vu valide.
    """
    jwt_controller = JwtController()
    revoked = jwt_controller.is_token_revoked(dummy_token_data)
    assert revoked is False


def test_is_token_revoked_with_revoked_token():
    """
    Description:
    Vérifier qu'un token révoqué est bien vu invalide.
    """
    jwt_controller = JwtController()
    dummy_token_data_copy = dummy_token_data.copy()
    dummy_token_data_copy["expiration"] = f"{datetime.utcnow() + timedelta(days=-1)}"
    revoked = jwt_controller.is_token_revoked(dummy_token_data_copy)
    assert revoked is True


def test_logout():
    """
    Description:
    Vérifier qu'on retire le jeton du PATH courant de l'application.
    (Noter le faux cas d'usage: on ne peut pas atteindre le PATH du processus parent.)
    """
    jwt_controller = JwtController()
    os.environ["OC_12_JWT"] = "OC_12_JWT='dummy_token'"
    jwt_controller.logout()
    revoked = bool("OC_12_JWT" in list(os.environ.keys()))
    assert revoked is False


def test_does_a_valid_token_exist_with_unvalid_token():
    """
    Description:
    Vérifier que le token en PATH est invalide.
    """
    jwt_controller = JwtController()
    os.environ["OC_12_JWT"] = "OC_12_JWT='dummy_token'"
    with pytest.raises(jwt.exceptions.InvalidSignatureError):
        exist = jwt_controller.does_a_valid_token_exist()
