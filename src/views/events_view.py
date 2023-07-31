"""
vue évènements
"""


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

    def get_events(self):
        """
        Description: vue dédiée à "méthode GET".
        """
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
