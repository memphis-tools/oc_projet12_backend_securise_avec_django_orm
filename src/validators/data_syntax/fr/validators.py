"""
Pour chaque données renseignées par l'utilisateur on instaure des possibles controles.
On retient les critères Français.
"""

import re
try:
    from src.commands import infos_data_commands
except ModuleNotFoundError:
    from commands import infos_data_commands


def is_adresse_valid(adresse):
    """
    Description: Controler l'adresse saisis.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'[\w ]{,150}$')
    return re.match(pattern, adresse).group()


def is_attendees_valid(attendees):
    """
    Description: Controler le montant saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    pattern = re.compile(r'\d{+}')
    return re.match(pattern, attendees).group()


def is_civility_valid(civility):
    """
    Description: Controler la civilité saisie.
    Fonction renvoie une exception AttributeError si libellé invalide.
    """
    civilities = ["MR", "MME", "MLE", "AUTRE"]
    if civility not in civilities:
        raise AttributeError()


def is_client_id_valid(client_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, client_id).group()


def is_code_postal_valid(code_postal):
    """
    Description: Controler le code postal saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{5}$')
    return re.match(pattern, code_postal).group()


def is_company_id_valid(company_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, company_id).group()


def is_company_name_valid(company_name):
    """
    Description: Controler le nom d'entreprise saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,130})$')
    return re.match(pattern, company_name).group()


def is_company_registration_number_valid(company_registration_number):
    """
    Description: Controler le SIREN saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{9}$')
    return re.match(pattern, company_registration_number).group()


def is_company_subregistration_number_valid(company_registration_number):
    """
    Description: Controler le NIC saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{5}$')
    return re.match(pattern, company_subregistration_number).group()


def is_complement_adresse_valid(complement_adresse):
    """
    Description: Controler le complément adresse saisis.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\w{,75}$')
    return re.match(pattern, complement_adresse).group()


def is_contract_id_valid(contract_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, contract_id).group()


def is_creation_date_valid(creation_date):
    """
    Description: Controler la date saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{4}-\d{,2}-\d{,2}$')
    return re.match(pattern, creation_date).group()


def is_department_id_valid(department_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, department_id).group()


def is_email_valid(email):
    """
    Description: Controler l'email saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'(\w{1,})(\.*)(\w{1,})@(\w{1,})\.(\w{2,4}$)')
    return re.match(pattern, email).group()


def is_employee_role_valid(employee_role):
    """
    Description: Controler la nature d'emploi saisie.
    Fonction renvoie une exception AttributeError si libellé invalide.
    """
    valid_roles_list = infos_data.get_metiers_roles_file()
    if employee_role not in valid_roles_list:
        raise AttributeError()


def is_event_end_date_valid(event_end_date):
    """
    Description: Controler la date+heure saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{4}-\d{,2}-\d{,2} \d{,2}:\d{,2}:\d{,2}$')
    return re.match(pattern, event_end_date).group()


def is_event_id_valid(event_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, event_id).group()


def is_event_start_date_valid(event_start_date):
    """
    Description: Controler la date+heure saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{4}-\d{,2}-\d{,2} \d{,2}:\d{,2}:\d{,2}$')
    return re.match(pattern, event_start_date).group()


def is_first_name_valid(first_name):
    """
    Description: Controler le prénom saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,150})$')
    return re.match(pattern, first_name).group()


def is_full_amount_to_pay_valid(full_amount_to_pay):
    """
    Description: Controler le montant saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    try:
        float(full_amount_to_pay)
    except ValueError:
        raise AttributeError()


def is_last_name_valid(first_name):
    """
    Description: Controler le nom saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,75})$')
    return re.match(pattern, first_name).group()


def is_location_id_valid(location_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, location_id).group()


def is_notes_valid(notes):
    """
    Description: Controler les notes saisis (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,2500})$')
    return re.match(pattern, notes).group()


def is_pays_valid(pays):
    """
    Description: Controler le pays saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,100})$')
    return re.match(pattern, pays).group()


def is_registration_number_valid(registration_number):
    """
    Description: Controler le matricule saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,12})$')
    return re.match(pattern, registration_number).group()


def is_remain_amount_to_pay_valid(remain_amount_to_pay):
    """
    Description: Controler le montant saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    try:
        float(remain_amount_to_pay)
    except ValueError:
        raise AttributeError()


def is_role_id_valid(role_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,120})$')
    return re.match(pattern, role_id).group()


def is_status_valid(status):
    """
    Description: Controler le statut saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    if status not in ["oui", "non"]:
        raise AttributeError()


def is_telephone_valid(telephone):
    """
    Description: Controler le téléphone saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{8,12}$')
    return re.match(pattern, telephone).group()


def is_title_valid(title):
    """
    Description: Controler le titre saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\w {,125}$')
    return re.match(pattern, title).group()


def is_username_valid(username):
    """
    Description: Controler le username saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'([\w ]{,65})$')
    return re.match(pattern, username).group()


def is_ville_valid(ville):
    """
    Description: Controler la ville saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\w{,100}$')
    return re.match(pattern, ville).group()
