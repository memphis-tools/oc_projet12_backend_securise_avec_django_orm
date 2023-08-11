"""
La console en mode update doit en outre permettre la mise à jour du mot de passe d'un collaborateur
"""
import re
import psycopg
try:
    from src.exceptions import exceptions
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from exceptions import exceptions
    from settings import settings
    from utils import utils


def old_collaborator_password_is_valid(
        user_registration_number,
        old_password,
    ) -> bool:
    """
    Description:
    Un validateur pour vérifier si le mot de passe fourni est celui connu en base.
    Paramètres:
    - update_app_view: une vue afin de pouvoir établir une jonction avec le controleur de bdd
    - user_registration_number: chaine de caractères, matricule d'un employé /du collaborateur
    - old_password: chaine de caractères, mot de passe actuel de l'employé /du collaborateur
    """
    try:
        conn = utils.get_a_database_connection(
            user_name=user_registration_number,
            user_pwd=old_password
        )
        conn.close()
        return True
    except psycopg.OperationalError:
        return False


def new_collaborator_password_is_valid(new_password):
    """
    Description:
    Un validateur pour vérifier si le nouveau mot de passe répond aux exigences de sécurité.
    Paramètres:
    - new_password: chaine de caractères, nouveau mot de passe de l'employé /du collaborateur
    """

    b1 = bool(len(new_password) >= settings.DEFAULT_NEW_PASSWORD_MIN_LENGTH)
    b2 = bool(len(new_password) < settings.DEFAULT_NEW_PASSWORD_MAX_LENGTH)

    min_digits = settings.DEFAULT_NEW_PASSWORD_MIN_DIGITS
    pattern = re.compile(rf'.*(\d{{{min_digits}}}).*')
    b3 = bool(re.match(pattern, new_password))

    min_specialchars = settings.DEFAULT_NEW_PASSWORD_MIN_SPECIAL_CHAR
    specialchars = "".join(settings.ALLOWED_SPECIALCHARS_IN_PASSWORD)
    pattern = re.compile(rf".*([{specialchars}]{{{min_specialchars}}}).*")
    try:
        check_password = re.match(pattern, new_password)
        b4 = bool(check_password.group())
    except Exception:
        raise exceptions.NewPasswordDoesRespectMinSpecialCharsException()

    forbidden_specialchars = "".join(settings.FORBIDDEN_SPECIALCHARS_IN_PASSWORD)
    pattern = re.compile(rf".*([{forbidden_specialchars}]{1,}).*")
    try:
        check_password = re.match(pattern, new_password)
        b5 = isinstance(type(check_password), type(None))
    except Exception as error:
        raise exceptions.NewPasswordDoesRespectForbiddenSpecialCharsException()

    if all([b1, b2, b3, b4]) and not b5:
        return True
