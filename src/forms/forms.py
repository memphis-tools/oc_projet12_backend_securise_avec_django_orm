"""
Classe dédiée aux mises à jour des modèles. Utilisée pour le dialogue avec l'utilisateur de l'application.
"""
import sys
import maskpass
from rich import print
from rich.prompt import Prompt
try:
    from src.validators.data_syntax.fr import validators
except ModuleNotFoundError:
    from validators.data_syntax.fr import validators


def submit_a_location_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une localité.
    On peut en outre ainsi éviter d'avoir à la saisir.
    """
    if custom_id == "":
        print("[bold blue][LOCATION LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id localité: ")
        except KeyboardInterrupt:
            print("[bold red][LOCATION LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_location_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer une localité. A la fois pour une entreprise ou un évènement.
    """
    if custom_dict == {}:
        location_expected_attributes_dict = {
            "location_id": "id (chaine libre)",
            "adresse": "adresse",
            "complement_adresse": "complement_adresse",
            "code_postal": "code_postal",
            "ville": "ville",
            "pays": "pays",
        }
        print("[bold blue][LOCATION CREATION][/bold blue]")
        try:
            while not len(custom_dict) == len(location_expected_attributes_dict):
                for key, value in location_expected_attributes_dict.items():
                    if key not in custom_dict.keys():
                        item = Prompt.ask(f"{value}: ")
                        if item.strip() != "":
                            try:
                                eval(f"validators.is_{key}_valid")(item)
                                custom_dict[key] = item
                            except:
                                print(f"[bold red]{item}[/bold red] not valid for {key}")
                                continue
        except KeyboardInterrupt:
            print("[bold red][LOCATION CREATION][/bold red] Creation aborted")
            sys.exit(0)
    return custom_dict


def submit_a_company_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une entreprise.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """
    if custom_id == "":
        print("[bold blue][COMPANY LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id entreprise: ")
        except KeyboardInterrupt:
            print("[bold red][COMPANY LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_company_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut location_id est attendu pour respecter le modèle.
    """
    if custom_dict == {}:
        company_expected_attributes_dict = {
            "company_id": "id entreprise (chaine libre)",
            "company_name": "nom entreprise",
            "company_registration_number": "siren",
            "company_subregistration_number": "nic",
        }
        print("[bold blue][COMPANY CREATION][/bold blue]")
        try:
            while not len(custom_dict) == len(company_expected_attributes_dict):
                for key, value in company_expected_attributes_dict.items():
                    if key not in custom_dict.keys():
                        item = Prompt.ask(f"{value}: ")
                        if item.strip() != "":
                            try:
                                eval(f"validators.is_{key}_valid")(item)
                                custom_dict[key] = item
                            except:
                                print(f"[bold red]{item}[/bold red] not valid for {key}")
                                continue
        except KeyboardInterrupt:
            print("[bold red][COMPANY CREATION][/bold red] Creation aborted")
            sys.exit(0)
    return custom_dict


def submit_a_client_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un client.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """
    if custom_id == "":
        print("[bold blue][CLIENT LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id client: ")
        except KeyboardInterrupt:
            print("[bold red][CLIENT LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_client_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut company_id est attendu pour respecter le modèle.
    """
    if custom_dict == {}:
        client_expected_attributes_dict = {
            "client_id": "id (chaine libre)",
            "civility": "civilité",
            "first_name": "prénom",
            "last_name": "nom",
            "employee_role": "fonction",
            "email": "email",
            "telephone": "telephone",
        }
        print("[bold blue][CLIENT CREATION][/bold blue]")
        try:
            while not len(custom_dict) == len(client_expected_attributes_dict):
                for key, value in client_expected_attributes_dict.items():
                    if key not in custom_dict.keys():
                        item = Prompt.ask(f"{value}: ")
                        if item.strip() != "":
                            try:
                                eval(f"validators.is_{key}_valid")(item)
                                custom_dict[key] = item
                            except:
                                print(f"[bold red]{item}[/bold red] not valid for {key}")
                                continue
        except KeyboardInterrupt:
            print("[bold red][CLIENT CREATION][/bold red] Creation aborted")
            sys.exit(0)
    return custom_dict


def submit_a_collaborator_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un collaborateur.
    """
    if custom_id == "":
        print("[bold blue][ROLE LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("matricule employé: ")
        except KeyboardInterrupt:
            print("[bold red][ROLE LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_collaborator_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un collaborateur /utilisateur, de l'entreprise.
    Noter que 2 clefs étrangères 'department id' et 'role id' sont attendues.
    """
    if custom_dict == {}:
        collaborator_expected_attributes_dict = {
            "registration_number": "matricule employé",
            "username": "nom utilisateur",
            "department": "service (OC12_COMMERCIAL, OC12_GESTION, OC12_SUPPORT)",
            "role": "role (MANAGER, EMPLOYEE)",
        }
        print("[bold blue][COLLABORATOR CREATION][/bold blue]")
        try:
            for key, value in collaborator_expected_attributes_dict.items():
                item = Prompt.ask(f"{value}: ")
                try:
                    eval(f"validators.is_{key}_valid")(item)
                    custom_dict[key] = item
                except:
                    print(f"[bold red]{item}[/bold red] not valid for {key}")
                    continue
        except KeyboardInterrupt:
            print("[bold red][COLLABORATOR CREATION][/bold red] Creation aborted")
            sys.exit(0)
    return custom_dict


