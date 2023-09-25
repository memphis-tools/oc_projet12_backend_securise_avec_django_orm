"""
Pour chaque données renseignées par l'utilisateur on instaure des possibles controles.
On retient les critères Français.
"""

import re

try:
    from src.controllers import infos_data_controller
    from src.exceptions import exceptions
except ModuleNotFoundError:
    from controllers import infos_data_controller
    from exceptions import exceptions


def is_adresse_valid(adresse):
    """
    Description: Controler l'adresse saisis.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"[\w \- ' , \.]{,150}$")
    return re.match(pattern, adresse).group()


def is_region_valid(region):
    """
    Description: Controler la région saisie, à minima, dans le cas d'une saisie manuelle.
    La région est nomarlement ramenée automatiquement par appel API externe.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"[\w \- ' , \.]{,150}$")
    return re.match(pattern, region).group()


def is_population_valid(population):
    """
    Description: Controler la population saisie, à minima, dans le cas d'une saisie manuelle.
    La population est nomarlement ramenée automatiquement par appel API externe.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d+")
    return re.match(pattern, population).group()


def is_cedex_valid(cedex):
    """
    Description: Controler le cedex saisie, à minima, dans le cas d'une saisie manuelle.
    Le cedex est nomarlement ramenée automatiquement par appel API externe.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d+")
    return re.match(pattern, cedex).group()


def is_attendees_valid(attendees):
    """
    Description: Controler le nombre saisi.
    Fonction renvoie une exception AttributeError si chiffre invalide.
    """
    pattern = re.compile(r"\d+")
    return re.match(pattern, attendees).group()


def is_civility_valid(civility):
    """
    Description: Controler la civilité saisie.
    Fonction renvoie une exception AttributeError si libellé invalide.
    """
    civilities = ["MR", "MME", "MLE", "AUTRE"]
    if civility not in civilities:
        raise AttributeError()
    return civility


def is_client_id_valid(client_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- ' \_]{,120})$")
    return re.match(pattern, client_id).group()


def is_code_postal_valid(code_postal):
    """
    Description: Controler le code postal saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{5}$")
    return re.match(pattern, code_postal).group()


def is_company_id_valid(company_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ \.]{,120})$")
    return re.match(pattern, company_id).group()


def is_company_name_valid(company_name):
    """
    Description: Controler le nom d'entreprise saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ ']{,130})$")
    return re.match(pattern, company_name).group()


def is_activite_principale_valid(code_activite):
    """
    Description: Controler le code activité de l'entreprise saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ \. ']{,15})$")
    return re.match(pattern, code_activite).group()


def is_company_registration_number_valid(company_registration_number):
    """
    Description: Controler le SIREN saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{9}$")
    return re.match(pattern, company_registration_number).group()


def is_company_subregistration_number_valid(company_subregistration_number):
    """
    Description: Controler le NIC saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{5}$")
    return re.match(pattern, company_subregistration_number).group()


def is_complement_word_foreseen(complement_words):
    """
    Description: Controler la présence d'au moins un mot clef dans le complément d'adresse.
    """
    valid_complement_list = infos_data_controller.get_infos_data("types_voies")
    for word in complement_words:
        if word in valid_complement_list:
            return True
    return False


def is_complement_adresse_valid(complement_adresse):
    """
    Description: Controler le complément adresse saisis.
    Fonction renvoie False si pattern ne correspond pas.
    """
    if complement_adresse == '""' or complement_adresse == "''":
        return complement_adresse
    pattern = re.compile(r"([\w' \- \_ \.]{,75})$")
    complement_words = complement_adresse.split(" ")
    if not is_complement_word_foreseen(complement_words):
        return False
    return re.match(pattern, complement_adresse).group()


def is_contract_id_valid(contract_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \_ \- \.']{,120})$")
    return re.match(pattern, contract_id).group()


def is_creation_date_valid(creation_date):
    """
    Description: Controler la date saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{4}-\d{,2}-\d{,2}$")
    return re.match(pattern, creation_date).group()


def is_commercial_contact_valid(commercial_contact_id):
    """
    Description: Controler le commercial qu'on souhaite modifier pour un client.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ \.']{,120})$")
    return re.match(pattern, commercial_contact_id).group()


def is_department_id_valid(department_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ \.']{,120})$")
    return re.match(pattern, department_id).group()


def is_department_valid(department):
    """
    Description: Controler le department saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \- \_ \.']{,120})$")
    return re.match(pattern, department).group()


