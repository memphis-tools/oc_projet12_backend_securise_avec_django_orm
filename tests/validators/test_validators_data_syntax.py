"""
Description:
test des controleurs de syntaxes des attributs, utilisés par les validateurs
"""
import random
import string
import pytest
try:
    from src.validators.data_syntax.fr import validators
    from src.exceptions import exceptions
except ModuleNotFoundError:
    from validators.data_syntax.fr import validators
    from exceptions import exceptions


def generate_random_string(nb_chars, extra_chars=True):
    letters = string.ascii_letters
    if extra_chars:
        letters += "' - , _ ."
    else:
        letters += "- _"
    random_string = "".join([random.choice(letters) for char in range(nb_chars)])
    return random_string


def test_is_adresse_valid():
    random_string = generate_random_string(35)
    result = validators.is_adresse_valid(random_string)
    assert isinstance(result, str)


def test_is_adresse_valid_when_pattern_not_respected():
    random_string = generate_random_string(155)
    with pytest.raises(AttributeError):
        result = validators.is_adresse_valid(random_string)


def test_is_attendees_valid():
    random_string = random.randint(1, 1000)
    result = validators.is_attendees_valid(str(random_string))
    assert isinstance(result, str)


def test_is_attendees_valid_when_pattern_not_respected():
    random_string = generate_random_string(20)
    with pytest.raises(AttributeError):
        result = validators.is_attendees_valid(random_string)


def test_is_civility_valid():
    result = validators.is_civility_valid("MR")
    assert isinstance(result, str)


def test_is_civility_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_civility_valid("Gentleman")


def test_is_client_id_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_client_id_valid(str(random_string))
    assert isinstance(result, str)


def test_is_client_id_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_client_id_valid(random_string)


def test_is_code_postal_valid():
    result = validators.is_code_postal_valid("75001")
    assert isinstance(result, str)


def test_is_code_postal_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_code_postal_valid("x20z29")


def test_is_is_company_id_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_company_id_valid(str(random_string))
    assert isinstance(result, str)


def test_is_company_id_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_company_id_valid(random_string)


def test_is_company_name_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_company_name_valid(str(random_string))
    assert isinstance(result, str)


def test_is_company_name_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_company_name_valid(random_string)


def test_is_company_registration_number_valid():
    result = validators.is_company_registration_number_valid("111222333")
    assert isinstance(result, str)


def test_is_company_registration_number_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_company_registration_number_valid("111222333444")


def test_is_company_subregistration_number_valid():
    result = validators.is_company_subregistration_number_valid("12345")
    assert isinstance(result, str)


def test_is_company_subregistration_number_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_company_subregistration_number_valid("1234567")


def test_is_complement_word_foreseen_valid():
    result = validators.is_complement_word_foreseen("Allée du venant.".split(" "))
    assert result is True


def test_is_complement_word_foreseen_valid_when_pattern_not_respected():
    result = validators.is_complement_word_foreseen("Caminito de la playa".split(" "))
    assert result is False


def test_is_complement_adresse_valid():
    result = validators.is_complement_adresse_valid("Chemin du venant.")
    assert isinstance(result, str)


def test_is_complement_adresse_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    result = validators.is_complement_adresse_valid(random_string)
    assert result is False


def test_is_creation_date_valid():
    result = validators.is_creation_date_valid("2023-12-15")
    assert isinstance(result, str)


def test_is_creation_date_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_creation_date_valid("15-12-2023")


def test_is_contract_id_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_contract_id_valid(str(random_string))
    assert isinstance(result, str)


def test_is_contract_id_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_contract_id_valid(random_string)


def test_is_commercial_contact_valid_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_commercial_contact_valid(str(random_string))
    assert isinstance(result, str)


def test_is_commercial_contact_valid_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_commercial_contact_valid(random_string)


def test_is_department_id_valid_valid_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_department_id_valid(str(random_string))
    assert isinstance(result, str)


def test_is_department_id_valid_valid_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_department_id_valid(random_string)


def test_is_department_valid_valid_valid_valid():
    random_string = generate_random_string(35, extra_chars=False)
    result = validators.is_department_valid(str(random_string))
    assert isinstance(result, str)


def test_is_department_valid_valid_valid_valid_when_pattern_not_respected():
    random_string = generate_random_string(155, extra_chars=False)
    with pytest.raises(AttributeError):
        result = validators.is_department_valid(random_string)


def test_is_email_valid():
    result = validators.is_email_valid("john.doe@fakenews.gouv")
    assert isinstance(result, str)


def test_is_email_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_email_valid("john.doe")


def test_is_event_end_date_valid():
    result = validators.is_event_end_date_valid("2023-12-15 15:00:00")
    assert isinstance(result, str)


def test_is_event_end_date_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_event_end_date_valid("15-12-2023 20:00:00")


def test_is_event_start_date_valid():
    result = validators.is_event_start_date_valid("2023-12-15 15:00:00")
    assert isinstance(result, str)


def test_is_event_start_date_valid_when_pattern_not_respected():
    with pytest.raises(AttributeError):
        result = validators.is_event_start_date_valid("15-12-2023 20:00:00")


def test_is_remain_amount_to_pay_valid():
    result = validators.is_remain_amount_to_pay_valid(55.55, 100.00)
    assert isinstance(result, float)


def test_is_remain_amount_to_pay_valid_when_pattern_not_respected():
    with pytest.raises(exceptions.ContractAmountToPayException):
        result = validators.is_remain_amount_to_pay_valid(555.55, 100.00)
