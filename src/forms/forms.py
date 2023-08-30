"""
Description:
Classe dédiée à la création de modèles. Utilisée pour le dialogue avec l'utilisateur de l'application.
Noter que les formulaires vont appeler les validateurs ('src/validators/data_syntax/fr/validators.py').
Dans les formulaires on parcourt les attributs à renseigner et on recherche dynamiquement le validateur:
eval(f"validators.is_{key}_valid")(item)
"""
import sys
from datetime import datetime
import maskpass
from rich.prompt import Prompt

try:
    from src.controllers import infos_data_controller
    from src.exceptions import exceptions
    from src.languages import language_bridge
    from src.external_datas.make_external_api_call_for_ville_based_on_code_postal import (
        get_town_name_region_name_and_population_from_insee_open_api,
    )
    from src.printers import printer
    from src.settings import settings, logtail_handler
    from src.utils import utils
    from src.validators.data_syntax.fr import validators
except ModuleNotFoundError:
    from controllers import infos_data_controller
    from exceptions import exceptions
    from languages import language_bridge
    from external_datas.make_external_api_call_for_ville_based_on_code_postal import (
        get_town_name_region_name_and_population_from_insee_open_api,
    )
    from printers import printer
    from settings import settings, logtail_handler
    from utils import utils
    from validators.data_syntax.fr import validators


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


def display_help(key, item, value):
    """
    Description:
    Appelée par fullfill_form(...).
    On isole cette fonctionnalité dédiée à proposer des valeurs à saisir.
    La présentation est içi une popup de Tkinter.
    """
    if key == "complement_adresse":
        if item == "?" or item == "help":
            infos_data_controller.display_info_data_thin_window("types_voies")
            item = Prompt.ask(f"{value}: ")
    elif key == "employee_role":
        if item == "?" or item == "help":
            infos_data_controller.display_info_data_medium_window("metiers")
            item = Prompt.ask(f"{value}: ")
    return item


def search_and_submit_a_town_name(code_postal):
    """
    Description:
    Si la variable "settings.INTERNET_CONNECTION" est True alors on interroge une API externe.
    Içi on appel l'API ouverte 'api-adresse.data.gouv.fr'.
    A partir du code postal saisi on propose de retenir le nom de ville trouvé.
    Si ville trouvée alors on connait le nom et on peut retenir le pays comme étant la France (par exemple).
    """
    town_name, region_name, population = get_town_name_region_name_and_population_from_insee_open_api(code_postal)
    return (town_name, region_name, population)