def submit_a_collaborator_role_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un role.
    """
    if custom_id == "":
        print("[bold blue][ROLE LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id role: ")
        except KeyboardInterrupt:
            print("[bold red][ROLE LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_collaborator_role_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un nouveau rôle pour un collaborateur de l'entreprise.
    """
    if custom_dict == {}:
        collaborator_role_expected_attributes_dict = {
            "role_id": "role (chaine libre)",
            "name": "name (MANAGER, EMPLOYEE, etc)",
        }
        print("[bold blue][COLLABORATOR ROLE CREATION][/bold blue]")
        try:
            for key, value in collaborator_role_expected_attributes_dict.items():
                item = Prompt.ask(f"{value}: ")
                try:
                    eval(f"validators.is_{key}_valid")(item)
                    custom_dict[key] = item
                except:
                    print(f"[bold red]{item}[/bold red] not valid for {key}")
                    continue
        except KeyboardInterrupt:
            print(
                "[bold red][COLLABORATOR ROLE CREATION][/bold red] Creation aborted"
            )
            sys.exit(0)
    return custom_dict


def submit_a_collaborator_department_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un département /service.
    """
    if custom_id == "":
        print("[bold blue][DEPARTMENT LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id service/département: ")
        except KeyboardInterrupt:
            print("[bold red][DEPARTMENT LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_collaborator_department_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un nouveau service /département de l'entreprise.
    """
    if custom_dict == {}:
        collaborator_department_expected_attributes_dict = {
            "department_id": "id service (chaine de caractères libre)",
            "department": "service (examples: OC12_COMMERCIAL, OC12_GESTION, ...)",
        }
        print("[bold blue][COLLABORATOR DEPARTMENT CREATION][/bold blue]")
        try:
            for key, value in collaborator_department_expected_attributes_dict.items():
                item = Prompt.ask(f"{value}: ")
                try:
                    eval(f"validators.is_{key}_valid")(item)
                    custom_dict[key] = item
                except:
                    print(f"[bold red]{item}[/bold red] not valid for {key}")
                    continue
        except KeyboardInterrupt:
            print(
                "[bold red][COLLABORATOR DEPARTMENT CREATION][/bold red] Creation aborted"
            )
            sys.exit(0)
    return custom_dict


def submit_a_collaborator_new_password_get_form(old_password="", new_password=""):
    """
    Deescription: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un département /service.
    """
    if new_password == "":
        print("[bold blue][COLLABORATOR PASSWORD LOOKUP][/bold blue]")
        try:
            old_password = maskpass.askpass(prompt="Ancien mot de passe: ")
            new_password = maskpass.askpass(prompt="Nouveau mot de passe: ")
        except KeyboardInterrupt:
            print("[bold red][DEPARTMENT LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return (old_password, new_password)


def submit_a_contract_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un contrat.
    """
    if custom_id == "":
        print("[bold blue][CONTRACT LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id contrat: ")
        except KeyboardInterrupt:
            print("[bold red][CONTRACT LOOKUP][/bold red] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_contract_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 2 clefs étrangères 'client id' et 'collaborator id' sont attendues.
    """
    if custom_dict == {}:
        contract_expected_attributes_dict = {
            "contract_id": "id",
            "full_amount_to_pay": "total à payer",
            "remain_amount_to_pay": "total restant à payer",
            "status": "signé /conclu ('oui' ou 'non')",
        }
        print("[bold blue][CONTRACT CREATION][/bold blue]")
        try:
            for key, value in contract_expected_attributes_dict.items():
                item = Prompt.ask(f"{value}: ")
                if key == "status":
                    if item == "oui":
                        item = True
                    else:
                        item = False
                try:
                    eval(f"validators.is_{key}_valid")(item)
                    custom_dict[key] = item
                except:
                    print(f"[bold red]{item}[/bold red] not valid for {key}")
                    continue
        except KeyboardInterrupt:
            print("[bold green][CONTRACT CREATION][/bold green] Creation aborted")
            sys.exit(0)
    return custom_dict


def submit_a_event_get_form(custom_id=""):
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un évènement.
    """
    if custom_id == "":
        print("[bold blue][EVENT LOOKUP][/bold blue]")
        try:
            custom_id = Prompt.ask("id evènement: ")
        except KeyboardInterrupt:
            print("[bold green][EVENT LOOKUP][/bold green] Lookup aborted")
            sys.exit(0)
    return custom_id


def submit_a_event_create_form(custom_dict={}):
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 4 clefs étrangères 'contract id', 'client id', 'collaborator id', et 'location id' sont attendues.
    """
    if custom_dict == {}:
        event_expected_attributes_dict = {
            "event_id": "id",
            "title": "titre",
            "attendees": "public max attendu",
            "notes": "description",
            "event_start_date": "date début (format: 2023-04-12 15:00:00)",
            "event_end_date": "date début (format: 2023-04-15 22:00:00)",
        }
        print("[bold blue][EVENT CREATION][/bold blue]")
        try:
            for key, value in event_expected_attributes_dict.items():
                item = Prompt.ask(f"{value}: ")
                try:
                    eval(f"validators.is_{key}_valid")(item)
                    custom_dict[key] = item
                except:
                    print(f"[bold red]{item}[/bold red] not valid for {key}")
                    continue
        except KeyboardInterrupt:
            print("[bold green][EVENT CREATION][/bold green] Creation aborted")
            sys.exit(0)
    return custom_dict
