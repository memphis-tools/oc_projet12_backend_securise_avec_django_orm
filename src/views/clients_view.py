"""
vue clients
"""
from rich.console import Console
try:
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils


class ClientsView:
    """
    Description: une classe dédiée à servir les vues pour les clients de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_clients(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(self.session, user_query_filters_args[0], "Client")
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data("clients", db_model_queryset)
                    console.print(table)
                    print("Aucun autres clients")
                else:
                    print("Aucun client trouvé")
            except Exception as error:
                print(f"Echec de la requête: {error}")
                raise Exception()
        else:
            db_model_queryset = self.db_controller.get_clients(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data("clients", db_model_queryset)
                console.print(table)
                print("Aucun autres clients")
            else:
                print("Aucun client trouvé")
        return self.db_controller.get_clients(self.session)

    def get_client(self, client_id):
        """
        Description: vue dédiée à obtenir un client de l'entreprise.
        """
        return self.db_controller.get_client(self.session, client_id)

    def add_client(self, client):
        """
        Description: vue dédiée à enregistrer un client.
        Parameters:
        - client: une instance valide de la classe Client.
        """
        return self.db_controller.add_client(self.session, client)

    def delete_client(self, client_id):
        """
        Description: vue dédiée à supprimer un client de l'entreprise.
        Parameters:
        - client_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_client(self.session, client_id)

    def update_client(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un client.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_client(self.session, custom_dict)
