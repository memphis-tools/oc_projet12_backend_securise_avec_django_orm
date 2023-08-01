"""
Un controleur avec toutes méthodes pour mettre à jour des données.
"""

import sqlalchemy
try:
    from src.exceptions import exceptions
    from src.models import models
except ModuleNotFoundError:
    from exceptions import exceptions
    from models import models


class DatabaseUpdateController:
    """
    Description: Toutes les méthodes pour mettre à jour des données.
    """

    def update_client(self, session, client_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un client.
        Requête de la base de données et renvoie l'id enregistré.
        """
        client_id = client_dict.pop("client_id")
        client = session.query(models.Client).filter_by(client_id=client_id).first()
        try:
            client.first_name = client_dict["first_name"]
            client.last_name = client_dict["last_name"]
            client.employee_role = client_dict["employee_role"]
            client.email = client_dict["email"]
            client.telephone = client_dict["telephone"]
            client.company_id = client_dict["company_id"]
            client.commercial_contact = client_dict["commercial_contact"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_collaborator(self, session, collaborator_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        """
        collaborator_id = collaborator_dict.pop("registration_number")
        collaborator = session.query(models.User).filter_by(registration_number=collaborator_id).first()
        try:
            collaborator.username = collaborator_dict["username"]
            collaborator.department = collaborator_dict["department"]
            collaborator.role = collaborator_dict["role"]
            collaborator.email = collaborator_dict["email"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_company(self, session, company_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        """
        company_id = company_dict.pop("client_id")
        company = session.query(models.Company).filter_by(company_id=company_id).first()
        try:
            company.company_name = company_dict["company_name"]
            company.company_registration_number = company_dict["company_registration_number"]
            company.company_subregistration_number = company_dict["company_subregistration_number"]
            company.location_id = company_dict["location_id"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_contract(self, session, contract_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un contrat.
        Requête de la base de données et renvoie l'id enregistré.
        """
        contract_id = contract_dict.pop("contract_id")
        contract = session.query(models.Contract).filter_by(contract_id=contract_id).first()
        try:
            contract.full_amount_to_pay = contract_dict["full_amount_to_pay"]
            contract.remain_amount_to_pay = contract_dict["remain_amount_to_pay"]
            contract.status = contract_dict["status"]
            contract.client_id = contract_dict["client_id"]
            contract.collaborator_id = contract_dict["collaborator_id"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_department(self, session, department_dict):
        """
        Description:
        Fonction dédiée à servir la vue lors de la mise à jour d'un department /service de l'entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        """
        department_id = department_dict.pop("department_id")
        department = session.query(models.UserDepartment).filter_by(department_id=department_id).first()
        try:
            department.name = department_dict["name"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_event(self, session, event_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un évènement.
        Requête de la base de données et renvoie l'id enregistré.
        """
        event_id = event_dict.pop("event_id")
        event = session.query(models.Event).filter_by(event_id=event_id).first()
        try:
            event.title = event_dict["title"]
            event.contract_id = event_dict["contract_id"]
            event.client_id = event_dict["client_id"]
            event.collaborator_id = event_dict["collaborator_id"]
            event.location_id = event_dict["location_id"]
            event.event_start_date = event_dict["event_start_date"]
            event.event_end_date = event_dict["event_end_date"]
            event.attendees = event_dict["attendees"]
            event.notes = event_dict["notes"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_location(self, session, location_dict):
        """
        Description: Fonction dédiée à servir la vue lors d'une mise à jour d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie l'id enregistré.
        """
        location_id = location_dict.pop("location_id")
        location = session.query(models.Location).filter_by(location_id=location_id).first()
        try:
            location.adresse = location_dict["adresse"]
            location.complement_adresse = location_dict["complement_adresse"]
            location.code_postal = location_dict["code_postal"]
            location.ville = location_dict["ville"]
            location.pays = location_dict["pays"]
        except KeyError:
            pass
        session.commit()
        return True

    def update_role(self, session, role_dict):
        """
        Description: Fonction dédiée à servir la vue lors de la mise à jour d'un rôle pour collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        """
        role_id = role_dict.pop("role_id")
        role = session.query(models.UserRole).filter_by(role_id=role_id).first()
        try:
            role.name = role_dict["name"]
        except KeyError:
            pass
        session.commit()
        return True
