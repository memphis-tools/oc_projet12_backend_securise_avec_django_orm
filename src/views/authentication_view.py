"""
On fournit une vue dédiée à controler l'authentification et une autre qui permet d'atteindre les modèles.
"""
from rich import print

try:
    from src.controllers.authentication_controller import JwtController
    from src.utils.utils import check_password_hash_from_input
except ModuleNotFoundError:
    from controllers.authentication_controller import JwtController
    from utils.utils import check_password_hash_from_input


class AuthenticationView:
    """
    Description: une classe dédiée à servir la vue sur l'authentification.
    """

    def __init__(self, AppView):
        """
        Description: vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.jwt_controller = JwtController()
        self.app_view = AppView

    def get_token(self, registration_number, password):
        """
        Description: vue dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
        """
        collaborator = self.app_view.db_controller.get_collaborator(
            self.app_view.session, registration_number
        )
        if collaborator:
            db_user_password = collaborator.password
            if check_password_hash_from_input(db_user_password, password):
                r_number = registration_number
                u_name = collaborator.username
                role = collaborator.role
                information = "[bold green]Please add the following in your path and execute 'run_app'[/bold green]:"
                to_do = f"OC_12_JWT='{self.jwt_controller.get_token(self.app_view.session, r_number, u_name, role)}'"
                print(information)
                print(to_do)
                return
        raise Exception("Wrong credentials sir")

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
