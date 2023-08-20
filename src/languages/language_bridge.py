"""
Description:
On va permettre de spécifier tout message dans une langue choisie.
On laisse la possibilité à l'administrateur de changer la langue par défaut.
"""
import os
from os import path
from jinja2 import Environment, FileSystemLoader
import json
try:
    from src.printers import printer
    from src.settings import settings
except ModuleNotFoundError:
    from printers import printer
    from settings import settings


FILENAME = f"src/languages/{settings.DEFAULT_COUNTRY_SHORT}/application_dictionnary.json"


class LanguageBridge:
    """
    Description:
    Dédiée à parcourir un fichier texte qui stocke tous les messages à communiquer.
    Le fichier est structuré comme représentant un dictionnaire.
    La fonction 'generate_env_messages' n'est appelée que par le module 'src/commands/init_commands.py'.
    Le fichier généré, par exemple : 'src/languages/fr/application_dictionnary.json'.
    Il n'est crée qu'à l'initialisation de l'appli.
    """
    def __init__(self):
        try:
            if os.path.isfile(FILENAME) and path.getsize(FILENAME) <= 2:
                self.generate_env_messages()
            else:
                with open(FILENAME, mode="r", encoding="utf-8") as fd:
                    self.dictionary = json.loads(fd.read())
        except FileNotFoundError:
            self.generate_env_messages()


    def generate_env_messages(self):
        """
        Description:
        On génère le fichier de message dans le langage attendu par l'administrateur
        """
        try:
            jinja_env = Environment(loader=FileSystemLoader("src/languages/templates/"))
            template = jinja_env.get_template("language.j2")
            content = template.render(settings.get_settings_referenced_in_languages_files()[0])
            with open(FILENAME, mode="w", encoding="utf-8") as fd:
                fd.write(content)
            with open(FILENAME, mode="r", encoding="utf-8") as fd:
                self.dictionary = json.loads(fd.read())
        except Exception:
            printer.print_message("error", 'ENV_MESSAGES_GENERATION_ERROR')

    def get_appli_dictionnary(self):
        return self.dictionary
