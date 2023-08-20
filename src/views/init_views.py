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

    def __init__(self, db_name=f"{settings.DEV_DATABASE_NAME}"):
        """
        Description:
        Vue dédiée à initialiser le(s) base(s) de données.
        Appelée seulement lors de l'initialisation de l'appli (par 'src/clients/init_console.py')
        """
        self.init_controller = CsvFilesInitController()

    def read_a_csv_file_and_return_data_as_json(self, csv_filename):
        """
        Description:
        (...)
        """
        return self.init_controller.read_a_csv_file_and_return_data_as_json(csv_filename)
