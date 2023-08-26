"""
Description:
Tests des formulaires
"""

try:
    from src.forms import forms
    from src.settings import settings
except ModuleNotFoundError:
    from forms import forms
    from settings import settings


def test_display_help():
    db_name = f"{settings.TEST_DATABASE_NAME}"
    result = forms.display_help("first_name", "?", "donald")
    assert isinstance(result, str)
    assert "?" == result


def test_search_and_submit_a_town_name():
    if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
        result = forms.search_and_submit_a_town_name("75001")
        assert isinstance(result, tuple)
        assert "Paris" in result
    else:
        assert 1 == 1


def test_display_any_error_message():
    result = forms.display_any_error_message("complement_adresse")
    assert isinstance(result, bool)
    assert result is False


def test_submit_a_location_get_form():
    result = forms.submit_a_location_get_form(custom_id="ZA123")
    assert isinstance(result, str)
    assert result == "ZA123"


def test_submit_a_location_create_form():
    result = forms.submit_a_location_create_form(location_id="ZA123", custom_dict={"location_id":"ZA123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_company_get_form():
    result = forms.submit_a_company_get_form(custom_id="XXZ123")
    assert isinstance(result, str)
    assert result == "XXZ123"


def test_submit_a_company_create_form():
    result = forms.submit_a_company_create_form(company_location_id="XXZ123", custom_dict={"company_id":"XXZ123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_client_get_form():
    result = forms.submit_a_client_get_form(custom_id="XXZ123")
    assert isinstance(result, str)
    assert result == "XXZ123"


def test_submit_a_client_create_form():
    result = forms.submit_a_client_create_form(custom_dict={"client_id":"XXZ123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_collaborator_get_form():
    result = forms.submit_a_collaborator_get_form(custom_id="fr123456789")
    assert isinstance(result, str)
    assert result == "fr123456789"


def test_submit_a_collaborator_create_form():
    result = forms.submit_a_collaborator_create_form(custom_dict={"client_id":"XXZ123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_collaborator_role_get_form():
    result = forms.submit_a_collaborator_role_get_form(custom_id="emp")
    assert isinstance(result, str)
    assert result == "emp"


def test_submit_a_collaborator_role_create_form():
    result = forms.submit_a_collaborator_role_create_form(custom_dict={"role_id":"emp"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_collaborator_department_get_form():
    result = forms.submit_a_collaborator_department_get_form(custom_id="ccial")
    assert isinstance(result, str)
    assert result == "ccial"


def test_submit_a_collaborator_department_create_form():
    result = forms.submit_a_collaborator_department_create_form(custom_dict={"department_id":"ccial"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_contract_get_form():
    result = forms.submit_a_contract_get_form(custom_id="XXZ123")
    assert isinstance(result, str)
    assert result == "XXZ123"


def test_submit_a_contract_create_form():
    result = forms.submit_a_contract_create_form(custom_dict={"contract_id":"XXZ123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_event_get_form():
    result = forms.submit_a_event_get_form(custom_id="XXZ123")
    assert isinstance(result, str)
    assert result == "XXZ123"


def test_submit_a_event_create_form():
    result = forms.submit_a_contract_create_form(custom_dict={"event_id":"XXZ123"})
    assert isinstance(result, dict)
    assert "creation_date" in result.keys()


def test_submit_a_collaborator_new_password_get_form():
    result = forms.submit_a_collaborator_new_password_get_form(old_password="@pplepie94", new_password="@pplepie95")
    assert isinstance(result, tuple)
    assert result == ("@pplepie94", "@pplepie95")
