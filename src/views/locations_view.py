"""
vue localisations
"""
from rich.console import Console
try:
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils


class LocationsView:
    """
    Description: une classe dédiée à servir les vues pour les localisations des évènements.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_locations(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les localités.
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(self.session, user_query_filters_args[0], "Location")
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data("lieu", db_model_queryset)
                    console.print(table)
                    print("Aucunes autres localités")
                else:
                    print("Aucune localité trouvée")
            except Exception as error:
                print(f"Echec de la requête: {error}")
                raise Exception()
        else:
            db_model_queryset = self.db_controller.get_locations(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data("lieu", db_model_queryset)
                console.print(table)
                print("Aucun autres localités")
            else:
                print("Aucune localité trouvée")
        return self.db_controller.get_locations(self.session)

    def get_location(self, location_id):
        """
        Description: vue dédiée à obtenir une localité.
        Parameters:
        - location_id: la clef primaire, un entier (en autoincrement) du modèle.
        """
        return self.db_controller.get_location(self.session, location_id)

    def add_location(self, location):
        """
        Description: vue dédiée à enregistrer une localité.
        Parameters:
        - location: une instance valide de la classe Location.
        """
        return self.db_controller.add_location(self.session, location)

    def delete_location(self, location_id):
        """
        Description: vue dédiée à supprimer une localité.
        Parameters:
        - location_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_location(self.session, location_id)

    def update_location(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour une localité.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_location(self.session, custom_dict)
