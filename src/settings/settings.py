"""
Description:
Fichier de variables diverses dédiées à l'authentification et à adresser le SGBD.
Dédiées à l'administrateur de l'application.
"""

import os
import platform
from pathlib import Path
from dotenv import load_dotenv

# détecter le système d'exploitation
if platform.system() == "Linux":
    USER_OPERATING_SYSTEM = "Linux"
elif platform.system() == "Windows":
    USER_OPERATING_SYSTEM = "Windows"

# on charge le PATH
dotenv_path = Path(".envrc")
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# interrupteur dédié à engager ou non une recherche auprès d'API externes.
INTERNET_CONNECTION = True
LOG_COLLECT_ACTIVATED = True
# on propose un log collector: "local", ou au nom de l'appli choisie, exemple "betterstack"
LOG_COLLECTOR = "betterstack"
BETTERSTACK_SOURCE_TOKEN = os.environ.get("BETTERSTACK_SOURCE_TOKEN")

# variables dédiées aux imports
FR_COMPANIES_API_URL = "https://recherche-entreprises.api.gouv.fr/search"
FR_COMPANIES_DEPARTEMENTS_STRING_LIST = "44,13"
# cette API est ouverte mais vient avec des limites, voir la documentation.
# https://recherche-entreprises.api.gouv.fr/docs/
FR_COMPANIES_API_MAX_PAGE_TO_PARSE = 1
FR_COMPANIES_API_MAX_COMPANIES_PER_PAGE = 10
COMPANIES_EXPORT_FILE_PATH = "src/external_datas/csv/french_companies.csv"
COMPANIES_CSV_HEADERS = [
    "siren",
    "siret",
    "nom_raison_sociale",
    "activite_principale",
    "date_debut_activite",
    "adresse",
    "complement_adresse",
    "cedex",
    "code_postal",
    "commune",
    "region",
    "pays",
    "tranche_effectif_salarie",
]

FR_COMPANIES_TOWN_API_URL = "https://geo.api.gouv.fr/communes?"

FR_COMPANIES_REGION_API_URL = "https://geo.api.gouv.fr/regions?"

# variables diverses
APP_FIGLET_TITLE = "EPIC EVENTS"
DEFAULT_COUNTRY = "France"
DEFAULT_COUNTRY_SHORT = "fr"
DEFAULT_CURRENCY = ("euro", "€")
TRANSLATED_MONTHS = [
    ("janvier", "Jan"),
    ("février", "Feb"),
    ("mars", "Mar"),
    ("avril", "Apr"),
    ("mai", "May"),
    ("juin", "Jun"),
    ("juillet", "Jul"),
    ("aout", "Aug"),
    ("septembre", "Sep"),
    ("octobre", "Oct"),
    ("novembre", "Nov"),
    ("décembre", "Dec"),
]

DEFAULT_NEW_COLLABORATOR_PASSWORD = "@pplepie94"
DEFAULT_NEW_PASSWORD_MIN_LENGTH = 8
DEFAULT_NEW_PASSWORD_MAX_LENGTH = 30
DEFAULT_NEW_PASSWORD_MIN_DIGITS = 1
DEFAULT_NEW_PASSWORD_MIN_SPECIAL_CHAR = 1
ALLOWED_SPECIALCHARS_IN_PASSWORD = ["@", "?", "!", "%", "$", "^", "+"]
FORBIDDEN_SPECIALCHARS_IN_PASSWORD = [
    " ",
    ",",
    "`",
    "|",
    "/",
    "\\",
    "{",
    "}",
    "[",
    "]",
    "*",
    ":",
    ";",
]
NEW_PASSWORD_POLICY = [
    "DEFAULT_NEW_COLLABORATOR_PASSWORD",
    "DEFAULT_NEW_PASSWORD_MIN_LENGTH",
    "DEFAULT_NEW_PASSWORD_MAX_LENGTH",
    "DEFAULT_NEW_PASSWORD_MIN_DIGITS",
    "DEFAULT_NEW_PASSWORD_MIN_SPECIAL_CHAR",
    "ALLOWED_SPECIALCHARS_IN_PASSWORD",
    "FORBIDDEN_SPECIALCHARS_IN_PASSWORD",
]

# variables dédiées aux autorisations
OC12_COMMERCIAL_CRUD_TABLES = ["client", "company", "contract", "event", "location"]
OC12_COMMERCIAL_PWD = os.environ.get("OC12_COMMERCIAL_PWD")

OC12_GESTION_CRUD_TABLES = [
    "client",
    "collaborator",
    "collaborator_department",
    "collaborator_role",
    "contract",
    "event",
]
OC12_GESTION_PWD = os.environ.get("OC12_GESTION_PWD")

OC12_SUPPORT_CRUD_TABLES = ["event"]
OC12_SUPPORT_PWD = os.environ.get("OC12_SUPPORT_PWD")

# variables dédiées pour définir la base de données à joindre
DATABASE_TO_CREATE = ["projet12", "dev_projet12", "test_projet12"]
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "projet12"
DEV_DATABASE_NAME = "dev_projet12"
TEST_DATABASE_NAME = "test_projet12"
DATABASE_PORT = "5432"

# variables dédiées à définir l'envionnement d'exécution
PATH_APPLICATION_ENV_NAME = "OC_12_ENV"
PATH_APPLICATION_JWT_NAME = "OC_12_JWT"
JWT_UNIT_DURATION = "hours"
JWT_DURATION = 24
if "PATH_APPLICATION_ENV_NAME" in os.environ:
    if os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "TEST":
        JWT_UNIT_DURATION = "seconds"
        JWT_DURATION = 1
    elif os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "DEV":
        JWT_UNIT_DURATION = "seconds"
        JWT_DURATION = 3600

HASH_ALGORITHM = "HS256"


def get_settings_referenced_in_languages_files():
    settings_for_template_list = [
        {
            "JWT_DURATION": JWT_DURATION,
            "JWT_UNIT_DURATION": JWT_UNIT_DURATION,
            "PATH_APPLICATION_ENV_NAME": PATH_APPLICATION_ENV_NAME,
            "PATH_APPLICATION_JWT_NAME": PATH_APPLICATION_JWT_NAME,
        }
    ]

    return settings_for_template_list
