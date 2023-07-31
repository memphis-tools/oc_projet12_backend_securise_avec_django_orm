"""
Description:
Test de fonctions utiles.
"""
import pytest
import psycopg
try:
    from srv.utils import utils
except ModuleNotFoundError:
    from utils import utils


def test_generate_password_hash_from_input():
    result = utils.generate_password_hash_from_input("alouette")
    pattern_to_find = "pbkdf2:sha256"
    assert result[0 : len(pattern_to_find)] == pattern_to_find


# def test_check_password_hash_from_input():
#     registration_number = "aa123456789"
#     conn = utils.get_a_database_connection()
#     cursor = conn.cursor()
#     sql = f"""SELECT password,username FROM collaborator WHERE registration_number={registration_number}"""
#     cursor.execute(sql)
#     conn.commit()

def test_get_a_database_connection_for_valid_user():
    user_name = "aa123456789"
    user_pwd = "applepie94"
    conn = utils.get_a_database_connection(user_name, user_pwd)
    conn.close()
    assert isinstance(conn, psycopg.Connection)


def test_get_a_database_connection_for_unvalid_user():
    user_name = "rtl2123456789"
    user_pwd = "applepie94"
    with pytest.raises(psycopg.OperationalError):
        conn = utils.get_a_database_connection(user_name, user_pwd)
