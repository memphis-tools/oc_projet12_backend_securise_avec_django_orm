"""
Un controleur avec toutes méthodes pour mettre à jour des données.
"""

try:
    from src.exceptions import exceptions
    from src.models import models
    from src.utils import utils
except ModuleNotFoundError:
    from exceptions import exceptions
    from models import models
    from utils import utils


class DatabaseUpdateController:
    """
    Description: Toutes les méthodes pour mettre à jour des données.
    """

    def update_client(
        self, session, current_user_collaborator_id, user_service, client_dict
    ):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un client.
        Requête de la base de données et renvoie True si réussie..
        """
        client_id = client_dict.pop("client_id")
        client = session.query(models.Client).filter_by(client_id=client_id).first()
        if client is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Client.metadata.tables["client"].columns.keys()
        try:
            for key in keys_to_explore:
                if key in client_dict.keys():
                    setattr(client, key, client_dict[key])
        except KeyError:
            session.flush()
            session.rollback()

        if int(current_user_collaborator_id) != int(client.commercial_contact):
            raise exceptions.CommercialCollaboratorIsNotAssignedToClient()
        client.last_update_date = utils.get_today_date()
        session.commit()
        return client.get_dict()

    def update_collaborator(self, session, collaborator_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un collaborateur.
        Requête de la base de données et renvoie True si réussie..
        """
        collaborator_id = collaborator_dict.pop("registration_number")
        collaborator = (
            session.query(models.Collaborator)
            .filter_by(registration_number=collaborator_id)
            .first()
        )
        if collaborator is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Collaborator.metadata.tables[
            "collaborator"
        ].columns.keys()
        department_id = collaborator.department_id
        current_department_name = utils.get_department_name_from_id(
            session, department_id
        )
        try:
            for key in keys_to_explore:
                if key in collaborator_dict.keys():
                    if key == "department":
                        asked_departement = collaborator_dict["department"]
                        new_department_id = utils.get_department_id_from_name(
                            session, asked_departement
                        )
                        new_department_name = utils.get_department_name_from_id(
                            session, new_department_id
                        )
                        setattr(collaborator, key, new_department_id)
                        utils.update_grant_for_collaborator(
                            session,
                            collaborator_id,
                            current_department_name,
                            new_department_name,
                        )
                    else:
                        setattr(collaborator, key, collaborator_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()

        return collaborator.get_dict()

    def update_collaborator_password(
        self, conn, user_registration_number, new_password
    ):
        """
        Description:
        Dédiée à mettre à jour le mot de passe d'un collaborateur.
        Parameters:
        - conn: une connection sur la bdd
        - user_registration_number: chaine de caractères, le matricule de l'employé /collaborateur
        - new_password: chaine de caractères, le nouveau mot de passe pour se connecter à la bdd
        """
        cursor = conn.cursor()
        try:
            sql = f"""ALTER USER {user_registration_number} WITH PASSWORD '{new_password}'"""
            cursor.execute(sql)
        except Exception as error:
            conn.rollback()
        conn.commit()
        conn.close()
        return True

    def update_company(self, session, company_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une entreprise.
        Requête de la base de données et renvoie True si réussie..
        """
        company_id = company_dict.pop("company_id")
        company = session.query(models.Company).filter_by(company_id=company_id).first()
        if company is None:
            raise exceptions.CustomIdMatchNothingException()
        companies = session.query(models.Company).all()
        keys_to_explore = models.Company.metadata.tables["company"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in company_dict.keys():
                    setattr(company, key, company_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()

        return company.get_dict()

    def update_contract(
        self, session, current_user_collaborator_id, user_service, contract_dict
    ):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un contrat.
        Requête de la base de données et renvoie True si réussie..
        """
        contract_id = contract_dict.pop("contract_id")
        contract = (
            session.query(models.Contract).filter_by(contract_id=contract_id).first()
        )
        if contract is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Contract.metadata.tables["contract"].columns.keys()
        try:
            for key in keys_to_explore:
                if key in contract_dict.keys():
                    setattr(contract, key, contract_dict[key])
        except KeyError:
            pass
        # un collaborateur du service gestion peut modifier tout contrat
        # un commercial ne peut modifier que les contrats auxquels il est rattaché
        if user_service.lower() == "oc12_commercial":
            if int(current_user_collaborator_id) != int(contract.client.commercial_contact):
                raise exceptions.CommercialCollaboratorIsNotAssignedToContract()

        session.commit()
        return contract.get_dict()

    def update_department(self, session, department_dict):
        """
        Description:
        Fonction dédiée à servir la vue lors de la mise à jour d'un department /service de l'entreprise.
        Requête de la base de données et renvoie True si réussie..
        """
        department_id = department_dict.pop("department_id")
        department = (
            session.query(models.Collaborator_Department)
            .filter_by(department_id=department_id)
            .first()
        )
        if department is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Collaborator_Department.metadata.tables[
            "collaborator_department"
        ].columns.keys()

        try:
            for key in keys_to_explore:
                if key in department_dict.keys():
                    setattr(department, key, department_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()

        return department.get_dict()

    def update_event(
        self, session, current_user_collaborator_id, user_service, event_dict
    ):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un évènement.
        Requête de la base de données et renvoie True si réussie..
        """
        event_id = event_dict.pop("event_id")
        event = session.query(models.Event).filter_by(event_id=event_id).first()
        if event is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Event.metadata.tables["event"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in event_dict.keys():
                    setattr(event, key, event_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        event_dict = event.get_dict()
        # un collaborateur du service support ne peut modifier que les évènements qui lui sont assignés
        if user_service.lower() == "oc12_support":
            if int(current_user_collaborator_id) != event_dict["collaborator_id"]:
                raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
        session.commit()
        return event.get_dict()

    def update_location(self, session, location_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie True si réussie..
        """
        location_id = location_dict.pop("location_id")
        location = (
            session.query(models.Location).filter_by(location_id=location_id).first()
        )
        if location is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Location.metadata.tables["location"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in location_dict.keys():
                    setattr(location, key, location_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return location.get_dict()

    def update_role(self, session, role_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un rôle pour collaborateur.
        Requête de la base de données et renvoie True si réussie..
        """
        role_id = role_dict.pop("role_id")
        role = (
            session.query(models.Collaborator_Role).filter_by(role_id=role_id).first()
        )
        if role is None:
            raise exceptions.CustomIdMatchNothingException()
        keys_to_explore = models.Collaborator_Role.metadata.tables[
            "collaborator_role"
        ].columns.keys()

        try:
            for key in keys_to_explore:
                if key in role_dict.keys():
                    setattr(role, key, role_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()

        return role.get_dict()
