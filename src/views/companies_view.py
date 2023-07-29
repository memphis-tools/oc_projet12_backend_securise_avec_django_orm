"""
vue entreprises
"""


class CompaniesView:
    """
    Description: une classe dédiée à servir les vues pour les entreprises clientes.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_companies(self):
        """
        Description: vue dédiée à obtenir les entreprises connues.
        """
        return self.db_controller.get_companies(self.session)

    def get_company(self, company_id):
        """
        Description: Vue dédiée à obtenir l'entreprise dont l'id est indiqué en entrée.
        Parameters:
        - company_id: une chaine libre qui identifie une entreprise.
        """
        return self.db_controller.get_company(self.session)

    def add_company(self, company):
        """
        Description: Vue dédiée à ajouter une entreprise.
        Parameters:
        - company: une instance du modèle de classe Company.
        """
        return self.db_controller.add_company(self.session, company)
