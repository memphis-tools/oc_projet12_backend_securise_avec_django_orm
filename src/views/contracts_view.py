"""
vue contrats
"""


class ContractsView:
    """
    Description: une classe dédiée à servir les vues pour les contrats de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_contracts(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        if user_query_filters_args != "":
            return self.db_controller.get_filtered_contracts(self.session, user_query_filters_args[0])
        return self.db_controller.get_contracts(self.session)

    def get_contract(self, contract_id):
        """
        Description: Vue dédiée à obtenir le contrat dont l'id est indiqué en entrée.
        Parameters:
        - contract_id: une chaine libre qui identifie un contrat.
        """
        return self.db_controller.get_contract(self.session, contract_id)

    def add_contract(self, contract):
        """
        Description: Vue dédiée à ajouter un contrat.
        Parameters:
        - contract: une instance du modèle de classe Contract.
        """
        return self.db_controller.add_contract(self.session, contract)

    def delete_contract(self, contract_id):
        """
        Description: Vue dédiée à supprimer un contrat.
        Parameters:
        - contract_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_contract(self.session, contract_id)

    def update_contract(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un contrat.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_contract(self.session, custom_dict)
