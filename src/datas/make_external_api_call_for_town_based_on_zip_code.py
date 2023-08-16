import requests

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


def get_town_name_from_insee_open_api(code_postal):
    """
    Description:
    Vérifier si le paramètre settings.INTERNET_CONNECTION est True.
    Si vrai alors interroger l'open API du gouvernement Français.
    """
    digit_code_postal = int(code_postal)
    url = "https://api-adresse.data.gouv.fr/search/?"
    query_string = f"q={digit_code_postal}&limit=2"
    town_name = ""
    if settings.INTERNET_CONNECTION:
        headers = {'user-agent': 'curl'}
        response = requests.get(url, query_string, headers=headers)
        try:
            town_name = response.json()['features'][0]['properties']['name']
        except IndexError:
            pass
        finally:
            return town_name
    else:
        return None
