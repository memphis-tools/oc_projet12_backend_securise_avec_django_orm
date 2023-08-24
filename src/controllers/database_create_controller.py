"""
Description:
Un controleur avec toutes méthodes pour ajouter des données.
"""
from sqlalchemy import text

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class DatabaseCreateController:
    """
    Description:
    Toutes les méthodes pour ajouter des données.
    """

    def __init__(self):
        self.app_dict = language_bridge.LanguageBridge()

    def add_client(self, session, client):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un client.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - client: une instance de la classe Client
        """
        try:
            session.add(client)
            session.commit()

            return client.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_collaborator(self, session, collaborator):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - collaborator: une instance de la classe Collaborator
        """
        try:
            session.add(collaborator)

            role = collaborator.registration_number
            password = settings.DEFAULT_NEW_COLLABORATOR_PASSWORD
            department_id = collaborator.department_id
            sql = text(
                f"""SELECT name FROM collaborator_department WHERE id = {department_id}"""
            )
            result = session.execute(sql).first()
            department = str(result[0]).lower()

            if department == "oc12_gestion":
                sql = text(
                    f"""CREATE ROLE {role} CREATEROLE LOGIN PASSWORD '{password}'"""
                )
                session.execute(sql)
            else:
                sql = text(f"""CREATE ROLE {role} LOGIN PASSWORD '{password}'""")
                session.execute(sql)

            sql = text(f"""GRANT {department} TO {role}""")
            session.execute(sql)

            session.commit()

            return collaborator.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_company(self, session, company):
        """
        Description:
        Fonction dédiée à servir la vue lors d'un ajout d'une entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - company: une instance de la classe Company
        """
        try:
            session.add(company)
            session.commit()

            return company.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
    def add_contract(self, session, contract):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un contrat.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - contract: une instance de la classe Contract
        """
        try:
            session.add(contract)
            session.commit()

            return contract.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_department(self, session, department):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un department /service pour l'entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - department: une instance de la classe Collaborator_Department
        """
        try:
            session.add(department)
            session.commit()
            return department.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_event(self, session, current_user_collaborator_id, event):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un évènement.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - current_user_collaborator_id: l'id de l'utilisateur courant (pas le custom id)
        - event: une instance de la classe Event
        """
        # un collaborateur du service commercial ne peut créer un évènements
        # que pour un contrat qu'il a conclu avec un client (signé ou non)
        if current_user_collaborator_id != event.get_dict()["collaborator_id"]:
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
        try:
            session.add(event)
            session.commit()
            return event.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_location(self, session, location):
        """
        Description:
        Fonction dédiée à servir la vue lors d'un ajout d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - location: une instance de la classe Location
        """
        try:
            session.add(location)
            session.commit()

            return location.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def add_role(self, session, role):
        """
        Description:
        Fonction dédiée à servir la vue lors de l'ajout d'un rôle pour collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        Paramètres:
        - role: une instance de la classe Collaborator_Role
        """
        try:
            session.add(role)
            session.commit()

            return role.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
