"""
On fournit une vue dédiée à controler l'authentification et une autre qui permet d'atteindre les modèles.
"""
from rich import print

try:
    from src.controllers.jwt_controller import JwtController
    from src.utils.utils import check_password_hash_from_input
except ModuleNotFoundError:
    from controllers.jwt_controller import JwtController
    from utils.utils import check_password_hash_from_input


class JwtView:
    """
    Description: une classe dédiée à servir la vue sur l'authentification.
    """

    def __init__(self, AppView):
        """
        Description: vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.jwt_controller = JwtController()
        self.app_view = AppView

    def get_token(self, registration_number):
        """
        Description: vue dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
        """
        collaborator, collaborator_department_name = self.app_view.db_controller.get_collaborator(
            self.app_view.session, registration_number
        )

        r_number = registration_number
        u_name = collaborator.username
        department = collaborator_department_name
        information = '[bold cyan]Add the following in your path and run any commands (try oc12_help)[/bold cyan]:'
        to_do = f"OC_12_JWT='{self.jwt_controller.get_token(self.app_view.session, r_number, u_name, department)}'"
        print(information)
        print(to_do)
        return

    def does_a_valid_token_exist(self):
        """
        Description:
        Fonction dédiée à controler le jeton utilisateur dans son environnement.
        """
        return self.jwt_controller.does_a_valid_token_exist()

    def logout(self):
        return self.jwt_controller.logout()

    def check_user_token(self):
        return self.jwt_controller.check_user_token()

    def get_decoded_token(self):
        return self.jwt_controller.get_decoded_token()
