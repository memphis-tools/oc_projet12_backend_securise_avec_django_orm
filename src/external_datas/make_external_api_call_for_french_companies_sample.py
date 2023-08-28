"""
Description:
Sert à effectuer une requête à une API ouverte du gouvernement Français.
Le fichier settings précise combien d'entreprises, et de 'pages' par entreprise l'API retourne.
"""
import csv
import requests
from time import sleep
from rich.progress import Progress
try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


EXPORT_FILE_PATH = settings.COMPANIES_EXPORT_FILE_PATH


def generate_companies_file():
    with open(f"{EXPORT_FILE_PATH}", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(settings.COMPANIES_CSV_HEADERS)

    api_max_page = settings.FR_COMPANIES_API_MAX_PAGE_TO_PARSE
    api_url = settings.FR_COMPANIES_API_URL
    api_max_per_page = settings.FR_COMPANIES_API_MAX_COMPANIES_PER_PAGE
    api_departements_string_list = settings.FR_COMPANIES_DEPARTEMENTS_STRING_LIST

    with Progress() as progress:
        nb_companies = api_max_page * api_max_per_page
        task = progress.add_task("[white]External_API Request Companies data", total=nb_companies)
        while not progress.finished:
            for page_number in range(api_max_page):
                progress.update(task, advance=1)
                url = f"{api_url}?departement={api_departements_string_list}&page={page_number+1}&per_page={api_max_per_page}"
                headers = {"Content-Type": "application/json; charset=utf-8"}
                response = requests.get(url, headers=headers)
                with open(f"{EXPORT_FILE_PATH}", "a+", newline="") as csvfile:
                    spamwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
                    for company in response.json()["results"]:
                        company["pays"] = "France"
                        adresse = ""
                        try:
                            adresse = (
                                company["siege"]["numero_voie"] + " " + company["siege"]["libelle_voie"]
                            )
                        except Exception:
                            adresse = company["siege"]["libelle_voie"]
                        # noter la correspondance avec les headers du csv, indiqués en 'settings.COMPANIES_CSV_HEADERS'
                        company_list = [
                            company["siren"],
                            company["siege"]["siret"],
                            company["nom_raison_sociale"],
                            company["siege"]["activite_principale"],
                            company["siege"]["date_debut_activite"],
                            adresse,
                            company["siege"]["complement_adresse"],
                            company["siege"]["cedex"],
                            company["siege"]["code_postal"],
                            company["siege"]["libelle_commune"],
                            company["siege"]["region"],
                            company["pays"],
                            company["tranche_effectif_salarie"],
                        ]
                        spamwriter.writerow(company_list)
                sleep(1)
    return True
