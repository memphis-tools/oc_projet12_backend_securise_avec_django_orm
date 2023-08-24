"""
Description:
Un controleur avec toutes méthodes pour supprimer des données.
"""

import sqlalchemy
from sqlalchemy import text

try:
    from src.exceptions import exceptions
    from src.models import models
except ModuleNotFoundError:
    from exceptions import exceptions
    from models import models


class DatabaseDeleteController:
    """
    Description: Toutes les méthodes pour supprimer des données.
    """

    def delete_client(self, session, client_id):
        """
        Description: Fonction dédiée à servir la vue lors de la suppression d'un client.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            client = session.query(models.Client).filter_by(id=client_id).first()
            session.delete(client)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_collaborator(self, session, collaborator_id):
        """
        Description: Fonction dédiée à servir la vue lors de la suppression d'un collaborateur.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            collaborator = (
                session.query(models.Collaborator).filter_by(id=collaborator_id).first()
            )
            removed_id = collaborator.registration_number
            role = collaborator.registration_number
            session.delete(collaborator)
            sql = text(f"""DROP ROLE {role}""")
            session.execute(sql)
            session.commit()
            session.close()
            return removed_id
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_company(self, session, company_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une suppression d'une entreprise.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            company = session.query(models.Company).filter_by(id=company_id).first()
            session.delete(company)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_contract(self, session, contract_id):
        """
        Description: Fonction dédiée à servir la vue lors de la suppression d'un contrat.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            contract = session.query(models.Contract).filter_by(id=contract_id).first()
            session.delete(contract)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_department(self, session, department_id):
        """
        Description:
        Fonction dédiée à servir la vue lors de la suppression d'un department /service de l'entreprise.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            department = (
                session.query(models.Collaborator_Department)
                .filter_by(id=int(department_id))
                .first()
            )
            session.delete(department)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_event(self, session, event_id):
        """
        Description: Fonction dédiée à servir la vue lors de la suppression d'un évènement.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            event = session.query(models.Event).filter_by(id=event_id).first()
            session.delete(event)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_location(self, session, location_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une suppression d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            location = session.query(models.Location).filter_by(id=location_id).first()
            session.delete(location)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)

    def delete_role(self, session, role_id):
        """
        Description: Fonction dédiée à servir la vue lors de la suppression d'un rôle pour collaborateur.
        Requête de la base de données et renvoie True si réussie.
        """
        try:
            role = session.query(models.Collaborator_Role).filter_by(id=role_id).first()
            session.delete(role)
            session.commit()
            session.close()
            return True
        except sqlalchemy.exc.IntegrityError as error:
            if "psycopg.errors.ForeignKeyViolation" in str(error):
                raise exceptions.ForeignKeyDependyException(error.orig)
