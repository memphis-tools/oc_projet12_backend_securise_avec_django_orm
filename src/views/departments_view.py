"""
vue departments
"""


class DepartmentsView:
    """
    Description: une classe dédiée à servir les vues pour les departments /services de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.session = session

    def get_departments(self):
        """
        Description: vue dédiée à "méthode GET".
        """
        return self.db_controller.get_departments(self.session)

    def get_department(self, department_id):
        """
        Description: Vue dédiée à obtenir le département /service dont l'id est indiqué en entrée.
        Parameters:
        - department_id: une chaine libre qui identifie un département.
        """
        return self.db_controller.get_department(self.session, department_id)

    def add_department(self, department):
        """
        Description: Vue dédiée à ajouter un département /service.
        Parameters:
        - department: une instance du modèle de classe UserDepartment.
        """
        return self.db_controller.add_department(self.session, department)

    def delete_department(self, department_id):
        """
        Description: Vue dédiée à supprimer un département /service.
        Parameters:
        - department_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_department(self.session, department_id)

    def update_department(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un departement /service.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_department(self.session, custom_dict)
