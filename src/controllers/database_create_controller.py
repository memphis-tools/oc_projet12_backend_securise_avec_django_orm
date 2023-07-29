"""
Un controleur avec toutes méthodes pour ajouter des données.
"""
from sqlalchemy.sql import text
try:
    from src.models import models
    from src.controllers.database_initializer_controller import DatabaseInitializerController
except ModuleNotFoundError:
    from models import models
    from controllers.database_initializer_controller import DatabaseInitializerController


class DatabaseCreateController:
    """
    Description: Toutes les méthodes pour ajouter des données.
    """

    def add_client(self, session, client):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un client.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(client)
            session.commit()
            return client.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_company(self, session, company):
        """
        Description: Fonction dédiée à servir la vue lors d'un ajout d'une entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(company)
            session.commit()
            return company.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_location(self, session, location):
        """
        Description: Fonction dédiée à servir la vue lors d'un ajout d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(location)
            session.commit()
            return location.id
        except Exception as error:
            print(f"Error while adding: {error}")
