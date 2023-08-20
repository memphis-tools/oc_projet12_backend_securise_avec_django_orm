"""
Description:
Dédié aux parcours des fichiers '.csv' constituées à partir des requêtes aux API externes.
Ce controleur est utilisé par le seul client console dédié à l'initialisation ('src/clients/init_console.py').
"""
import csv
import json
from rich import print
from unidecode import unidecode
try:
    from src.controllers import database_initializer_controller
    from src.models import models
    from src.settings import settings
    from src.utils import utils
    from src.external_datas.make_external_api_call_for_region_based_on_int_code import get_region_name_from_insee_open_api
except ModuleNotFoundError:
    from controllers import database_initializer_controller
    from models import models
    from settings import settings
    from utils import utils
    from external_datas.make_external_api_call_for_region_based_on_int_code import get_region_name_from_insee_open_api


class CsvFilesInitController:
    """
    Description:
    (...)
    """
    def __init__(self):
        """
        Description:
        (...)
        """
        self.csv_file_jsonified = {}

    def set_a_location_id(self, pays, region, code_postal, nom_raison_sociale):
        location_custom_id = utils.set_a_location_custom_id(pays, region, code_postal, nom_raison_sociale)
        return location_custom_id

    def set_a_company_id(self, nom_raison_sociale, siren, siret, date_debut_activite, ville):
        company_custom_id = utils.set_a_company_custom_id(nom_raison_sociale, siren, siret, date_debut_activite, ville)
        return company_custom_id

    def make_locations_and_companies_with_api_data(self, api_data):
        location_attributes_from_api_list = [
            "location_id",
            "adresse",
            "complement_adresse",
            "cedex",
            "code_postal",
            "commune",
            "region",
            "pays",
        ]

        company_api_from_model_dict = {
          "siren":"company_registration_number",
          "siret":"company_subregistration_number",
          "nom_raison_sociale":"company_name",
          "activite_principale":"activite_principale",
          "date_debut_activite":"date_debut_activite",
          "tranche_effectif_salarie":"tranche_effectif_salarie",
        }
        # on parcourt un dictionnaire type {"siren1":{entreprise1}, "siren2":{entreprise2}, ...}
        temp_insee_dict = {}

        new_company_dict = {}
        new_location_dict = {}
        new_location_dict["pays"] = "France"
        for k, v in api_data.items():
            if k in location_attributes_from_api_list:
                if k == "region":
                    # l'API nous aura renvoyé une région avec un entier (v est içi un id, un entier)
                    if v in temp_insee_dict.keys():
                        new_location_dict[k] = temp_insee_dict[v]
                    else:
                        region_name = get_region_name_from_insee_open_api(v)
                        new_location_dict[k] = unidecode(region_name)
                        # on met en mémoire au cas d'autres localités ont la meme région
                        temp_insee_dict[v] = region_name
                elif k == "code_postal":
                    new_location_dict[k] = int(v)
                elif k == "commune":
                    new_location_dict["ville"] = v
                elif k == "cedex":
                    if v == "":
                        new_location_dict["cedex"] = 0
                    else:
                        new_location_dict["cedex"] = v
                else:
                    new_location_dict[k] = v
            elif k in company_api_from_model_dict.keys():
                if k == "siret":
                    new_company_dict[company_api_from_model_dict[k]] = v[-5:]
                elif k == "tranche_effectif_salarie":
                    if not k.isdigit():
                        new_company_dict[company_api_from_model_dict[k]] = 0
                else:
                    new_company_dict[company_api_from_model_dict[k]] = v
        return (new_location_dict, new_company_dict)

    def append_external_datas_to_dev_database(self, api_data_dict):
        try:
            controller = database_initializer_controller.DatabaseInitializerController(f"{settings.DEV_DATABASE_NAME}")
            session_on_dev_db = controller.return_session(
                f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=f"{settings.DEV_DATABASE_NAME}"
            )
            controller = database_initializer_controller.DatabaseInitializerController(f"{settings.TEST_DATABASE_NAME}")
            session_on_test_db = controller.return_session(
                f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=f"{settings.TEST_DATABASE_NAME}"
            )
            for api_data in api_data_dict.values():
                (new_location_dict, new_company_dict) = self.make_locations_and_companies_with_api_data(api_data)

                new_location_id = self.set_a_location_id(
                    new_location_dict["pays"],
                    new_location_dict["region"],
                    new_location_dict["code_postal"],
                    new_company_dict["company_name"]
                )

                new_company_id = self.set_a_company_id(
                    new_company_dict["company_name"],
                    new_company_dict["company_registration_number"],
                    new_company_dict["company_subregistration_number"],
                    new_company_dict["date_debut_activite"],
                    new_location_dict["ville"]
                )

                id = utils.get_location_id_from_location_custom_id(session_on_dev_db, new_location_id)
                if not id:
                    new_location_dict["location_id"] = new_location_id.upper()
                    new_location_object = models.Location(**new_location_dict)
                    session_on_dev_db.add(new_location_object)
                    session_on_dev_db.commit()
                    session_on_dev_db.refresh(new_location_object)
                    new_company_dict["location_id"] = new_location_object.id
                    new_company_dict["company_id"] = new_company_id
                else:
                    new_company_dict["location_id"] = id
                    new_company_dict["company_id"] = new_company_id
                new_company_object = models.Company(**new_company_dict)
                session_on_dev_db.add(new_company_object)
                session_on_dev_db.commit()
                # session_on_dev_db.expunge(new_location_object)
                # session_on_dev_db.expunge(new_company_object)

                id = utils.get_location_id_from_location_custom_id(session_on_test_db, new_location_id)
                if not id:
                    new_location_object = models.Location(**new_location_dict)
                    session_on_test_db.add(new_location_object)
                    session_on_test_db.commit()
                    session_on_test_db.refresh(new_location_object)
                    new_company_dict["location_id"] = new_location_object.id
                    new_company_dict["company_id"] = new_company_id
                else:
                    new_company_dict["location_id"] = id
                    new_company_dict["company_id"] = new_company_id
                new_company_object = models.Company(**new_company_dict)
                session_on_test_db.add(new_company_object)
                session_on_test_db.commit()


            session_on_dev_db.close()
            session_on_test_db.close()
        except Exception:
            session_on_dev_db.close()
            session_on_test_db.close()

    def read_a_csv_file_and_return_data_as_json(self, csv_filename=""):
        """
        Description:
        (...)
        """
        with open(csv_filename, newline='') as csv_file_handler:
            csv_reader = csv.DictReader(csv_file_handler)
            for rows in csv_reader:
                #assuming a column named 'No'
                #to be the primary key
                key = rows['siren']
                self.csv_file_jsonified[key] = rows

        self.append_external_datas_to_dev_database(api_data_dict = self.csv_file_jsonified)
        return True
