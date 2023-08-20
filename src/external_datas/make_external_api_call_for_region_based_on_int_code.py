import requests

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


def get_region_name_from_insee_open_api(region_id_code):
    """
    Description:
    Vérifier si le paramètre settings.INTERNET_CONNECTION est True.
    Si vrai alors interroger l'open API du gouvernement Français.
    """
    digit_region_id_code = int(region_id_code)
    url = settings.FR_COMPANIES_REGION_API_URL
    query_string = f"q={digit_region_id_code}"
    region_name = ""
    if settings.INTERNET_CONNECTION:
        headers = {'user-agent': 'curl'}
        response = requests.get(url, query_string, headers=headers)
        try:
            region_name = response.json()[0]['nom']
        except IndexError:
            pass
        finally:
            return region_name
    else:
        return None
