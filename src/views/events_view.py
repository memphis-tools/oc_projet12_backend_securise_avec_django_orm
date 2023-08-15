"""
vue évènements
"""
from rich.console import Console
try:
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils

class EventsView:
    """
    Description: une classe dédiée à servir les vues pour les évènements de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_events(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(self.session, user_query_filters_args[0], "Event")
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data("events", db_model_queryset)
                    console.print(table)
                    print("Aucuns autres évènements")
                else:
                    print("Aucun évènement trouvé")
            except Exception as error:
                print(f"Echec de la requête: {error}")
                raise Exception()
        else:
            db_model_queryset = self.db_controller.get_events(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data("events", db_model_queryset)
                console.print(table)
                print("Aucun autres évènements")
            else:
                print("Aucun évènement trouvé")

        return self.db_controller.get_events(self.session)

    def get_event(self, event_id):
        """
        Description: Vue dédiée à obtenir l'évènement dont l'id est indiqué en entrée.
        Parameters:
        - event_id: une chaine libre qui identifie un évènement.
        """
        return self.db_controller.get_event(self.session, event_id)

    def add_event(self, event):
        """
        Description: Vue dédiée à ajouter un évènement.
        Parameters:
        - event: une instance du modèle de classe Event.
        """
        return self.db_controller.add_event(self.session, event)

    def delete_event(self, event_id):
        """
        Description: Vue dédiée à supprimer un évènement.
        Parameters:
        - event_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_event(self.session, event_id)

    def update_event(self, current_user_collaborator_id, custom_dict):
        """
        Description: vue dédiée à mettre à jour un évènement.
        Parameters:
        - current_user_collaborator_id: l'id (la clef primaire, 'pas un custom id')
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_event(self.session, current_user_collaborator_id, custom_dict)
