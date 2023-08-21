"""
vue departments
"""
from rich.console import Console

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from utils import utils


class DepartmentsView:
    """
    Description: une classe dédiée à servir les vues pour les departments /services de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.session = session

    def get_departments(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Collaborator_Department"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "services /départements", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info",
                        self.app_dict.get_appli_dictionnary()["NO_MORE_DEPARTEMENT"],
                    )
                else:
                    printer.print_message(
                        "error",
                        self.app_dict.get_appli_dictionnary()[
                            "DATABASE_QUERY_NO_MATCHES"
                        ],
                    )
            except Exception as error:
                printer.print_message(
                    "error",
                    self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"],
                )
        else:
            db_model_queryset = self.db_controller.get_departments(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "services /départements", db_model_queryset
                )
                console.print(table)
                print("Aucun autres services")
            else:
                printer.print_message(
                    "error",
                    self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"],
                )
        return self.db_controller.get_departments(self.session)

    def get_department(self, department_id):
        """
        Description: Vue dédiée à obtenir le département /service dont l'id est indiqué en entrée.
        Parameters:
        - department_id: une chaine libre qui identifie un département.
        """
        return self.db_controller.get_department(self.session, department_id)

    def add_department(self, department):
        """
        Description: Vue dédiée à ajouter un département /service.
        Parameters:
        - department: une instance du modèle de classe Collaborator_Department.
        """
        return self.db_controller.add_department(self.session, department)

    def delete_department(self, department_id):
        """
        Description: Vue dédiée à supprimer un département /service.
        Parameters:
        - department_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_department(self.session, department_id)

    def update_department(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un departement /service.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_department(self.session, custom_dict)
