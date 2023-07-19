"""
Fichier de variables diverses dédiées à l'authentification et à adresser le SGBD.
"""

from os import environ
from pathlib import Path
from dotenv import load_dotenv


dotenv_path = Path(".envrc")
load_dotenv(dotenv_path=dotenv_path)

SECRET_KEY = environ.get("SECRET_KEY")
ADMIN_LOGIN = environ.get("ADMIN_LOGIN")
ADMIN_PASSWORD = environ.get("ADMIN_PASSWORD")
DATABASE_HOST = "127.0.0.1"
DATABASE_NAME = "projet12"
DATABASE_PORT = "5432"
