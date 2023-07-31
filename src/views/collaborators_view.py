"""
vue collaborateurs
"""


class CollaboratorsView:
    """
    Description: une classe dédiée à servir les vues pour les collaborateurs de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_collaborators(self):
        """
        Description: vue dédiée à "méthode GET".
        """
        return self.db_controller.get_collaborators(self.session)

    def get_collaborator(self, collaborator_id):
        """
        Description: Vue dédiée à obtenir le collaborateur dont l'id est indiqué en entrée.
        Parameters:
        - collaborator_id: une chaine libre qui identifie un collaborateur.
        """
        return self.db_controller.get_collaborator(self.session, collaborator_id)

    def add_collaborator(self, collaborator):
        """
        Description: Vue dédiée à ajouter un collaborateur de l'entreprise.
        Parameters:
        - collaborator: une instance du modèle de classe User.
        """
        return self.db_controller.add_collaborator(self.session, collaborator)

    def delete_collaborator(self, collaborator):
        """
        Description: Vue dédiée à supprimer un collaborateur de l'entreprise.
        Parameters:
        - collaborator: une instance du modèle de classe User.
        """
        return self.db_controller.delete_collaborator(self.session, collaborator)
