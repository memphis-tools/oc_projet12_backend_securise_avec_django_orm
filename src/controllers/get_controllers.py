"""
Un controleur avec toutes méthodes GET.
"""
try:
    from src.models import models
except ModuleNotFoundError:
    from models import models


class DatabaseGETController:
    """
    Description: Toutes les méthodes GET.
    """

    def get_clients(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des clients de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        """
        db_collaborators_clients = session.query(models.Client).all()
        session.close()
        return db_collaborators_clients

    def get_collaborator(self, session, registration_number):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        """
        db_collaborator = (
            session.query(models.User)
            .filter_by(registration_number=registration_number)
            .first()
        )
        session.close()
        return db_collaborator

    def get_collaborators(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des utilisateurs de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        """
        db_collaborators = session.query(models.User).all()
        session.close()
        return db_collaborators

    def get_contracts(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des contrats de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        """
        db_collaborators_contracts = session.query(models.Contract).all()
        session.close()
        return db_collaborators_contracts

    def get_departments(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des départements /services de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserDepartment.
        """
        db_collaborators_department = session.query(models.UserDepartment).all()
        session.close()
        return db_collaborators_department

    def get_events(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des évènements de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        """
        db_collaborators_events = session.query(models.Event).all()
        session.close()
        return db_collaborators_events

    def get_locations(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des localisations des évènements.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        """
        db_collaborators_locations = session.query(models.Location).all()
        session.close()
        return db_collaborators_locations

    def get_roles(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserRole.
        """
        db_collaborators_role = session.query(models.UserRole).all()
        session.close()
        return db_collaborators_role
