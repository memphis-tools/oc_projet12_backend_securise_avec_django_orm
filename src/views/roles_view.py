"""
vue roles
"""


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

    def get_roles(self):
        """
        Description: vue dédiée à "méthode GET".
        """
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
        - role: une instance du modèle de classe UserRole.
        """
        return self.db_controller.add_role(self.session, role)

    def delete_role(self, role):
        """
        Description: Vue dédiée à supprimer un role.
        Parameters:
        - role: une instance du modèle de classe UserRole.
        """
        return self.db_controller.delete_role(self.session, role)
