"""
Un controleur avec toutes méthodes pour mettre à jour des données.
"""

try:
    from src.models import models
except ModuleNotFoundError:
    from models import models


class DatabaseUpdateController:
    """
    Description: Toutes les méthodes pour mettre à jour des données.
    """

    def update_client(self, session, client_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un client.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        client_id = client_dict.pop("client_id")
        client = session.query(models.Client).filter_by(client_id=client_id).first()
        keys_to_explore = models.Client.metadata.tables["client"].columns.keys()
        try:
            for key in keys_to_explore:
                if key in client_dict.keys():
                    setattr(client, key, client_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return f"{client.client_id}"

    def update_collaborator(self, session, collaborator_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un collaborateur.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        collaborator_id = collaborator_dict.pop("registration_number")
        collaborator = (
            session.query(models.User)
            .filter_by(registration_number=collaborator_id)
            .first()
        )
        keys_to_explore = models.User.metadata.tables["collaborator"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in collaborator_dict.keys():
                    setattr(collaborator, key, collaborator_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return True

    def update_company(self, session, company_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une entreprise.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        company_id = company_dict.pop("company_id")
        company = session.query(models.Company).filter_by(company_id=company_id).first()
        companies =  session.query(models.Company).all()
        keys_to_explore = models.Company.metadata.tables["company"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in company_dict.keys():
                    setattr(company, key, company_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return True

    def update_contract(self, session, contract_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un contrat.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        contract_id = contract_dict.pop("contract_id")
        contract = (
            session.query(models.Contract).filter_by(contract_id=contract_id).first()
        )
        keys_to_explore = models.Contract.metadata.tables["contract"].columns.keys()
        try:
            for key in keys_to_explore:
                if key in contract_dict.keys():
                    setattr(contract, key, contract_dict[key])
        except KeyError:
            pass
        session.commit()
        return True

    def update_department(self, session, department_dict):
        """
        Description:
        Fonction dédiée à servir la vue lors de la mise à jour d'un department /service de l'entreprise.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        department_id = department_dict.pop("department_id")
        department = (
            session.query(models.UserDepartment)
            .filter_by(department_id=department_id)
            .first()
        )
        keys_to_explore = models.UserDepartment.metadata.tables[
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
        return True

    def update_event(self, session, event_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un évènement.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        event_id = event_dict.pop("event_id")
        event = session.query(models.Event).filter_by(event_id=event_id).first()
        keys_to_explore = models.Event.metadata.tables["event"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in event_dict.keys():
                    setattr(event, key, event_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return True

    def update_location(self, session, location_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        location_id = location_dict.pop("location_id")
        location = (
            session.query(models.Location).filter_by(location_id=location_id).first()
        )
        keys_to_explore = models.Location.metadata.tables["location"].columns.keys()

        try:
            for key in keys_to_explore:
                if key in location_dict.keys():
                    setattr(location, key, location_dict[key])
        except KeyError:
            session.flush()
            session.rollback()
        session.commit()
        return True

    def update_role(self, session, role_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un rôle pour collaborateur.
        Requête de la base de données et renvoie le custom_id (ou matricule pour employé) de l'instance.
        """
        role_id = role_dict.pop("role_id")
        role = session.query(models.UserRole).filter_by(role_id=role_id).first()
        keys_to_explore = models.UserRole.metadata.tables[
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
        return True
