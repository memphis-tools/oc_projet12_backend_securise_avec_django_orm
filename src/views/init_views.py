"""
Description
On fournit une vue dédiée à s'interfacer entre le client et controleur suivants:
- le client console 'src/clients/init_console.py'
- le controleur 'src/controllers/csv_file_read_controller.py'.
"""
try:
    from src.controllers.csv_file_read_controller import CsvFilesInitController
    from src.settings import settings
except ModuleNotFoundError:
    from controllers.csv_file_read_controller import CsvFilesInitController
    from settings import settings


class InitAppViews:
    """
    Description:
    Classe dédiée à effectuer l'interfaçage entre client et contrôleur.
    """

    def __init__(self):
        """
        Description:
        Vue dédiée à initialiser le(s) base(s) de données.
        Appelée seulement lors de l'initialisation de l'appli (par 'src/clients/init_console.py')
        """
        self.init_controller = CsvFilesInitController()

    def read_a_csv_file_and_return_data_as_json(self, csv_filename):
        """
        Description:
        Appelée par l'init_console (InitAppliConsole).
        Retourne une structure de données qui recense tous les enregistrements d'un fichier .csv
        """
        return self.init_controller.read_a_csv_file_and_return_data_as_json(
            csv_filename
        )

    def append_external_datas_to_dev_and_test_databases(self, csv_file_jsonified):
        """
        Description:
        Appelée par l'init_console (InitAppliConsole).
        On va enregistrer une à une les entreprises.
        Pour chaque entreprise vient une localité: si elle existe on ajoute la correspondance,
        Si elle n'existe pas, on la crée. On va donc créer en bases des localités et des entreprises.
        On enregistre ces entreprises dans les 2 seules bases DEV et TEST.
        Retourne True si les enregistrements ont été réalisés.
        """
        return self.init_controller.append_external_datas_to_dev_and_test_databases(
            api_data_dict=csv_file_jsonified
        )
