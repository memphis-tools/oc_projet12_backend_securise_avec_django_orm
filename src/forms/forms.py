"""
Classe dédiée aux mises à jour des modèles. Utilisée pour le dialogue avec l'utilisateur de l'application.
"""
import sys
from rich import print
from rich.prompt import Prompt


def submit_a_location_get_form():
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une localité.
    On peut en outre ainsi éviter d'avoir à la saisir.
    """

    print("[bold blue][LOCATION LOOKUP][/bold blue]")
    company_id_dict = {}
    try:
        location_id["id"] = Prompt.ask(f"id localité (ne rien saisir si inconnue): ")
    except KeyboardInterrupt:
        print("[bold green][LOCATION LOOKUP][/bold green] Lookup aborted")
        sys.exit(0)
    return company_id_dict


def submit_a_location_create_form():
    """
    Description: Fonction dédiée à créer une localité. A la fois pour une entreprise ou un évènement.
    """
    location_expected_attributes_dict = {
        "adresse": "adresse",
        "complement_adresse": "complement_adresse",
        "code_postal": "code_postal",
        "ville": "ville",
        "pays": "pays"
    }
    location_attributes_dict = {}
    print("[bold blue][LOCATION CREATION][/bold blue]")
    try:
        for key, value in location_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            location_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][LOCATION CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return location_attributes_dict


def submit_a_company_get_form():
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'une entreprise.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """

    print("[bold blue][COMPANY LOOKUP][/bold blue]")
    company_id = {}
    try:
        company_id["id"] = Prompt.ask(f"id entreprise (ne rien saisir si inconnue): ")
    except KeyboardInterrupt:
        print("[bold green][COMPANY LOOKUP][/bold green] Lookup aborted")
        sys.exit(0)
    return company_id


def submit_a_company_create_form():
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut location_id est attendu pour respecter le modèle.
    """

    company_expected_attributes_dict = {
        "company_id": "id entreprise",
        "company_name": "nom entreprise",
        "company_registration_number": "siren",
        "company_subregistration_number": "nic"
    }
    company_attributes_dict = {}
    print("[bold blue][COMPANY CREATION][/bold blue]")
    try:
        for key, value in company_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            company_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][COMPANY CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return company_attributes_dict


def submit_a_client_get_form():
    """
    Description: Fonction dédiée à permettre à l'utilisateur d'indiquer l'id d'un client.
    On peut en outre ainsi éviter la saisie d'une localisation, et de l'entreprise.
    """

    print("[bold blue][CLIENT LOOKUP][/bold blue]")
    client_id = {}
    try:
        client_id["id"] = Prompt.ask(f"id client (ne rien saisir si inconnu): ")
    except KeyboardInterrupt:
        print("[bold green][CLIENT LOOKUP][/bold green] Lookup aborted")
        sys.exit(0)
    return client_id


def submit_a_client_create_form():
    """
    Description: Fonction dédiée à créer une entreprise.
    Noter qu'un attribut company_id est attendu pour respecter le modèle.
    """

    client_expected_attributes_dict = {
        "civility": "civilité",
        "first_name": "prénom",
        "last_name": "nom",
        "employee_role": "fonction",
        "email": "email",
        "telephone": "telephone"
    }
    client_attributes_dict = {}
    print("[bold blue][CLIENT CREATION][/bold blue]")
    try:
        for key, value in client_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            client_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][CLIENT CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return client_attributes_dict


def submit_a_collaborator_create_form():
    """
    Description: Fonction dédiée à créer un collaborateur /utilisateur, de l'entreprise.
    Noter que 2 clefs étrangères 'department' et 'role' sont attendues.
    """
    collaborator_expected_attributes_dict = {
        "registration_number": "matricule employé",
        "username": "nom utilisateur",
        "department": "service (OC12_COMMERCIAL, OC12_GESTION, OC12_SUPPORT)",
        "role": "role (MANAGER, EMPLOYEE)"
    }
    collaborator_attributes_dict = {}
    print("[bold blue][COLLABORATOR CREATION][/bold blue]")
    try:
        for key, value in collaborator_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            collaborator_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][COLLABORATOR CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return collaborator_attributes_dict


def submit_a_collaborator_role_create_form():
    """
    Description: Fonction dédiée à créer un nouveau rôle pour un collaborateur de l'entreprise.
    """
    collaborator_role_expected_attributes_dict = {
        "name": "name (MANAGER, EMPLOYEE)"
    }
    collaborator_role_attributes_dict = {}
    print("[bold blue][COLLABORATOR ROLE CREATION][/bold blue]")
    try:
        for key, value in collaborator_role_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            collaborator_role_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][COLLABORATOR ROLE CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return collaborator_role_attributes_dict


def submit_a_collaborator_department_create_form():
    """
    Description: Fonction dédiée à créer un nouveau service /département de l'entreprise.
    """
    collaborator_department_expected_attributes_dict = {
        "department": "service (examples: OC12_COMMERCIAL, OC12_GESTION, ...)"
    }
    collaborator_department_attributes_dict = {}
    print("[bold blue][COLLABORATOR DEPARTMENT CREATION][/bold blue]")
    try:
        for key, value in collaborator_department_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            collaborator_department_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][COLLABORATOR DEPARTMENT CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return collaborator_department_attributes_dict


def submit_a_contract_create_form():
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 2 clefs étrangères 'client_id' et 'collaborator_id' sont attendues.
    """
    contract_expected_attributes_dict = {
        "full_amount_to_pay": "total à payer",
        "remain_amount_to_pay": "total restant à payer",
        "status": "statut ('True' ou 'False')",
    }
    contract_attributes_dict = {}
    print("[bold blue][CONTRACT CREATION][/bold blue]")
    try:
        for key, value in contract_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            contract_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][CONTRACT CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return contract_attributes_dict


def submit_an_event_create_form():
    """
    Description: Fonction dédiée à créer un contrat entre un commercial de l'entreprise et un client.
    Noter que 4 clefs étrangères 'contract_id', 'client_id', 'collaborator_id', et 'location_id' sont attendues.
    """
    event_expected_attributes_dict = {
        "title": "titre",
        "attendees": "public max attendu",
        "notes": "description",
    }
    event_attributes_dict = {}
    print("[bold blue][EVENT CREATION][/bold blue]")
    try:
        for key, value in event_expected_attributes_dict.items():
            item = Prompt.ask(f"{value}: ")
            event_attributes_dict[key] = item
    except KeyboardInterrupt:
        print("[bold green][EVENT CREATION][/bold green] Creation aborted")
        sys.exit(0)
    return event_attributes_dict