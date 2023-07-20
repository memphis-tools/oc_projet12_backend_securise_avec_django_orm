"""
Description:
Définir les fonctions d'authentification et les paramètres des jetons /tokens.
Permettre login, logout. Controler le jeton /token utilisé par l'utilisateur courant.
"""
import os
from datetime import datetime, timedelta
import jwt

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


class JwtAuthenticator:
    """
    Description:
    Classe dédiée au controle de l'authentification via JWT
    """

    def __init__(self, registration_number="", username="", role=""):
        self.registration_number = registration_number
        self.username = username
        self.role = role

    def get_decoded_token():
        """
        Description: Dédiée à servir le token en clair (s'il a pu être décodé avec la clef secrète).
        """
        token = os.environ[f"{settings.PATH_APPLICATION_JWT_NAME}"]
        decoded_token = jwt.decode(
            token,
            key=f"{settings.SECRET_KEY}",
            algorithms=[f"{settings.HASH_ALGORITHM}"],
        )
        return decoded_token

    @staticmethod
    def is_authenticated():
        """
        Description: Méthode statique pour vérifeir la présence d'un jeton dans le path.
        """
        if f"{settings.PATH_APPLICATION_JWT_NAME}" in os.environ:
            return True
        return False

    def get_token(self):
        """
        Description: Dédiée à confectionner un jeton d'accès pour l'utilisateur.
        """
        now = datetime.now()
        timedelta_setting = {f"{settings.JWT_UNIT_DURATION}": settings.JWT_DURATION}
        expiration = now + timedelta(**timedelta_setting)
        payload_data = {
            "registration_number": self.registration_number,
            "username": self.username,
            "role": self.role,
            "expiration": f"{expiration}",
        }
        token = jwt.encode(
            payload=payload_data,
            key=f"{settings.SECRET_KEY}",
            algorithm=f"{settings.HASH_ALGORITHM}",
        )
        os.environ[f"{settings.PATH_APPLICATION_JWT_NAME}"] = token
        return token

    def login(self):
        """
        Description: sert d'alias, pour obtention du token.
        """
        self.get_token()
        return True

    def logout(self):
        """
        Description: Dédiée à représenter une déconnexion de l'application.
        Rappel, le jeton d'accès est dans le path "principal /parent".
        On ne pourra pas unset la variable du path.
        """
        if f"{settings.PATH_APPLICATION_JWT_NAME}" in os.environ:
            del os.environ[f"{settings.PATH_APPLICATION_JWT_NAME}"]
        return True
