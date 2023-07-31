"""
Fichier de variables diverses dédiées à l'authentification et à adresser le SGBD.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# on charge le PATH
dotenv_path = Path(".envrc")
load_dotenv(dotenv_path=dotenv_path)
SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")

# variables diverses
APP_FIGLET_TITLE = "EPIC EVENTS"

# variables dédiées aux autorisations
OC12_COMMERCIAL_CRUD_TABLES = ["client", "company", "contract", "event", "location"]
OC12_COMMERCIAL_PWD = os.environ.get("OC12_COMMERCIAL_PWD")

OC12_GESTION_CRUD_TABLES = [
    "collaborator",
    "collaborator_department",
    "collaborator_role",
    "contract",
    "location",
]
OC12_GESTION_PWD = os.environ.get("OC12_GESTION_PWD")

OC12_SUPPORT_CRUD_TABLES = []
OC12_SUPPORT_PWD = os.environ.get("OC12_SUPPORT_PWD")

# variables dédiées pour définir la base de données à joindre
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "projet12"
DATABASE_PORT = "5432"

# variables dédiées à définir l'envionnement d'exécution
PATH_APPLICATION_ENV_NAME = "OC_12_ENV"
PATH_APPLICATION_JWT_NAME = "OC_12_JWT"
if os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "TEST":
    JWT_UNIT_DURATION = "seconds"
    JWT_DURATION = 1
elif os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "DEV":
    JWT_UNIT_DURATION = "seconds"
    JWT_DURATION = 1200
elif os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "PROD":
    JWT_UNIT_DURATION = "hours"
    JWT_DURATION = 24
HASH_ALGORITHM = "HS256"
