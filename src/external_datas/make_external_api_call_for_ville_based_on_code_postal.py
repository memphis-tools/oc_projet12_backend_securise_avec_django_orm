import requests
import json

try:
    from src.settings import settings
    from src.external_datas.make_external_api_call_for_region_based_on_int_code import (
        get_region_name_from_insee_open_api,
    )
except ModuleNotFoundError:
    from settings import settings
    from external_datas.make_external_api_call_for_region_based_on_int_code import (
        get_region_name_from_insee_open_api,
    )


URL = settings.FR_COMPANIES_TOWN_API_URL
HEADERS = {"user-agent": "curl"}


def get_population_from_insee_open_api(code_postal):
    """
    Description:
    Vérifier si le paramètre settings.INTERNET_CONNECTION est True.
    Si vrai alors interroger l'open API du gouvernement Français.
    On récupère içi la seule population. Cette fonction est appelée seulement lors
    de l'initialisation de l'application, pour l'import en masse.
    """
    digit_code_postal = int(code_postal)

    fields = "population&format=json&geometry=centre"
    query_string = f"codePostal={digit_code_postal}&fields={fields}"
    town_name = ""
    region_name = ""
    population = ""
    if settings.INTERNET_CONNECTION:
        try:
            response = requests.get(URL + query_string, headers=HEADERS)
            json_response = json.loads(response.text)
            population = int(json_response[0]["population"])
        except Exception:
            population = 0
        finally:
            return population
    else:
        return None


def get_town_name_region_name_and_population_from_insee_open_api(code_postal):
    """
    Description:
    Vérifier si le paramètre settings.INTERNET_CONNECTION est True.
    Si vrai alors interroger l'open API du gouvernement Français.
    """
    digit_code_postal = int(code_postal)

    fields = "nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=json&geometry=centre"
    query_string = f"codePostal={digit_code_postal}&fields={fields}"
    town_name = ""
    region_name = ""
    population = ""
    if settings.INTERNET_CONNECTION:
        try:
            response = requests.get(URL + query_string, headers=HEADERS)
            json_response = json.loads(response.text)
            town_name = json_response[0]["nom"]
            region_id = json_response[0]["codeRegion"]
            region_name = get_region_name_from_insee_open_api(region_id)
            population = json_response[0]["population"]
        except IndexError:
            pass
        finally:
            return (town_name, region_name, population)
    else:
        return None
