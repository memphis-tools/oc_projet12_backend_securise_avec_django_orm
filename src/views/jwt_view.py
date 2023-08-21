"""
Description:
On fournit une vue dédiée à controler l'authentification et une autre qui permet d'atteindre les modèles.
"""
from rich import print

try:
    from src.exceptions import exceptions
    from src.controllers.jwt_controller import JwtController
    from src.languages import language_bridge
    from src.printers import printer
except ModuleNotFoundError:
    from exceptions import exceptions
    from controllers.jwt_controller import JwtController
    from languages import language_bridge
    from printers import printer


class JwtView:
    """
    Description:
    Classe dédiée à servir la vue sur l'authentification.
    """

    def __init__(self, AppView):
        """
        Description:
        Vue dédiée à instancier la base de données et retourner un controleur.
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.jwt_controller = JwtController()
        self.app_view = AppView

    def get_token(self, registration_number):
        """
        Description:
        Fonction dédiée à obtenir un token, nécessaire pour s'authentifier sur l'application.
        """
        try:
            (
                collaborator_username,
                collaborator_department_name,
            ) = self.app_view.db_controller.get_collaborator_join_department(
                self.app_view.session, registration_number
            )
            r_number = registration_number
            u_name = collaborator_username
            department = collaborator_department_name
            printer.print_message(
                "info",
                self.app_dict.get_appli_dictionnary()[
                    "TOKEN_INFO_IN_TERMINAL_OUTPUT_1"
                ],
            )
            printer.print_message(
                "info",
                self.app_dict.get_appli_dictionnary()[
                    "TOKEN_INFO_IN_TERMINAL_OUTPUT_2"
                ],
            )
            printer.print_message(
                "info",
                self.app_dict.get_appli_dictionnary()[
                    "TOKEN_INFO_IN_TERMINAL_OUTPUT_3"
                ],
            )
            to_do = f"OC_12_JWT='{self.jwt_controller.get_token(r_number, u_name, department)}'"
            print(to_do)
            return
        except exceptions.AuthenticationCredentialsFailed:
            raise exceptions.AuthenticationCredentialsFailed()

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
