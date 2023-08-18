"""
Description: Toutes les commandes pour générer des échantillons de données à importer.
"""
import click
from rich import print

try:
    from src.datas import make_a_french_companies_sample
    from src.printers import printer
    from src.languages import language_bridge
except ModuleNotFoundError:
    from datas import make_a_french_companies_sample
    from printers import printer
    from languages import language_bridge


APP_DICT = language_bridge.LanguageBridge()


@click.command
def generate_companies_sample():
    """
    Description: commande dédiée à générer un fichier entreprise lambda.
    """
    try:
        make_a_french_companies_sample.generate_companies_file()
    except Exception:
        printer.print_message("success", APP_DICT.get_appli_dictionnary()['API_INSEE_ACCESS_FAILED'])
