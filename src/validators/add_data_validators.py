"""
La console en mode création permet les ajouts de données aux modèles de 2 manières:
- soit de présenter un formulaire à l'utilisateur
- soit de donner en paramètre un dictionnaire avec les paramètres attendus pour l'instanciation d'un modèle
C'est pour le 2ème cas qu'on introduit ce module.
"""


def data_is_dict(data) -> bool:
    if isinstance(data, dict):
        return True
    return False


def add_client_data_is_valid(data) -> bool:
    expected_keys = [
        "client_id",
        "civility",
        "first_name",
        "last_name",
        "employee_role",
        "email",
        "telephone",
        "company_id",
        "commercial_contact",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_collaborator_data_is_valid(data) -> bool:
    expected_keys = ["registration_number", "username", "department", "role"]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_company_data_is_valid(data) -> bool:
    expected_keys = [
        "company_id",
        "company_name",
        "company_registration_number",
        "company_subregistration_number",
        "location_id",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_contract_data_is_valid(data) -> bool:
    expected_keys = [
        "contract_id",
        "full_amount_to_pay",
        "remain_amount_to_pay",
        "status",
        "client_id",
        "collaborator_id",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_department_data_is_valid(data) -> bool:
    expected_keys = [
        "department_id",
        "name",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_event_data_is_valid(data) -> bool:
    expected_keys = [
        "event_id",
        "title",
        "attendees",
        "notes",
        "event_start_date",
        "event_end_date",
        "contract_id",
        "client_id",
        "collaborator_id",
        "location_id",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_location_data_is_valid(data) -> bool:
    expected_keys = [
        "location_id",
        "adresse",
        "complement_adresse",
        "code_postal",
        "ville",
        "pays",
    ]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b


def add_role_data_is_valid(data) -> bool:
    expected_keys = ["role_id", "name"]
    b = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and b
