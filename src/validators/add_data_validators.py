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
        "creation_date",
        "client_id",
        "civility",
        "first_name",
        "last_name",
        "employee_role",
        "email",
        "telephone",
        "company_id",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_collaborator_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
        "registration_number",
        "username",
        "department_id",
        "role_id",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_company_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
        "company_id",
        "company_registration_number",
        "company_subregistration_number",
        "company_name",
        "activite_principale",
        "location_id",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_contract_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
        "contract_id",
        "full_amount_to_pay",
        "remain_amount_to_pay",
        "status",
        "client_id",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_department_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
        "department_id",
        "name",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_event_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
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
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_location_data_is_valid(data) -> bool:
    expected_keys = [
        "creation_date",
        "location_id",
        "adresse",
        "complement_adresse",
        "code_postal",
        "cedex",
        "ville",
        "region",
        "pays",
    ]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid


def add_role_data_is_valid(data) -> bool:
    expected_keys = ["creation_date", "role_id", "name"]
    expected_keys_valid = bool(len(data) == len(expected_keys))
    return list(data.keys()).sort() == expected_keys.sort() and expected_keys_valid
