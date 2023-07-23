"""
Fichier de variables diverses dédiées à l'authentification et à adresser le SGBD.
"""

import os
from pathlib import Path
from dotenv import load_dotenv


dotenv_path = Path(".envrc")
load_dotenv(dotenv_path=dotenv_path)

APP_FIGLET_TITLE = "EPIC EVENTS"

SECRET_KEY = os.environ.get("SECRET_KEY")
ADMIN_LOGIN = os.environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD")
OC12_COMMERCIAL_PWD = os.environ.get("OC12_COMMERCIAL_PWD")
OC12_GESTION_PWD = os.environ.get("OC12_GESTION_PWD")
OC12_SUPPORT_PWD = os.environ.get("OC12_SUPPORT_PWD")
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "projet12"
DATABASE_PORT = "5432"

PATH_APPLICATION_ENV_NAME = "OC_12_ENV"
PATH_APPLICATION_JWT_NAME = "OC_12_JWT"

os.environ[f"{PATH_APPLICATION_ENV_NAME}"] = "DEV"

if os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "TEST":
    JWT_UNIT_DURATION = "seconds"
    JWT_DURATION = 1
elif os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "DEV":
    JWT_UNIT_DURATION = "seconds"
    JWT_DURATION = 600
elif os.environ[f"{PATH_APPLICATION_ENV_NAME}"] == "PROD":
    JWT_UNIT_DURATION = "hours"
    JWT_DURATION = 24

HASH_ALGORITHM = "HS256"
