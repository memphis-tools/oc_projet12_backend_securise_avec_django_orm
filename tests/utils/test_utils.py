"""
Description:
Test de fonctions utiles.
"""

try:
    from srv.utils import utils
    from src.settings import settings
except ModuleNotFoundError:
    from utils import utils
    from settings import settings


def test_generate_password_hash_from_input():
    result = utils.generate_password_hash_from_input("alouette")
    pattern_to_find = "pbkdf2:sha256"
    assert result[0:len(pattern_to_find)] == pattern_to_find


# def test_check_password_hash_from_input():
#     registration_number = "123456789A"
#     conn = utils.get_a_database_connection()
#     cursor = conn.cursor()
#     sql = f"""SELECT password,username FROM collaborator WHERE registration_number={registration_number}"""
#     cursor.execute(sql)
#     conn.commit()
