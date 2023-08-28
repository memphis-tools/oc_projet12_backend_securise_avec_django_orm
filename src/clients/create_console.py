"""
Description:
Client en mode console, dédié aux mises à jour (ajout, modification, suppression).
"""
import sys
from datetime import datetime
from rich import print
import logtail

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.create_views import CreateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings, logtail_handler
    from src.utils import utils
    from src.validators import add_data_validators
    from src.validators.data_syntax.fr import validators
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from forms import forms
    from models import models
    from views.create_views import CreateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings, logtail_handler
    from utils import utils
    from validators import add_data_validators
    from validators.data_syntax.fr import validators


LOGGER = logtail_handler.logger


class ConsoleClientForCreate:
    """
    Description:
    Dédiée à l'usage d'un client en mode console, pour la création /ajout de données.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        On instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name=db_name)
        self.app_dict = language_bridge.LanguageBridge()
        utils.display_banner()
        self.app_view = AppViews(db_name=db_name)
        self.create_app_view = CreateAppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    def ask_for_a_client_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        client_id = forms.submit_a_client_get_form()
        try:
            if client_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        client_lookup = None
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(client_id)
            return client_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            sys.exit(0)

    def ask_for_a_contract_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        contract_id = forms.submit_a_contract_get_form()
        try:
            if contract_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        contract_lookup = None
        try:
            # on propose de rechercher le contrat
            contract_lookup = self.app_view.get_contracts_view().get_contract(
                contract_id
            )
            return contract_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message,)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False

    def ask_for_a_contract_custom_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Fonction renvoie le custom_id saisi
        """
        contract_custom_id = forms.submit_a_contract_get_form()
        try:
            if contract_custom_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        return contract_custom_id

    def ask_for_a_company_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        company_id = forms.submit_a_company_get_form()
        try:
            if company_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        company_lookup = None
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(company_id)
            return company_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message,)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False

    def ask_for_a_department_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        department_id = forms.submit_a_collaborator_department_get_form()
        try:
            if department_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        department_lookup = None
        try:
            # on propose de rechercher led département /service
            department_lookup = self.app_view.get_departments_view().get_department(
                department_id
            )
            return department_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False

    def ask_for_a_event_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        event_id = forms.submit_a_event_get_form()
        try:
            if event_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        event_lookup = None
        try:
            # on propose de rechercher l'évènement
            event_lookup = self.app_view.get_events_view().get_event(event_id)
            return event_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False
        return True

    def ask_for_a_location_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        location_id = forms.submit_a_location_get_form()
        try:
            if location_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        location_lookup = None
        try:
            # on propose de rechercher la localité
            location_lookup = self.app_view.get_locations_view().get_location(
                location_id
            )
            if isinstance(location_lookup.id, int):
                raise exceptions.LocationCustomIdAlReadyExists()
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return location_id

    def ask_for_a_role_id(self):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        role_id = forms.submit_a_collaborator_role_get_form()
        try:
            if role_id == "":
                raise exceptions.CustomIdEmptyException()
        except exceptions.CustomIdEmptyException:
            message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
            printer.print_message("info", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.info(message)
            return False
        role_lookup = None
        try:
            # on propose de rechercher le role
            role_lookup = self.app_view.get_roles_view().get_role(role_id)
            return role_lookup.id
        except AttributeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False

    @utils.authentication_permission_decorator
    def add_client(self, client_attributes_dict=""):
        # rechercher le id de l'utilisateur courant
        # obtenir le token décodé (et valide)
        # demander mot de passe à utilisateur en cours
        # controler le mot de passe
        """
        Description:
        Dédiée à créer un client de l'entreprise.
        """
        client_id = ""
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, registration_number
        )
        message = ""
        try:
            if (
                "client" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if client_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(client_attributes_dict)
                dict_is_valid = add_data_validators.add_client_data_is_valid(
                    client_attributes_dict
                )
                client_attributes_dict["commercial_contact"] = user_id
                if data_is_dict and dict_is_valid:
                    client_id = self.create_app_view.get_clients_view().add_client(
                        models.Client(**client_attributes_dict)
                    )
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                company_id = self.ask_for_a_company_id()
                if not company_id:
                    # on entame le dialogue pour enregistrer localité, entreprise.
                    location_id = self.add_location()
                    company_id = self.add_company(company_location_id=location_id)

                client_attributes_dict = forms.submit_a_client_create_form()
                client_attributes_dict["company_id"] = company_id
                client_attributes_dict["commercial_contact"] = user_id
                client_id = self.create_app_view.get_clients_view().add_client(models.Client(**client_attributes_dict))
            message = f"Creation client {client_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(client={ 'client_id': client_attributes_dict['client_id'] }):
                    LOGGER.info(message)
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        return message

    @utils.authentication_permission_decorator
    def add_collaborator(self, collaborator_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator = ""
        message = ""
        try:
            if (
                "collaborator" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(collaborator_attributes_dict)
                dict_is_valid = add_data_validators.add_collaborator_data_is_valid(
                    collaborator_attributes_dict
                )
                if data_is_dict and dict_is_valid:
                    collaborator = models.Collaborator(**collaborator_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                collaborator_attributes_dict = forms.submit_a_collaborator_create_form()
                department_custom_id = collaborator_attributes_dict["department_id"]
                department_primary_id = utils.get_department_id_from_custom_id(
                    self.app_view.session, department_custom_id
                )
                collaborator_attributes_dict["department_id"] = department_primary_id

                role_custom_id = collaborator_attributes_dict["role_id"]
                role_primary_id = utils.get_role_id_from_role_custom_id(
                    self.app_view.session, role_custom_id
                )
                collaborator_attributes_dict["role_id"] = role_primary_id

                collaborator = models.Collaborator(**collaborator_attributes_dict)
            collaborator_id = self.create_app_view.get_collaborators_view().add_collaborator(collaborator)
            message = f"Creation collaborator {collaborator.registration_number} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(collaborator={'registration_number': collaborator.registration_number }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.CollaboratorAlreadyExistException:
            raise exceptions.CollaboratorAlreadyExistException()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_company(self, company_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company = ""
        message = ""
        try:
            if (
                "company" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if company_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(company_attributes_dict)
                dict_is_valid = add_data_validators.add_company_data_is_valid(
                    company_attributes_dict
                )
                if data_is_dict and dict_is_valid:
                    company = models.Company(**company_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                company_location_id = self.ask_for_a_location_id()
                if not company_location_id:
                    company_location_id = self.add_location()
                company_attributes_dict = forms.submit_a_company_create_form(
                    company_location_id=company_location_id
                )
                company = models.Company(**company_attributes_dict)
                company.creation_date = datetime.now()
            company_id = self.create_app_view.get_companies_view().add_company(company)
            message = f"Creation company {company_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(company={ 'company_id': company_attributes_dict['company_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_contract(self, contract_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, registration_number
        )
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract = ""
        message = ""
        try:
            if (
                "contract" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if contract_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(contract_attributes_dict)
                dict_is_valid = add_data_validators.add_contract_data_is_valid(
                    contract_attributes_dict
                )
                if data_is_dict and dict_is_valid:
                    contract = models.Contract(**contract_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                client_id = self.ask_for_a_client_id()
                if not client_id:
                    raise exceptions.ClientNotFoundWithClientId()
                contract_attributes_dict = forms.submit_a_contract_create_form()
                contract_attributes_dict["client_id"] = client_id
                contract = models.Contract(**contract_attributes_dict)
                contract.creation_date = datetime.now()
            contract_id = self.create_app_view.get_contracts_view().add_contract(contract)
            message = f"Creation contract {contract_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(contract={ 'contract_id': contract_attributes_dict['contract_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_department(self, department_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department = ""
        message = ""
        try:
            if (
                "collaborator_department" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if department_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(department_attributes_dict)
                dict_is_valid = add_data_validators.add_department_data_is_valid(
                    department_attributes_dict
                )
                if data_is_dict and dict_is_valid:
                    department = models.Collaborator_Department(
                        **department_attributes_dict
                    )
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                department_attributes_dict = (
                    forms.submit_a_collaborator_department_create_form()
                )
                department = models.Collaborator_Department(
                    **department_attributes_dict
                )
                department.creation_date = datetime.now()
            department_id = self.create_app_view.get_departments_view().add_department(department)
            message = f"Creation department {department_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(department={ 'department_id': department_attributes_dict['department_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_event(self, event_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        registration_number = str(decoded_token["registration_number"])
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event = ""
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, registration_number
        )
        message = ""
        try:
            if (
                "event" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if event_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(event_attributes_dict)
                dict_is_valid = add_data_validators.add_event_data_is_valid(event_attributes_dict)
                custom_id = utils.get_contract_custom_id_from_contract_id(
                    self.app_view.session,
                    event_attributes_dict["contract_id"]
                )
                contract = self.app_view.get_contracts_view().get_contract(contract_id=custom_id)
                commercial_id_attached_to_contract = contract.client.commercial_contact
                if commercial_id_attached_to_contract != int(user_id):
                    raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
                if data_is_dict and dict_is_valid:
                    event = models.Event(**event_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                contract_id_asked = self.ask_for_a_contract_custom_id()
                contract = self.app_view.get_contracts_view().get_contract(contract_id=contract_id_asked)
                commercial_id_attached_to_contract = contract.client.commercial_contact
                if not contract:
                    raise exceptions.ContractNotFoundWithContractId()
                if commercial_id_attached_to_contract != int(user_id):
                    raise exceptions.CommercialCollaboratorIsNotAssignedToContract()

                event_attributes_dict = forms.submit_a_event_create_form()
                event_attributes_dict["collaborator_id"] = user_id
                event_attributes_dict["contract_id"] = contract.id
                event = models.Event(**event_attributes_dict)
                event.creation_date = datetime.now()
            event_id = self.create_app_view.get_events_view().add_event(user_id, event)
            message = f"Creation event {event_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(event={ 'event_id': event_attributes_dict['event_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ContractNotFoundWithContractId:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ContractNotFoundWithContractId()
            sys.exit(0)
        except exceptions.CommercialCollaboratorIsNotAssignedToContract:
            message = self.app_dict.get_appli_dictionnary()["COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
            sys.exit(0)
        except exceptions.SupportCollaboratorIsNotAssignedToEvent:
            message = self.app_dict.get_appli_dictionnary()["SUPPORT_COLLABORATOR_IS_NOT_ASSIGNED_TO_EVENT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_location(self, location_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location = ""
        message = ""
        try:
            if (
                "location" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if location_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(location_attributes_dict)
                dict_is_valid = add_data_validators.add_location_data_is_valid(
                    location_attributes_dict
                )
                complement_adresse_valid = validators.is_complement_adresse_valid(
                    location_attributes_dict["complement_adresse"]
                )
                if data_is_dict and dict_is_valid and complement_adresse_valid:
                    location = models.Location(**location_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                location_id = self.ask_for_a_location_id()
                location_attributes_dict = forms.submit_a_location_create_form(
                    location_id
                )
                location = models.Location(**location_attributes_dict)
                location.creation_date = datetime.now()
            location_id = self.create_app_view.get_locations_view().add_location(location)
            message = f"Creation location {location_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(location={ 'location_id': location_attributes_dict['location_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.LocationCustomIdAlReadyExists:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_ALREADY_EXISTS_"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.LocationCustomIdAlReadyExists()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_role(self, role_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role = ""
        message = ""
        try:
            if (
                "collaborator_role" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if role_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(role_attributes_dict)
                dict_is_valid = add_data_validators.add_role_data_is_valid(role_attributes_dict)
                if data_is_dict and dict_is_valid:
                    role = models.Collaborator_Role(**role_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                role_attributes_dict = forms.submit_a_collaborator_role_create_form()
                role = models.Collaborator_Role(**role_attributes_dict)
                role.creation_date = datetime.now()
            role_id = self.create_app_view.get_roles_view().add_role(role)
            message = f"Creation role {role_id} by {registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(role={ 'role_id': role_attributes_dict['role_id'] }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()["SUPPLIED_DATA_DO_NOT_MATCH_MODEL"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.ApplicationErrorException()
            sys.exit(0)
