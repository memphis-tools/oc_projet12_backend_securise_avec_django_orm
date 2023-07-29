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