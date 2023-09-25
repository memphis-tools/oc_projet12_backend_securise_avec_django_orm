"""
Description:
Client en mode console, dédié aux mises à jour (ajout, modification, suppression).
"""
from datetime import datetime
import logtail
from rich.prompt import Prompt
import sqlalchemy

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.crud_views.create_views import CreateAppViews
    from src.views.crud_views.views import AppViews
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
    from views.crud_views.create_views import CreateAppViews
    from views.crud_views.views import AppViews
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
        self.app_view = AppViews(db_name=db_name)
        self.create_app_view = CreateAppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        self.decoded_token = self.jwt_view.get_decoded_token()
        self.user_service = str(self.decoded_token["department"]).upper()
        self.registration_number = str(self.decoded_token["registration_number"])
        self.allowed_crud_tables = eval(f"settings.{self.user_service}_CRUD_TABLES")
        utils.display_banner(registration_number=self.registration_number)

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
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

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
            printer.print_message(
                "error",
                message,
            )
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
            printer.print_message(
                "error",
                message,
            )
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
            printer.print_message("error", message)
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
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            return False
        return True

    def ask_for_a_location_id(self, location_id=""):
        """
        Description:
        Proposer à l'utilisateur de saisir un 'custom id' relatif au modèle.
        Si un résultat correspond à la requête, son 'id' (primary key) est renvoyé.
        Si aucun résultat, on lève une exception CustomIdEmptyException.
        """
        if location_id == "":
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
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except exceptions.LocationCustomIdAlReadyExists:
            return location_lookup.id

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
            printer.print_message("error", message)
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
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, self.registration_number
        )
        message = ""
        try:
            grant_valid = bool("client" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()
            if client_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(client_attributes_dict)
                dict_is_valid = add_data_validators.add_client_data_is_valid(
                    client_attributes_dict
                )
                existing_client = self.app_view.get_clients_view().get_client(
                    client_attributes_dict["client_id"]
                )
                if existing_client is not None:
                    raise exceptions.ClientAlreadyExistException()

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
                    # on entame le dialogue pour enregistrer entreprise du client.
                    company_id = self.add_company()
                    company_id = self.ask_for_a_company_id()

                asked_client_id = Prompt.ask("Client id: ")
                if not asked_client_id:
                    raise exceptions.CustomIdEmptyException()
                existing_client = self.app_view.get_clients_view().get_client(
                    asked_client_id
                )
                if existing_client is not None:
                    raise exceptions.ClientAlreadyExistException()

                client_attributes_dict = forms.submit_a_client_create_form(
                    client_id=asked_client_id
                )
                client_attributes_dict["company_id"] = company_id
                client_attributes_dict["commercial_contact"] = user_id
                client_id = self.create_app_view.get_clients_view().add_client(
                    models.Client(**client_attributes_dict)
                )
            message = f"Creation client {client_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    client={
                        "client_id": client_attributes_dict["client_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
        except exceptions.ClientAlreadyExistException:
            raise exceptions.ClientAlreadyExistException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()
        return message

    @utils.authentication_permission_decorator
    def add_collaborator(self, collaborator_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        collaborator = ""
        message = ""
        try:
            grant_valid = bool("collaborator" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_gestion":
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(
                    collaborator_attributes_dict
                )
                dict_is_valid = add_data_validators.add_collaborator_data_is_valid(
                    collaborator_attributes_dict
                )
                existing_registration_number = (
                    self.app_view.get_collaborators_view().get_collaborator(
                        collaborator_attributes_dict["registration_number"]
                    )
                )
                if existing_registration_number is not None:
                    raise exceptions.RegistrationNumberAlreadyExistException()

                if data_is_dict and dict_is_valid:
                    collaborator = models.Collaborator(**collaborator_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                asked_registration_number = Prompt.ask("Registration number: ")
                if not asked_registration_number:
                    raise exceptions.CustomIdEmptyException()
                existing_registration_number = (
                    self.app_view.get_collaborators_view().get_collaborator(
                        asked_registration_number
                    )
                )
                if existing_registration_number is not None:
                    raise exceptions.RegistrationNumberAlreadyExistException()

                collaborator_attributes_dict = forms.submit_a_collaborator_create_form(
                    registration_number=asked_registration_number
                )
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
            collaborator_id = (
                self.create_app_view.get_collaborators_view().add_collaborator(
                    collaborator
                )
            )
            message = f"Creation collaborator {collaborator.registration_number} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    collaborator={
                        "registration_number": collaborator.registration_number,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except sqlalchemy.exc.ProgrammingError:
            raise exceptions.RegistrationNumberAlreadyExistException()
        except exceptions.RegistrationNumberEmptyException:
            raise exceptions.RegistrationNumberEmptyException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    collaborator={
                        "collaborator_attributes_dict": collaborator_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_company(self, company_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        message = ""
        try:
            grant_valid = bool("company" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()
            if company_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(company_attributes_dict)
                dict_is_valid = add_data_validators.add_company_data_is_valid(
                    company_attributes_dict
                )
                existing_company = self.app_view.get_companies_view().get_company(
                    company_attributes_dict["company_id"]
                )
                if existing_company is not None:
                    raise exceptions.CompanyAlreadyExistException()

                if data_is_dict and dict_is_valid:
                    models.Company(**company_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                location_id = Prompt.ask("id localité: ")
                company_location_id = self.ask_for_a_location_id(location_id)
                if not company_location_id:
                    company_location_id = self.add_location(location_id=location_id)

                location_id = utils.get_location_id_from_location_custom_id(
                    self.app_view.session, location_id
                )

                asked_company_id = Prompt.ask("Company id: ")
                if not asked_company_id:
                    raise exceptions.CustomIdEmptyException()
                existing_company = self.app_view.get_companies_view().get_company(
                    asked_company_id
                )
                if existing_company is not None:
                    raise exceptions.CompanyAlreadyExistException()

                company_attributes_dict = forms.submit_a_company_create_form(
                    company_location_id=location_id, company_id=asked_company_id
                )
            company_id = self.create_app_view.get_companies_view().add_company(
                models.Company(**company_attributes_dict)
            )
            message = f"Creation company {company_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    company={
                        "company_id": company_attributes_dict["company_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.CompanyAlreadyExistException:
            raise exceptions.CompanyAlreadyExistException()
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    company={
                        "company_attributes_dict": company_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_contract(self, contract_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un contrat pour le client.
        """
        contract = ""
        message = ""
        try:
            grant_valid = bool("contract" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_gestion":
                raise exceptions.InsufficientPrivilegeException()
            if contract_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(
                    contract_attributes_dict
                )
                dict_is_valid = add_data_validators.add_contract_data_is_valid(
                    contract_attributes_dict
                )
                existing_contract = self.app_view.get_contracts_view().get_contract(
                    contract_attributes_dict["contract_id"]
                )
                if existing_contract is not None:
                    raise exceptions.ContractAlreadyExistException()
                if data_is_dict and dict_is_valid:
                    contract = models.Contract(**contract_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                client_id = self.ask_for_a_client_id()
                if not client_id:
                    raise exceptions.CustomIdEmptyException()
                asked_contract_id = Prompt.ask("Contract id: ")
                if not asked_contract_id:
                    raise exceptions.ContractNotFoundWithContractId()
                existing_contract = self.app_view.get_contracts_view().get_contract(
                    asked_contract_id
                )
                if existing_contract is not None:
                    raise exceptions.ContractAlreadyExistException()
                contract_attributes_dict = forms.submit_a_contract_create_form(
                    contract_id=asked_contract_id
                )
                contract_attributes_dict["client_id"] = client_id
                contract = models.Contract(**contract_attributes_dict)
                contract.creation_date = datetime.now()
            contract_id = self.create_app_view.get_contracts_view().add_contract(
                contract
            )
            message = f"Creation contract {contract_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    contract={
                        "contract_id": contract_attributes_dict["contract_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.ContractAlreadyExistException:
            raise exceptions.ContractAlreadyExistException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    contract={
                        "contract_attributes_dict": contract_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_department(self, department_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        department = ""
        message = ""
        try:
            grant_valid = bool(
                "collaborator_department" not in self.allowed_crud_tables
            )
            if grant_valid or self.user_service.lower() != "oc12_gestion":
                raise exceptions.InsufficientPrivilegeException()
            if department_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(
                    department_attributes_dict
                )
                dict_is_valid = add_data_validators.add_department_data_is_valid(
                    department_attributes_dict
                )
                existing_department = (
                    self.app_view.get_departments_view().get_department(
                        department_attributes_dict["department_id"]
                    )
                )
                if existing_department is not None:
                    raise exceptions.DepartmentAlreadyExistException()
                if data_is_dict and dict_is_valid:
                    department = models.Collaborator_Department(
                        **department_attributes_dict
                    )
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                asked_department_id = Prompt.ask("Department id: ")
                if not asked_department_id:
                    raise exceptions.CustomIdEmptyException()
                existing_department = (
                    self.app_view.get_departments_view().get_department(
                        asked_department_id
                    )
                )
                if existing_department is not None:
                    raise exceptions.DepartmentAlreadyExistException()

                department_attributes_dict = (
                    forms.submit_a_collaborator_department_create_form(
                        department_id=asked_department_id
                    )
                )
                department = models.Collaborator_Department(
                    **department_attributes_dict
                )
                department.creation_date = datetime.now()
            department_id = self.create_app_view.get_departments_view().add_department(
                department
            )
            message = (
                f"Creation department {department_id} by {self.registration_number}"
            )
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    department={
                        "department_id": department_attributes_dict["department_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.DepartmentAlreadyExistException:
            raise exceptions.DepartmentAlreadyExistException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.DepartmentAlreadyExistException:
            raise exceptions.DepartmentAlreadyExistException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    department={
                        "department_attributes_dict": department_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_event(self, event_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un évènement de l'entreprise.
        """
        event = ""
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, self.registration_number
        )
        message = ""
        try:
            grant_valid = bool("event" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()
            if event_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(event_attributes_dict)
                dict_is_valid = add_data_validators.add_event_data_is_valid(
                    event_attributes_dict
                )
                custom_id = utils.get_contract_custom_id_from_contract_id(
                    self.app_view.session, event_attributes_dict["contract_id"]
                )
                contract = self.app_view.get_contracts_view().get_contract(
                    contract_id=custom_id
                )
                commercial_id_attached_to_contract = contract.client.commercial_contact
                existing_event = self.app_view.get_events_view().get_event(
                    event_attributes_dict["event_id"]
                )
                if existing_event is not None:
                    raise exceptions.EventAlreadyExistException()
                if commercial_id_attached_to_contract != int(user_id):
                    raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
                if contract.status == "unsigned":
                    raise exceptions.ContractUnsignedException()
                if contract.status == "canceled":
                    raise exceptions.ContractCanceledException()
                if data_is_dict and dict_is_valid:
                    event = models.Event(**event_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                contract_id_asked = self.ask_for_a_contract_custom_id()
                contract = self.app_view.get_contracts_view().get_contract(
                    contract_id=contract_id_asked
                )
                if contract.status == "unsigned":
                    raise exceptions.ContractUnsignedException()
                if contract.status == "canceled":
                    raise exceptions.ContractCanceledException()
                if not contract:
                    raise exceptions.ContractNotFoundWithContractId()
                commercial_id_attached_to_contract = contract.client.commercial_contact
                if commercial_id_attached_to_contract != int(user_id):
                    raise exceptions.CommercialCollaboratorIsNotAssignedToContract()

                location_id = Prompt.ask("id localité: ")
                company_location_id = self.ask_for_a_location_id(location_id)
                if not company_location_id:
                    company_location_id = self.add_location(location_id=location_id)

                location_id = utils.get_location_id_from_location_custom_id(
                    self.app_view.session, location_id
                )

                asked_event_id = Prompt.ask("Event id: ")
                if not asked_event_id:
                    raise exceptions.CustomIdEmptyException()
                existing_event = self.app_view.get_events_view().get_event(
                    asked_event_id
                )
                if existing_event is not None:
                    raise exceptions.EventAlreadyExistException()

                event_attributes_dict = forms.submit_a_event_create_form(
                    event_id=asked_event_id
                )
                event_attributes_dict["contract_id"] = contract.id
                event_attributes_dict["location_id"] = location_id
                event_attributes_dict["client_id"] = contract.client_id
                event = models.Event(**event_attributes_dict)
                event.creation_date = datetime.now()
            event_id = self.create_app_view.get_events_view().add_event(user_id, event)
            message = f"Creation event {event_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "event_id": event_attributes_dict["event_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.EventAlreadyExistException:
            raise exceptions.EventAlreadyExistException()
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.ContractCanceledException:
            message = self.app_dict.get_appli_dictionnary()["CONTRACT_CANCELED"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except exceptions.ContractUnsignedException:
            message = self.app_dict.get_appli_dictionnary()["CONTRACT_UNSIGNED"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.ContractNotFoundWithContractId:
            raise exceptions.ContractNotFoundWithContractId()
        except exceptions.CommercialCollaboratorIsNotAssignedToContract:
            message = self.app_dict.get_appli_dictionnary()[
                "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
        except exceptions.SupportCollaboratorIsNotAssignedToEvent:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPORT_COLLABORATOR_IS_NOT_ASSIGNED_TO_EVENT"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "event_attributes_dict": event_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_location(self, location_attributes_dict="", location_id=""):
        """
        Description:
        Dédiée à enregistrer une localité.
        """
        location = ""
        message = ""
        try:
            grant_valid = bool("location" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()
            if location_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(
                    location_attributes_dict
                )
                dict_is_valid = add_data_validators.add_location_data_is_valid(
                    location_attributes_dict
                )
                complement_adresse_valid = validators.is_complement_adresse_valid(
                    location_attributes_dict["complement_adresse"]
                )
                existing_location = self.app_view.get_locations_view().get_location(
                    location_attributes_dict["location_id"]
                )
                if existing_location is not None:
                    raise exceptions.LocationAlreadyExistException()
                if data_is_dict and dict_is_valid and complement_adresse_valid:
                    location = models.Location(**location_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                asked_location_id = Prompt.ask("Location id: ")
                if not asked_location_id:
                    raise exceptions.CustomIdEmptyException()
                existing_location = self.app_view.get_locations_view().get_location(
                    asked_location_id
                )
                if existing_location is not None:
                    raise exceptions.LocationAlreadyExistException()

                location_attributes_dict = forms.submit_a_location_create_form(
                    asked_location_id
                )
                location = models.Location(**location_attributes_dict)
                location.creation_date = datetime.now()
            location_id = self.create_app_view.get_locations_view().add_location(
                location
            )
            message = f"Creation location {location_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    location={
                        "location_id": location_attributes_dict["location_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.LocationAlreadyExistException:
            raise exceptions.LocationAlreadyExistException()
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    location={
                        "location_attributes_dict": location_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()

    @utils.authentication_permission_decorator
    def add_role(self, role_attributes_dict=""):
        """
        Description:
        Dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        role = ""
        message = ""
        try:
            grant_valid = bool("collaborator_role" not in self.allowed_crud_tables)
            if grant_valid or self.user_service.lower() != "oc12_gestion":
                raise exceptions.InsufficientPrivilegeException()
            if role_attributes_dict != "":
                data_is_dict = add_data_validators.data_is_dict(role_attributes_dict)
                dict_is_valid = add_data_validators.add_role_data_is_valid(
                    role_attributes_dict
                )
                existing_role = self.app_view.get_roles_view().get_role(
                    role_attributes_dict["role_id"]
                )
                if existing_role is not None:
                    raise exceptions.RoleAlreadyExistException()
                if data_is_dict and dict_is_valid:
                    role = models.Collaborator_Role(**role_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                asked_role_id = Prompt.ask("Role id: ")
                if not asked_role_id:
                    raise exceptions.CustomIdEmptyException()
                existing_role = self.app_view.get_roles_view().get_role(asked_role_id)
                if existing_role is not None:
                    raise exceptions.RoleAlreadyExistException()

                role_attributes_dict = forms.submit_a_collaborator_role_create_form(
                    role_id=asked_role_id
                )
                role = models.Collaborator_Role(**role_attributes_dict)
                role.creation_date = datetime.now()
            role_id = self.create_app_view.get_roles_view().add_role(role)
            message = f"Creation role {role_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    role={
                        "role_id": role_attributes_dict["role_id"],
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.RoleAlreadyExistException:
            raise exceptions.RoleAlreadyExistException()
        except exceptions.CustomIdEmptyException:
            raise exceptions.CustomIdEmptyException()
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.SuppliedDataNotMatchModel:
            message = self.app_dict.get_appli_dictionnary()[
                "SUPPLIED_DATA_DO_NOT_MATCH_MODEL"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    location={
                        "role_attributes_dict": role_attributes_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.error(message)
            raise exceptions.SuppliedDataNotMatchModel()
        except Exception:
            raise exceptions.ApplicationErrorException()
