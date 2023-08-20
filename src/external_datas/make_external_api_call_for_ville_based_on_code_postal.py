import requests
import json
try:
    from src.settings import settings
    from src.external_datas.make_external_api_call_for_region_based_on_int_code import get_region_name_from_insee_open_api
except ModuleNotFoundError:
    from settings import settings
    from external_datas.make_external_api_call_for_region_based_on_int_code import get_region_name_from_insee_open_api


def get_town_name_from_insee_open_api(code_postal):
    """
    Description:
    Vérifier si le paramètre settings.INTERNET_CONNECTION est True.
    Si vrai alors interroger l'open API du gouvernement Français.
    """
    digit_code_postal = int(code_postal)
    url = settings.FR_COMPANIES_TOWN_API_URL
    query_string = f"codePostal={digit_code_postal}&fields=nom,code,codesPostaux,siren,codeEpci,codeDepartement,codeRegion,population&format=json&geometry=centre"
    town_name = ""
    region_name = ""
    population = ""
    if settings.INTERNET_CONNECTION:
        headers = {'user-agent': 'curl'}

        try:
            response = requests.get(url+query_string, headers=headers)
            json_response = json.loads(response.text)
            town_name = json_response[0]['nom']
            region_id = json_response[0]['codeRegion']
            region_name = get_region_name_from_insee_open_api(region_id)
            population = json_response[0]['population']
        except IndexError:
            pass
        finally:
            return (town_name, region_name, population)
    else:
        return None
