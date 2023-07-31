"""
vue localisations
"""


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

    def get_locations(self):
        """
        Description: vue dédiée à obtenir les localités.
        """
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
