"""
Description:
Test de fonctions utiles.
"""
import pytest
import psycopg

try:
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils
    from settings import settings


def test_get_a_database_connection_for_valid_user():
    user_name = "aa123456789"
    user_pwd = f"{settings.DEFAULT_NEW_COLLABORATOR_PASSWORD}"
    conn = utils.get_a_database_connection(user_name, user_pwd)
    conn.close()
    assert isinstance(conn, psycopg.Connection)


def test_get_a_database_connection_for_unvalid_user():
    user_name = "rtl2123456789"
    user_pwd = f"{settings.DEFAULT_NEW_COLLABORATOR_PASSWORD}"
    with pytest.raises(psycopg.OperationalError):
        conn = utils.get_a_database_connection(user_name, user_pwd)
