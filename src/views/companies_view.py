"""
vue entreprises
"""
from rich.console import Console

try:
    from src.utils import utils
except ModuleNotFoundError:
    from utils import utils


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

    def get_companies(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les entreprises connues.
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Company"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "entreprises", db_model_queryset
                    )
                    console.print(table)
                    print("Aucunes autres entreprises")
                else:
                    print("Aucune entreprise trouvée")
            except Exception as error:
                print(f"Echec de la requête: {error}")
                raise Exception()
        else:
            db_model_queryset = self.db_controller.get_companies(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "entreprises", db_model_queryset
                )
                console.print(table)
                print("Aucunes autres entreprises")
            else:
                print("Aucune entreprise trouvée")
        return self.db_controller.get_companies(self.session)

    def get_company(self, company_id):
        """
        Description: Vue dédiée à obtenir l'entreprise dont l'id est indiqué en entrée.
        Parameters:
        - company_id: une chaine libre qui identifie une entreprise.
        """
        return self.db_controller.get_company(self.session, company_id)

    def add_company(self, company):
        """
        Description: Vue dédiée à ajouter une entreprise.
        Parameters:
        - company: une instance du modèle de classe Company.
        """
        return self.db_controller.add_company(self.session, company)

    def delete_company(self, company_id):
        """
        Description: Vue dédiée à supprimer une entreprise.
        Parameters:
        - company_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_company(self.session, company_id)

    def update_company(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour une entreprise.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_company(self.session, custom_dict)
