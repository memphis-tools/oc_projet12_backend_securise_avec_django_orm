"""
Description:
Un controleur avec toutes méthodes GET.
"""
from sqlalchemy import text

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.models import models
    from src.utils import utils
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from models import models
    from utils import utils
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


class DatabaseReadController:
    """
    Description: Toutes les méthodes GET.
    """

    def get_filtered_models(self, session, user_query_filters_args, filtered_db_model):
        """
        Description:
        Fonction dédiée à servir la vue lors d'une requête filtrée à un modèle métier.
        On utilise une fonction utile "rebuild_filter_query" qui va construire une requête SQL.
        La requête SQL va être construite au traver des arguments précisés par l'utilisateur.
        Paramètre:
        - user_query_filters_args: chaine de caractère avec 1 ou plusieurs filtres.
            Exemple pour contrats: "status=signed et remain_amount_to_pay =>0"
        - filtered_db_model: chaine caractères qui nomme un modèle métier, soit
            Collaborator, Collaborator_Role, Client, Contract, etc
        """
        filter_to_apply_rebuilt_query = utils.rebuild_filter_query(
            user_query_filters_args, filtered_db_model, session
        )
        try:
            db_model_queryset = (
                session.query(eval(f"models.{filtered_db_model}"))
                # noter la possibilité de proposer des jointures, on ferait par exemple ceci
                # .join(models.Client, models.Event.client_id == models.Client.id)
                # .join(models.Collaborator, models.Event.collaborator_id == models.Collaborator.registration_number)
                # .join(models.Contract, models.Event.contract_id == models.Contract.contract_id)
                # .join(models.Location, models.Event.location_id == models.Location.location_id)
                .filter(text(filter_to_apply_rebuilt_query)).all()
            )
            return db_model_queryset
        except Exception as error:
            print(f"DEBUG SIR: {error}")
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_FAILURE"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)

    def get_client(self, session, client_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un client.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        Paramètres:
        - client_id: c'est le custom id (chaine libre)
        """
        try:
            db_client_queryset = (
                session.query(models.Client).filter_by(client_id=client_id).first()
            )

            return db_client_queryset
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_clients(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des clients de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        """
        db_collaborators_clients = session.query(models.Client).all()

        return db_collaborators_clients

    def get_collaborator(self, session, registration_number):
        """
        Description:
        Fonction dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(models.Collaborator)
                .filter_by(registration_number=registration_number)
                .first()
            )
            return db_collaborator_queryset
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_collaborator_join_department(self, session, registration_number):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise pour la création du token.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(
                    models.Collaborator.username, models.Collaborator_Department.name
                )
                .filter(
                    models.Collaborator.department_id == models.Collaborator_Department.id
                )
                .filter_by(registration_number=registration_number)
                .first()
            )
            return db_collaborator_queryset
        except Exception:
            raise exceptions.AuthenticationCredentialsFailed()

    def get_collaborators(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des utilisateurs de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator.
        """
        db_collaborators = session.query(models.Collaborator).all()
        return db_collaborators

    def get_company(self, session, company_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'une entreprise cliente.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        try:
            db_company_queryset = (
                session.query(models.Company).filter_by(company_id=company_id).first()
            )

            return db_company_queryset
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_companies(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des entreprises clientes de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        db_companies = session.query(models.Company).all()
        return db_companies

    def get_contract(self, session, contract_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un contrat de l'entreprise.
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

            return db_collaborators_contract
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_contracts(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des contrats de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        """
        db_collaborators_contracts = session.query(models.Contract).all()
        return db_collaborators_contracts

    def get_department(self, session, department_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un département /service de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator_Department.
        Paramètres:
        - department_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_department = (
                session.query(models.Collaborator_Department)
                .filter_by(department_id=department_id)
                .first()
            )

            return db_collaborators_department
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_departments(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des départements /services de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator_Department.
        """
        db_collaborators_department = session.query(
            models.Collaborator_Department
        ).all()

        return db_collaborators_department

    def get_event(self, session, event_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un évènement de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        Paramètres:
        - event_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_event = (
                session.query(models.Event).filter_by(event_id=event_id).first()
            )

            return db_collaborators_event
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_events(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des évènements de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        """
        db_collaborators_events = session.query(models.Event).all()

        return db_collaborators_events

    def get_location(self, session, location_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'une localité (entreprise ou évènement).
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

            return db_locations_queryset
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_locations(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des localisations des évènements.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        """
        db_collaborators_locations = session.query(models.Location).all()

        return db_collaborators_locations

    def get_role(self, session, role_id):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator_Role.
        Paramètres:
        - role_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_role = (
                session.query(models.Collaborator_Role)
                .filter_by(role_id=role_id)
                .first()
            )

            return db_collaborators_role
        except Exception:
            message = APP_DICT.get_appli_dictionnary()["DATABASE_QUERY_NO_MATCHES"]
            printer.print_message("info",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)

    def get_roles(self, session):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête des rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Collaborator_Role.
        """
        db_collaborators_role = session.query(models.Collaborator_Role).all()

        return db_collaborators_role