def is_email_valid(email):
    """
    Description: Controler l'email saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"(\w){2,}[(\.){*](\w){2,}@([\w \-]){2,}[(\.){+](\w){2,}")
    return re.match(pattern, email).group()


def is_employee_role_valid(employee_role):
    """
    Description: Controler la nature d'emploi saisie.
    Fonction renvoie une exception AttributeError si libellé invalide.
    """
    valid_roles_list = infos_data_controller.get_infos_data("metiers")
    if employee_role not in valid_roles_list:
        raise AttributeError()


def is_event_end_date_valid(event_end_date):
    """
    Description: Controler la date+heure saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{4}-\d{,2}-\d{,2} \d{,2}:\d{,2}:\d{,2}$")
    return re.match(pattern, event_end_date).group()


def is_event_id_valid(event_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \_ \- \.]{,120})$")
    return re.match(pattern, event_id).group()


def is_event_start_date_valid(event_start_date):
    """
    Description: Controler la date+heure saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{4}-\d{,2}-\d{,2} \d{,2}:\d{,2}:\d{,2}$")
    return re.match(pattern, event_start_date).group()


def is_first_name_valid(first_name):
    """
    Description: Controler le prénom saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w \.']{,150})$")
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
    pattern = re.compile(r"([\w ']{,75})$")
    return re.match(pattern, first_name).group()


def is_location_id_valid(location_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w -']{,120})$")
    return re.match(pattern, location_id).group()


def is_notes_valid(notes):
    """
    Description: Controler les notes saisis (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ' \. \"]{,2500})$")
    return re.match(pattern, notes).group()


def is_pays_valid(pays):
    """
    Description: Controler le pays saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ']{,100})$")
    return re.match(pattern, pays).group()


def is_registration_number_valid(registration_number):
    """
    Description: Controler le matricule saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ]{,12})$")
    return re.match(pattern, registration_number).group()


def is_collaborator_id_valid(id):
    """
    Description: Controler l'id du collaborateur. C'est utilisé notamment en cas de mise à jour d'un évènement.
    Pour éviter d'introduire des exceptions ailleurs dans le code, ce validateur est crée.
    Cependant il ne fait que vérifier que l'id (réel, la primary key) du collaborateur, est un entier.
    Et c'est ce qu'elle est pas défintion dans le modèle.
    """
    pattern = re.compile(r"\d")
    return re.match(pattern, id).group()


def is_remain_amount_to_pay_valid(remain_amount_to_pay, full_amount_to_pay):
    """
    Description: Controler le montant saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    try:
        float(remain_amount_to_pay)
        if float(remain_amount_to_pay) > float(full_amount_to_pay):
            raise exceptions.ContractAmountToPayException()
    except ValueError:
        raise AttributeError()
    return remain_amount_to_pay


def is_role_id_valid(role_id):
    """
    Description: Controler le custom id saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ' ]{,120})$")
    return re.match(pattern, role_id).group()


def is_role_valid(role):
    """
    Description: Controler le role saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ' - ]{,120})$")
    return re.match(pattern, role).group()


def is_name_valid(role):
    """
    Description: Controler le nom saisi (nom du role)
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ' ]{,120})$")
    return re.match(pattern, role).group()


def is_status_valid(status):
    """
    Description: Controler le statut saisi.
    Fonction renvoie une exception AttributeError si montant invalide.
    """
    if status not in ["signed", "unsigned", "canceled"]:
        raise AttributeError()


def is_telephone_valid(telephone):
    """
    Description: Controler le téléphone saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"\d{8,12}$")
    return re.match(pattern, telephone).group()


def is_title_valid(title):
    """
    Description: Controler le titre saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ' ]{,125})$")
    return re.match(pattern, title).group()


def is_username_valid(username):
    """
    Description: Controler le username saisi (nombre caractères max repris du modèle).
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"([\w ]{,65})$")
    return re.match(pattern, username).group()


def is_ville_valid(ville):
    """
    Description: Controler la ville saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r"[\w' -]{,100}$")
    return re.match(pattern, ville).group()
