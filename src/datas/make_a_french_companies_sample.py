import csv
import requests
from time import sleep


csv_headers = [
    "siren",
    "nom_raison_sociale",
    "activite_principale",
    "adresse",
    "cedex",
    "code_postal",
    "complement_adresse",
    "date_debut_activite",
    "siret",
    "pays",
]

export_file_path = "src/datas/csv/french_companies.csv"


def generate_companies_file():
    with open(f"{export_file_path}", "w", newline="") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(csv_headers)

    for page_number in range(30):
        url = f"https://recherche-entreprises.api.gouv.fr/search?departement=94,44,13&page={page_number+1}&per_page=20"
        headers = {"Content-Type": "application/json; charset=utf-8"}
        response = requests.get(url, headers=headers)
        with open(f"{export_file_path}", "a+", newline="") as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=",", quoting=csv.QUOTE_MINIMAL)
            for company in response.json()["results"]:
                company["pays"] = "France"
                company_list = [
                    company["siren"],
                    company["nom_raison_sociale"],
                    company["siege"]["activite_principale"],
                    company["siege"]["adresse"],
                    company["siege"]["cedex"],
                    company["siege"]["code_postal"],
                    company["siege"]["complement_adresse"],
                    company["siege"]["date_debut_activite"],
                    company["siege"]["siret"],
                    company["pays"],
                ]
                spamwriter.writerow(company_list)
        sleep(1)


generate_companies_file()
