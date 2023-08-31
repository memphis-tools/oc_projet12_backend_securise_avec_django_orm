"""
vue collaborateurs
"""
from rich.console import Console

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.utils import utils
    from src.validators import update_data_validators
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from utils import utils
    from validators import update_data_validators
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class CollaboratorsView:
    """
    Description: une classe dédiée à servir les vues pour les collaborateurs de l'entreprise.
    """

    def __init__(self, db_controller, db_initializer, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.db_initializer = db_initializer
        self.session = session

    def get_collaborators(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Collaborator"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "utilisateurs", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info",
                        self.app_dict.get_appli_dictionnary()["NO_MORE_COLLABORATOR"],
                    )
                else:
                    message = self.app_dict.get_appli_dictionnary()[
                        "DATABASE_QUERY_NO_MATCHES"
                    ]
                    printer.print_message("info", message)
                    if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                        LOGGER.info(message)
            except TypeError:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_NO_MATCHES"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
            except Exception:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_FAILURE"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
        else:
            db_model_queryset = self.db_controller.get_collaborators(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "utilisateurs", db_model_queryset
                )
                console.print(table)
                printer.print_message(
                    "info",
                    self.app_dict.get_appli_dictionnary()["NO_MORE_COLLABORATOR"],
                )
            else:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_NO_MATCHES"
                ]
                printer.print_message("info", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.info(message)
        return self.db_controller.get_collaborators(self.session)

    def get_collaborator(self, registration_number):
        """
        Description: Vue dédiée à obtenir le collaborateur dont l'id est indiqué en entrée.
        Parameters:
        - registration_number: une chaine libre qui identifie un collaborateur, un matricule.
        """
        return self.db_controller.get_collaborator(self.session, registration_number)

    def add_collaborator(self, collaborator):
        """
        Description: Vue dédiée à ajouter un collaborateur de l'entreprise.
        Parameters:
        - collaborator: une instance du modèle de classe Collaborator.
        """
        return self.db_controller.add_collaborator(self.session, collaborator)

    def delete_collaborator(self, collaborator_id):
        """
        Description: Vue dédiée à supprimer un collaborateur de l'entreprise.
        Parameters:
        - collaborator_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_collaborator(self.session, collaborator_id)

    def update_collaborator(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un collaborateur.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_collaborator(self.session, custom_dict)

    def update_collaborator_filtered(self, user_query_filters_args):
        if len(user_query_filters_args) > 0:
            db_model_queryset = self.db_controller.get_filtered_models(
                self.session, user_query_filters_args[0], "Collaborator"
            )

    def update_collaborator_password(
        self, user_registration_number, old_password, new_password
    ):
        """
        Description:
        Dédiée à mettre à jour le mot de passe d'un collaborateur.
        Parameters:
        - user_registration_number: chaine de caractères, le matricule de l'employé /du collaborateur.
        - old_password: chaine de caractères, l'ancien mot de passe de l'utilisateur /du collaborateur.
        - new_password: chaine de caractères, le nouveau mot de passe de l'utilisateur /du collaborateur.
        """
        conn = utils.get_a_database_connection(
            user_name=user_registration_number, user_pwd=old_password
        )
        return self.db_controller.update_collaborator_password(
            conn, user_registration_number, new_password
        )

    def old_collaborator_password_is_valid(
        self,
        user_registration_number,
        old_password,
    ):
        """
        Description:
        Dédiée à vérifier le mot de passe courant d'un collaborateur de l'entreprise.
        """
        return update_data_validators.old_collaborator_password_is_valid(
            user_registration_number,
            old_password,
        )

    def new_collaborator_password_is_valid(self, new_password):
        """
        Description:
        Dédiée à vérifier le nouveau mot de passe d'un collaborateur de l'entreprise.
        """
        return update_data_validators.new_collaborator_password_is_valid(new_password)
