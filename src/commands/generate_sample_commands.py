"""
Description: Toutes les commandes pour générer des échantillons de données à importer.
"""
import click
from rich import print

try:
    from src.datas import make_a_french_companies_sample
except ModuleNotFoundError:
    from datas import make_a_french_companies_sample


@click.command
def generate_companies_sample():
    """
    Description: commande dédiée à générer un fichier entreprise lambda.
    """
    try:
        make_a_french_companies_sample.generate_companies_file()
    except Exception:
        print("[bold red]Problème lors de la création de l'échantillon[/bold red]")