def display_any_error_message(key):
    """
    Description:
    Appelée par fonction fullfill_form.
    Selon la clef en erreur, un message spécifique est adressé ou non.
    """
    if key == "complement_adresse" or key == "employee_role":
        message = APP_DICT.get_appli_dictionnary()["FORM_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)

        message = APP_DICT.get_appli_dictionnary()["FORM_GET_MORE_INFO_ABOUT_A_NULLABLE_FIELD"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)

        message = APP_DICT.get_appli_dictionnary()["FORM_GET_MORE_INFO_ABOUT_VALID_VALUES"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    else:
        message = APP_DICT.get_appli_dictionnary()["FORM_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)

        message = APP_DICT.get_appli_dictionnary()["FORM_GET_MORE_INFO_ABOUT_A_NULLABLE_FIELD"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    return False


def validate_key(custom_dict, key, item):
    """
    Description:
    Appelée par fonction fullfill_form.
    On fait appel aux "validators" (validators/data_syntax/fr/validators.py) pour controler la saisie.
    """
    try:
        # si quelque chose a été saisi on vérifie si ça respecte la /les valeur(s) attendue(s).
        if key == "remain_amount_to_pay":
            eval(f"validators.is_{key}_valid")(item, custom_dict["full_amount_to_pay"])
        else:
            eval(f"validators.is_{key}_valid")(item)
        custom_dict[key] = item
    except exceptions.ContractAmountToPayException:
        message = APP_DICT.get_appli_dictionnary()["EXCEPTION_CONTRACT_AMOUNT_TO_PAY"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["UNEXPECTED_VALUE_IN_FORM"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    return custom_dict


def fullfill_form(custom_dict, expected_attributes_dict):
    """
    Description:
    Faire remplir interractivement un formulaire par l'utilisateur.
    Paramètres:
    - expected_attributes_dict: un dictionnaire, il représente les attributs attendus
    """
    while not len(custom_dict) == len(expected_attributes_dict):
        for key, value in expected_attributes_dict.items():
            if key not in custom_dict.keys():
                item = Prompt.ask(f"{value}: ")
                # 2 cas spécifiques avec popup prévue
                if key in ["complement_adresse", "employee_role"]:
                    item = display_help(key, item, value)
                if key == "code_postal":
                    pays = ""
                    ville, region, population = search_and_submit_a_town_name(item)
                    if ville and ville is not None:
                        custom_dict["code_postal"] = item
                        custom_dict["ville"] = ville
                        custom_dict["region"] = region
                        custom_dict["pays"] = f"{settings.DEFAULT_COUNTRY}"
                        custom_dict["population"] = population
                else:
                    # vérifier si quelque chose a été saisi
                    if item.strip() != "":
                        custom_dict = validate_key(custom_dict, key, item)
                        break
                    else:
                        display_any_error_message(key)
                        break
    return custom_dict


def submit_a_location_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une localité.
    On peut en outre ainsi éviter d'avoir à la saisir.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_LOCATION"]
        )
        try:
            custom_id = Prompt.ask("id localité: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_location_create_form(location_id, custom_dict={}):
    """
    Description: Fonction dédiée à créer une localité. A la fois pour une entreprise ou un évènement.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "location_id": "id (chaine libre)",
            "adresse": "adresse",
            "complement_adresse": "complement_adresse",
            "code_postal": "code_postal",
            "ville": "ville",
            "region": "region",
            "pays": "pays",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_LOCATION"]
        )
        try:
            if location_id:
                custom_dict["location_id"] = location_id
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_company_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une entreprise.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_COMPANY"]
        )
        try:
            custom_id = Prompt.ask("id entreprise: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_company_create_form(company_location_id, custom_dict={}):
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut location_id est attendu pour respecter le modèle.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "company_id": "id entreprise (chaine libre)",
            "company_registration_number": "siren",
            "company_subregistration_number": "nic",
            "company_name": "nom entreprise",
            "activite_principale": "activité principale (code APE etc)",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_COMPANY"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    custom_dict["location_id"] = company_location_id
    custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_client_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un client.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_CLIENT"]
        )
        try:
            custom_id = Prompt.ask("id client: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_client_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut company_id est attendu pour respecter le modèle.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "client_id": "id (chaine libre)",
            "civility": "civilité",
            "first_name": "prénom",
            "last_name": "nom",
            "employee_role": "fonction",
            "email": "email",
            "telephone": "telephone",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_CLIENT"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_collaborator_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un collaborateur.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_COLLABORATOR"]
        )
        try:
            custom_id = Prompt.ask("id collaborator: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_collaborator_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un collaborateur /utilisateur, de l'entreprise.
    Noter que 2 clefs étrangères 'department id' et 'role id' sont attendues.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "registration_number": "matricule employé",
            "username": "nom utilisateur",
            "department_id": "service ccial, gest ou supp (OC12_COMMERCIAL, OC12_GESTION, OC12_SUPPORT)",
            "role_id": "role man ou emp (MANAGER, EMPLOYEE)",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_COLLABORATOR"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_collaborator_role_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un role.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_COLLABORATOR_ROLE"]
        )
        try:
            custom_id = Prompt.ask("id role: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_collaborator_role_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un nouveau rôle pour un collaborateur de l'entreprise.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "role_id": "role (chaine libre)",
            "name": "name (MANAGER, EMPLOYEE, etc)",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_COLLABORATOR_ROLE"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_collaborator_department_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un département /service.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_COLLABORATOR_DEPARTMENT"]
        )
        try:
            custom_id = Prompt.ask("id service/département: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_collaborator_department_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un nouveau service /département de l'entreprise.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "department_id": "id service (chaine de caractères libre)",
            "name": "service (examples: OC12_COMMERCIAL, OC12_GESTION, ...)",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_COLLABORATOR_DEPARTMENT"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_collaborator_new_password_get_form(old_password="", new_password=""):
    """
    Deescription: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un département /service.
    """
    if new_password == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_COLLABORATOR_PASSWORD"]
        )
        try:
            old_password = maskpass.askpass(prompt="Ancien mot de passe: ")
            new_password = maskpass.askpass(prompt="Nouveau mot de passe: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return (old_password, new_password)


def submit_a_contract_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un contrat.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_CONTRACT"]
        )
        try:
            custom_id = Prompt.ask("id contrat: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_contract_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 2 clefs étrangères 'client id' et 'collaborator id' sont attendues.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "contract_id": "id",
            "full_amount_to_pay": "total à payer",
            "remain_amount_to_pay": "total restant à payer",
            "status": "statut ('signed', 'unsigned', 'canceled')",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_CONTRACT"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def submit_a_event_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un évènement.
    """
    if custom_id == "":
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["LOOKUP_A_EVENT"]
        )
        try:
            custom_id = Prompt.ask("id evènement: ")
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["LOOKUP_ABORTED"]
            )
            sys.exit(0)
    return custom_id


def submit_a_event_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 4 clefs étrangères 'contract id', 'client id', 'collaborator id', et 'location id' sont attendues.
    """
    if custom_dict == {}:
        expected_attributes_dict = {
            "event_id": "id",
            "title": "titre",
            "attendees": "public max attendu",
            "notes": "description",
            "event_start_date": "date début (format: 2023-04-12 15:00:00)",
            "event_end_date": "date début (format: 2023-04-15 22:00:00)",
        }
        printer.print_message(
            "info", APP_DICT.get_appli_dictionnary()["CREATE_A_EVENT"]
        )
        try:
            while not len(custom_dict) == len(expected_attributes_dict):
                fullfill_form(custom_dict, expected_attributes_dict)
        except KeyboardInterrupt:
            printer.print_message(
                "info", APP_DICT.get_appli_dictionnary()["CREATION_ABORTED"]
            )
            sys.exit(0)
    if "creation_date" not in custom_dict.keys():
        custom_dict["creation_date"] = f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}'
    return custom_dict


def respect_flake8():
    # validators module is used, dynamically: on déclare pour respect du flake8
    validators.is_adresse_valid("adresse")
    return None
