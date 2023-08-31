"""
vue roles
"""
from rich.console import Console

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.utils import utils
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from utils import utils
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class RolesView:
    """
    Description: une classe dédiée à servir les vues pour les roles de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.session = session

    def get_roles(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Collaborator_Role"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "roles dans entreprise", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info", self.app_dict.get_appli_dictionnary()["NO_MORE_ROLE"]
                    )
                else:
                    message = self.app_dict.get_appli_dictionnary()[
                        "DATABASE_QUERY_NO_MATCHES"
                    ]
                    printer.print_message("info", message)
                    if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                        LOGGER.info(message)
            except Exception:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_FAILURE"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
        else:
            db_model_queryset = self.db_controller.get_roles(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "roles dans entreprise", db_model_queryset
                )
                console.print(table)
                printer.print_message(
                    "info", self.app_dict.get_appli_dictionnary()["NO_MORE_ROLE"]
                )
            else:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_NO_MATCHES"
                ]
                printer.print_message("info", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.info(message)
        return self.db_controller.get_roles(self.session)

    def get_role(self, role_id):
        """
        Description: Vue dédiée à obtenir le role dont l'id est indiqué en entrée.
        Parameters:
        - role_id: une chaine libre qui identifie un role.
        """
        return self.db_controller.get_role(self.session, role_id)

    def add_role(self, role):
        """
        Description: Vue dédiée à ajouter un role.
        Parameters:
        - role: une instance du modèle de classe Collaborator_Role.
        """
        return self.db_controller.add_role(self.session, role)

    def delete_role(self, role_id):
        """
        Description: Vue dédiée à supprimer un role.
        Parameters:
        - role_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_role(self.session, role_id)

    def update_role(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un rôle.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_role(self.session, custom_dict)

    def update_role_filtered(self, user_query_filters_args):
        if len(user_query_filters_args) > 0:
            db_model_queryset = self.db_controller.get_filtered_models(
                self.session, user_query_filters_args[0], "Collaborator_role"
            )
