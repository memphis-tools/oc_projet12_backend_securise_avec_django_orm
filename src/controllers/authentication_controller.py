"""
Un controleur dédié à la gestion de l'authentification.
"""
from datetime import datetime
import jwt

try:
    from src.authenticators.jwt_authenticator import JwtAuthenticator
except ModuleNotFoundError:
    from authenticators.jwt_authenticator import JwtAuthenticator


class JwtController:
    """
    Description: Toutes les méthodes dédiées à l'authentification.
    """

    def __init__(self):
        self.jwt_authenticator = JwtAuthenticator()

    def get_token(self, session, registration_number, username, role):
        """
        Description:
        Fonction dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
        """
        self.jwt_authenticator = JwtAuthenticator(registration_number, username, role)
        token = self.jwt_authenticator.get_token()
        return token

    def is_token_revoked(self, decoded_token):
        now = datetime.now()
        token_duration = datetime.strptime(
            decoded_token["expiration"], "%Y-%m-%d %H:%M:%S.%f"
        )
        if bool((token_duration - now).days >= 0):
            return False
        return True

    def logout(self):
        """
        Description:
        Fonction dédiée à détruire le jeton utilisateur de son environnement.
        """
        self.jwt_authenticator.logout()

    def does_a_valid_token_exist(self):
        """
        Description:
        Fonction dédiée à controler le jeton utilisateur dans son environnement.
        """
        try:
            decoded_token = JwtAuthenticator.get_decoded_token()
            if self.is_token_revoked(decoded_token):
                return False
            else:
                return True
        except Exception:
            raise jwt.exceptions.InvalidSignatureError
