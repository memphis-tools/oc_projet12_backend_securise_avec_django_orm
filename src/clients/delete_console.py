"""
Description:
Client en mode console, dédié aux mises à jour pour suppression.
"""
import sys
import logtail

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.forms import forms
    from src.views.delete_views import DeleteAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings, logtail_handler
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from forms import forms
    from views.delete_views import DeleteAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings, logtail_handler
    from utils import utils


LOGGER = logtail_handler.logger


class ConsoleClientForDelete:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la création /ajout de données.
    """

    def __init__(self, custom_id="", db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        On instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name=db_name)
        self.app_dict = language_bridge.LanguageBridge()
        utils.display_banner()
        self.app_view = AppViews(db_name=db_name)
        self.delete_app_view = DeleteAppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    def ask_for_a_client_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        client_id = ""
        if custom_id == "":
            client_id = forms.submit_a_client_get_form()
            try:
                if client_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            client_lookup = None
        else:
            client_id = custom_id
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(
                client_id=client_id
            )
            return client_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_contract_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            contract_id = forms.submit_a_contract_get_form()
            try:
                if contract_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            contract_lookup = None
        else:
            contract_id = custom_id
        try:
            # on propose de rechercher le contrat
            contract_lookup = self.app_view.get_contracts_view().get_contract(
                contract_id=contract_id
            )
            return contract_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_collaborator_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            registration_number = forms.submit_a_collaborator_get_form()
            try:
                if registration_number == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            collaborator_lookup = None
        else:
            registration_number = custom_id
        try:
            # on propose de rechercher le collaborateur
            collaborator_lookup = (
                self.app_view.get_collaborators_view().get_collaborator(
                    registration_number
                )
            )
            return collaborator_lookup.id
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_company_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            company_id = forms.submit_a_company_get_form()
            try:
                if company_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            company_lookup = None
        else:
            company_id = custom_id
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(
                company_id=company_id
            )
            return company_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_department_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            department_id = forms.submit_a_collaborator_department_get_form()
            try:
                if department_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            department_lookup = None
        else:
            department_id = custom_id
        try:
            # on propose de rechercher led département /service
            department_lookup = self.app_view.get_departments_view().get_department(
                department_id=department_id
            )
            return department_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_event_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            event_id = forms.submit_a_event_get_form()
            try:
                if event_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            event_lookup = None
        else:
            event_id = custom_id
        try:
            # on propose de rechercher l'évènement
            event_lookup = self.app_view.get_events_view().get_event(event_id=event_id)
            return event_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    def ask_for_a_location_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            location_id = forms.submit_a_location_get_form()
            try:
                if location_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            location_lookup = None
        else:
            location_id = custom_id
        try:
            # on propose de rechercher la localité
            location_lookup = self.app_view.get_locations_view().get_location(
                location_id=location_id
            )
            return location_lookup.get_dict()
        except Exception:
            return False

    def ask_for_a_role_id(self, custom_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if custom_id == "":
            role_id = forms.submit_a_collaborator_role_get_form()
            try:
                if role_id == "":
                    raise exceptions.CustomIdEmptyException()
            except exceptions.CustomIdEmptyException:
                message = self.app_dict.get_appli_dictionnary()["MISSING_CUSTOM_ID"]
                printer.print_message("info",message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                	LOGGER.info(message)
                return False
            role_lookup = None
        else:
            role_id = custom_id
        try:
            # on propose de rechercher le role
            role_lookup = self.app_view.get_roles_view().get_role(role_id=role_id)
            return role_lookup.get_dict()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            return False

    @utils.authentication_permission_decorator
    def delete_client(self, client_custom_id=""):
        # rechercher le id de l'utilisateur courant
        # obtenir le token décodé (et valide)
        # demander mot de passe à utilisateur en cours
        # controler le mot de passe
        """
        Description:
        Dédiée à supprimer un client de l'entreprise.
        """
        client_id = ""
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        try:
            if (
                "client" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if client_custom_id != "":
                client_id = self.ask_for_a_client_id(client_custom_id)["id"]
            else:
                client_id = self.ask_for_a_client_id()["id"]

            client_id = self.delete_app_view.get_clients_view().delete_client(client_id)
            message = f"Suppression {client_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(user={
                    'client_id': client_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["CLIENT_RATTACHED_TO_CONTRACT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(client={
                    'client_id': client_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.ForeignKeyDependyException("")
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_collaborator(self, collaborator_custom_id=""):
        """
        Description:
        Dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator_id = ""
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_custom_id != "":
                collaborator_id = self.ask_for_a_collaborator_id(collaborator_custom_id)
            else:
                collaborator_id = self.ask_for_a_collaborator_id()
            collaborator_id = self.delete_app_view.get_collaborators_view().delete_collaborator(collaborator_id)
            message = f"Suppression {collaborator_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(collaborator={
                    'collaborator_id': collaborator_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["CLIENT_RATTACHED_TO_COLLABORATOR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(collaborator={
                    'collaborator_id': collaborator_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.ForeignKeyDependyException("")
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_company(self, company_custom_id=""):
        """
        Description:
        Dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company_id = ""
        try:
            if "company" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if company_custom_id != "":
                company_id = self.ask_for_a_company_id(company_custom_id)["id"]
            else:
                company_id = self.ask_for_a_company_id()["id"]

            company_id = self.delete_app_view.get_companies_view().delete_company(company_id)
            message = f"Suppression {company_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(user={
                    'company_id': company_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["COMPANY_RATTACHED_TO_CLIENT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(company={
                    'company_id': company_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.ForeignKeyDependyException("")
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_contract(self, contract_custom_id=""):
        """
        Description:
        Dédiée à enregistrer un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract_id = ""
        try:
            if "contract" not in allowed_crud_tables or user_service != "OC12_GESTION":
                raise exceptions.InsufficientPrivilegeException()
            if contract_custom_id != "":
                contract_id = self.ask_for_a_contract_id(contract_custom_id)["id"]
            else:
                contract_id = self.ask_for_a_contract_id()["id"]
            contract_id = self.delete_app_view.get_contracts_view().delete_contract(contract_id)
            message = f"Suppression {contract_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(contract={
                    'contract_id': contract_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["CONTRACT_RATTACHED_TO_EVENT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(contract={ 'contract_id': contract_id }):
                	LOGGER.error(message)
            raise exceptions.ForeignKeyDependyException("")
            sys.exit(0)
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_department(self, department_custom_id=""):
        """
        Description:
        Dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department_id = ""
        try:
            if "collaborator_department" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if department_custom_id != "":
                department_id = utils.get_department_id_from_department_custom_id(
                    self.app_view.session, department_custom_id
                )
            else:
                department_id = self.ask_for_a_department_id()["id"]

            department_id = self.delete_app_view.get_departments_view().delete_department(department_id)
            message = f"Suppression {department_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(department={
                    'department_id': department_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["DEPARTMENT_RATTACHED_TO_COLLABORATOR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(department={
                    'department_id': department_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.ForeignKeyDependyException("")
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_event(self, event_custom_id=""):
        """
        Description:
        Dédiée à enregistrer un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event_id = ""
        try:
            if "event" not in allowed_crud_tables or user_service != "OC12_GESTION":
                raise exceptions.InsufficientPrivilegeException()
            if event_custom_id != "":
                event_id = self.ask_for_a_event_id(event_custom_id)["id"]
            else:
                event_id = self.ask_for_a_event_id()["id"]

            event_id = self.delete_app_view.get_events_view().delete_event(event_id)
            message = f"Suppression {event_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(event={
                    'event_id': event_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_location(self, location_custom_id=""):
        """
        Description:
        Dédiée à enregistrer une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location_id = ""
        try:
            if "location" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if location_custom_id != "":
                location_id = self.ask_for_a_location_id(location_custom_id)["id"]
            else:
                location_id = self.ask_for_a_location_id()["id"]

            location_id = self.delete_app_view.get_locations_view().delete_location(location_id)
            message = f"Suppression {location_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(location={
                    'location_id': location_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["LOCATION_RATTACHED_TO_COMPANY"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(location={ 'location_id': location_id }):
                	LOGGER.error(message)
            raise exceptions.ForeignKeyDependyException("")
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def delete_role(self, role_custom_id=""):
        """
        Description:
        Dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role_id = ""
        try:
            if "collaborator_role" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if role_custom_id != "":
                role_id = self.ask_for_a_role_id(role_custom_id)["id"]
            else:
                role_id = self.ask_for_a_role_id()["id"]

            role_id = self.delete_app_view.get_roles_view().delete_role(role_id)
            message = f"Suppression {role_id} by {registration_number}"
            return message
        except exceptions.InsufficientPrivilegeException:
            message = self.app_dict.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(role={
                    'role_id': role_id,
                    'current_collaborator': registration_number,
                }):
                    LOGGER.info(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ForeignKeyDependyException:
            message = self.app_dict.get_appli_dictionnary()["ROLE_RATTACHED_TO_COLLABORATOR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(role={ 'role_id': role_id }):
                	LOGGER.error(message)
            raise exceptions.ForeignKeyDependyException("")
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
