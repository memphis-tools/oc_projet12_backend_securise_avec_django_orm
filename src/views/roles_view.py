"""
vue roles
"""
from rich.console import Console

try:
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils


class RolesView:
    """
    Description: une classe dédiée à servir les vues pour les roles de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
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
                    print("Aucuns autres roles")
                else:
                    print("Aucun role trouvé")
            except Exception as error:
                print(f"Echec de la requête: {error}")
                raise Exception()
        else:
            db_model_queryset = self.db_controller.get_roles(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "roles dans entreprise", db_model_queryset
                )
                console.print(table)
                print("Aucuns autres roles")
            else:
                print("Aucun role trouvé")
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
