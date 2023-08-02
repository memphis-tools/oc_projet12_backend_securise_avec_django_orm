"""
Un controleur avec toutes méthodes GET.
"""

try:
    from src.models import models
except ModuleNotFoundError:
    from models import models


class DatabaseReadController:
    """
    Description: Toutes les méthodes GET.
    """

    def get_client(self, session, client_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un client.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        Paramètres:
        - client_id: c'est le custom id (chaine libre)
        """
        try:
            db_client_queryset = (
                session.query(models.Client).filter_by(client_id=client_id).first()
            )
            session.close()
            return db_client_queryset
        except Exception as error:
            print(f"Client not found: {error}")

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
        Description:
        Fonction dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(models.User)
                .filter_by(registration_number=registration_number)
                .first()
            )
            session.close()
            return db_collaborator_queryset
        except Exception as error:
            print(f"User or Department not found: {error}")

    def get_collaborator_join_department(self, session, registration_number):
        """
        Description:
        Fonction dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise pour la création du token.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(models.User, models.UserDepartment)
                .filter(models.User.department == models.UserDepartment.id)
                .filter_by(registration_number=registration_number)
                .first()
            )
            session.close()
            return db_collaborator_queryset
        except Exception as error:
            print(f"User or Department not found: {error}")

    def get_collaborators(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des utilisateurs de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        """
        db_collaborators = session.query(models.User).all()
        session.close()
        return db_collaborators

    def get_company(self, session, company_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'une entreprise cliente.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        try:
            db_company_queryset = (
                session.query(models.Company)
                # session.query(models.Company, models.Location)
                # .filter(models.Company.location_id == models.Location.id)
                .filter_by(company_id=company_id).first()
            )
            session.close()
            return db_company_queryset
        except Exception as error:
            print(f"Company not found: {error}")

    def get_companies(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des entreprises clientes de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        db_companies = session.query(models.Company).all()
        session.close()
        return db_companies

    def get_contract(self, session, contract_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un contrat de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        Paramètres:
        - contract_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_contract = (
                session.query(models.Contract)
                .filter_by(contract_id=contract_id)
                .first()
            )
            session.close()
            return db_collaborators_contract
        except Exception as error:
            print(f"Department not found: {error}")

    def get_contracts(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des contrats de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        """
        db_collaborators_contracts = session.query(models.Contract).all()
        session.close()
        return db_collaborators_contracts

    def get_department(self, session, department_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un département /service de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserDepartment.
        Paramètres:
        - department_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_department = (
                session.query(models.UserDepartment)
                .filter_by(department_id=department_id)
                .first()
            )
            session.close()
            return db_collaborators_department
        except Exception as error:
            print(f"Department not found: {error}")

    def get_departments(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des départements /services de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserDepartment.
        """
        db_collaborators_department = session.query(models.UserDepartment).all()
        session.close()
        return db_collaborators_department

    def get_event(self, session, event_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un évènement de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        Paramètres:
        - event_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_event = (
                session.query(models.Event).filter_by(event_id=event_id).first()
            )
            session.close()
            return db_collaborators_event
        except Exception as error:
            print(f"Event not found: {error}")

    def get_events(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des évènements de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        """
        db_collaborators_events = session.query(models.Event).all()
        session.close()
        return db_collaborators_events

    def get_location(self, session, location_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        Paramètres:
        - location_id: chaine de caractères (ce n'est pas l'id integer pour la clef primaire).
        """
        try:
            db_locations_queryset = (
                session.query(models.Location)
                .filter_by(location_id=location_id)
                .first()
            )
            session.close()
            return db_locations_queryset
        except Exception as error:
            print(f"Location not found: {error}")

    def get_locations(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des localisations des évènements.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        """
        db_collaborators_locations = session.query(models.Location).all()
        session.close()
        return db_collaborators_locations

    def get_role(self, session, role_id):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête d'un rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserRole.
        Paramètres:
        - role_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_role = (
                session.query(models.UserRole).filter_by(role_id=role_id).first()
            )
            session.close()
            return db_collaborators_role
        except Exception as error:
            print(f"Role not found: {error}")

    def get_roles(self, session):
        """
        Description: Fonction dédiée à servir la vue lors d'une requête des rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserRole.
        """
        db_collaborators_role = session.query(models.UserRole).all()
        session.close()
        return db_collaborators_role
