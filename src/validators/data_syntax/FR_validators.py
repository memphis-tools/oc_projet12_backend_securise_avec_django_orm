"""
Pour chaque données renseignées par l'utilisateur on instaure des possibles controles.
On retient les critères Français.
"""

import re


def is_code_postal_valid(code_postal):
    """
    Description: Controler le code postal saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{5}')
    return re.match(pattern, code_postal).group()


def is_email_valid(email):
    """
    Description: Controler l'email saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'(\w{1,})(\.*)(\w{1,})@(\w{1,})\.(\w{2,4}$)')
    return re.match(pattern, email).group()


def is_telephone_valid(telephone):
    """
    Description: Controler le téléphone saisi.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    pattern = re.compile(r'\d{8,12}')
    return re.match(pattern, telephone).group()


def is_civility_valid(civility):
    """
    Description: Controler la civilité saisie.
    Fonction renvoie une exception AttributeError si pattern ne correspond pas.
    """
    civilities = ["MR", "MME", "MLE", "AUTRE"]
    if civility not in civilities:
        raise AttributeError()
