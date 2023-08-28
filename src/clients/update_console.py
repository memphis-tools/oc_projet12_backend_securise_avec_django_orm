"""
Description:
Client en mode console, dédié aux mises à jour.
"""
import sys
import logtail

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.forms import forms
    from src.views.update_views import UpdateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings, logtail_handler
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from forms import forms
    from views.update_views import UpdateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings, logtail_handler
    from utils import utils


LOGGER = logtail_handler.logger


class ConsoleClientForUpdate:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la mise à jour de données.
    """

    def __init__(self, custom_id="", db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name=db_name)
        self.app_dict = language_bridge.LanguageBridge()
        utils.display_banner()
        self.app_view = AppViews(db_name=db_name)
        self.update_app_view = UpdateAppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    @utils.authentication_permission_decorator
    def update_client(self, custom_partial_dict, db_name=f"{settings.DATABASE_NAME}", user_query_filters_args=""):
        # rechercher le id de l'utilisateur courant
        # obtenir le token décodé (et valide)
        # demander mot de passe à utilisateur en cours
        # controler le mot de passe
        """
        Description:
        Dédiée à mettre à jour un client de l'entreprise.
        Paramètres:
        - custom_partial_dict: un dictionnaire, exemple:
            " {'client_id': 'DBLATT85', 'commercial_contact': 'ab123456789'} "
        """
        client_id = ""
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        user_collaborator_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, r_number)}"
        try:
            if (
                "client" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()

            if ("commercial_contact" in custom_partial_dict.keys() and user_service.lower() == "oc12_commercial"):
                raise exceptions.CommercialCanNotUpdateClientCommercialContactException()

            client_id = custom_partial_dict["client_id"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_clients_view().update_client(user_collaborator_id, user_service, custom_partial_dict)
            else:
                self.update_app_view.get_clients_view().update_client_filtered(self, user_query_filters_args)
            message = f"Update client {client_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(client={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CommercialCollaboratorIsNotAssignedToClient:
            raise exceptions.CommercialCollaboratorIsNotAssignedToClient()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.CommercialCanNotUpdateClientCommercialContactException:
            message = self.app_dict.get_appli_dictionnary()["COMMERCIAL_COLLABORATOR_CAN_NOT_UPDATE_CLIENT_COMMERCIAL_CONTACT"]
            printer.print_message("error",message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(user={ 'registration_number': r_number }):
                    LOGGER.error(message)
            sys.exit(0)
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_collaborator(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator_id = ""
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            matricule = custom_partial_dict["registration_number"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_collaborators_view().update_collaborator(custom_partial_dict)
            else:
                self.update_app_view.get_collaborators_view().update_collaborator_filtered(self, user_query_filters_args)

            message = f"Update collaborator {matricule} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(collaborator={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message

        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_collaborator_password(self, old_password="", new_password=""):
        """
        Description:
        Dédiée à mettre à jour le mot de passe d'un collaborateur de l'entreprise.
        """
        if old_password == "" and new_password == "":
            (
                old_password,
                new_password,
            ) = forms.submit_a_collaborator_new_password_get_form()
        decoded_token = self.jwt_view.get_decoded_token()
        user_registration_number = str(decoded_token["registration_number"])
        if old_password == "" or new_password == "":
            printer.print_message(
                "error", self.app_dict.get_appli_dictionnary()["MISSING_PASSWORD"]
            )
            raise exceptions.MissingUpdateParamException()
        try:
            if not bool(
                self.update_app_view.get_collaborators_view().old_collaborator_password_is_valid(
                    user_registration_number, old_password
                )
            ):
                raise exceptions.OldPasswordNotValidException
            self.update_app_view.get_collaborators_view().new_collaborator_password_is_valid(
                new_password
            )

        except exceptions.OldPasswordNotValidException:
            message = self.app_dict.get_appli_dictionnary()["OLD_PASSWORD_NOT_MATCH"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except exceptions.NewPasswordDoesRespectMinSpecialCharsException:
            message = self.app_dict.get_appli_dictionnary()["NEW_PASSWORD_NOT_MATCH_SPECIAL_CHARS"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except exceptions.NewPasswordDoesRespectForbiddenSpecialCharsException:
            message = self.app_dict.get_appli_dictionnary()["NEW_PASSWORD_NOT_MATCH_FORBIDEN_CHARS"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        return (
            self.update_app_view.get_collaborators_view().update_collaborator_password(
                user_registration_number, old_password, new_password
            )
        )

    @utils.authentication_permission_decorator
    def update_company(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company_id = ""
        try:
            if "company" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            company_id = custom_partial_dict["company_id"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_companies_view().update_company(custom_partial_dict)
            else:
                self.update_app_view.get_companies_view().update_company_filtered(self, user_query_filters_args)
            message = f"Update company {company_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(company={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_contract(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract_id = ""
        user_collaborator_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, r_number)}"
        try:
            if "contract" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            contract_id = custom_partial_dict["contract_id"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_contracts_view().update_contract(
                    user_collaborator_id, user_service, custom_partial_dict
                )
            else:
                self.update_app_view.get_contracts_view().update_contract_filtered(self, user_query_filters_args)
            message = f"Update contract {contract_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(contract={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CommercialCollaboratorIsNotAssignedToContract:
            raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_department(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un département /service de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department_id = ""
        try:
            if "collaborator_department" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            department_id = custom_partial_dict["department_id"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_departments_view().update_department(custom_partial_dict)
            else:
                self.update_app_view.get_departments_view().update_department_filtered(self, user_query_filters_args)
            message = f"Update department {department_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(department={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_event(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"]).lower()
        username = str(decoded_token["username"]).lower()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event_id = ""
        user_collaborator_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, r_number)}"
        try:
            # un membre du service commercial n'a accès qu'en lecture seule
            if (
                "event" not in allowed_crud_tables or user_service.lower() == "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()

            event_id = custom_partial_dict["event_id"]
            if len(user_query_filters_args) == 0:
                if "collaborator_id" in custom_partial_dict:
                    if custom_partial_dict["collaborator_id"] != None:
                        # un membre du service Gestion doit seulement pouvoir assigner un membre du service Support.
                        # Ainsi il ne doit pas être possible d'assigner un membre du service commercial etc.
                        assigned_user_department_id = utils.get_department_name_from_collaborator_id(
                            self.app_view.session,
                            custom_partial_dict["collaborator_id"]
                        )
                        department_name = utils.get_department_name_from_id(
                            self.app_view.session,
                            assigned_user_department_id
                        )
                        if department_name != "oc12_support":
                            raise exceptions.OnlySuportMemberCanBeAssignedToEventSupportException()
                self.update_app_view.get_events_view().update_event(
                    user_collaborator_id, user_service, custom_partial_dict
                )
            else:
                self.update_app_view.get_events_view().update_event_filtered(self, user_query_filters_args)
            message = f"Update event {event_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(event={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.OnlySuportMemberCanBeAssignedToEventSupportException:
            raise exceptions.OnlySuportMemberCanBeAssignedToEventSupportException()
        except exceptions.SupportCollaboratorIsNotAssignedToEvent:
            printer.print_message(
                "error",
                self.app_dict.get_appli_dictionnary()[
                    "SUPPORT_COLLABORATOR_IS_NOT_ASSIGNED_TO_EVENT"
                ],
            )
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
            sys.exit(0)
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_location(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location_id = ""
        try:
            if "location" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            if len(user_query_filters_args) == 0:
                return self.update_app_view.get_locations_view().update_location(
                    custom_partial_dict
                )
            else:
                return self.update_app_view.get_locations_view().update_location_filtered(self, user_query_filters_args)
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)

    @utils.authentication_permission_decorator
    def update_role(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        r_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role_id = ""
        try:
            if "collaborator_role" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            role_id = custom_partial_dict["role_id"]
            if len(user_query_filters_args) == 0:
                self.update_app_view.get_roles_view().update_role(
                    custom_partial_dict
                )
            else:
                self.update_app_view.get_roles_view().update_role_filtered(self, user_query_filters_args)
            message = f"Update role {role_id} by {r_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(role={'custom_partial_dict': custom_partial_dict }):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            	LOGGER.error(message)
            sys.exit(0)
