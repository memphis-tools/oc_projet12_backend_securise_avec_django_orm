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
    from src.views.crud_views.update_views import UpdateAppViews
    from src.views.crud_views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings, logtail_handler
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from forms import forms
    from views.crud_views.update_views import UpdateAppViews
    from views.crud_views.views import AppViews
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
        self.app_view = AppViews(db_name=db_name)
        self.update_app_view = UpdateAppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE
        self.decoded_token = self.jwt_view.get_decoded_token()
        self.user_service = str(self.decoded_token["department"]).upper()
        self.registration_number = str(self.decoded_token["registration_number"])
        self.allowed_crud_tables = eval(f"settings.{self.user_service}_CRUD_TABLES")
        utils.display_banner(registration_number=self.registration_number)

    @utils.authentication_permission_decorator
    def update_client(
        self,
        custom_partial_dict,
        db_name=f"{settings.DATABASE_NAME}",
        user_query_filters_args="",
    ):
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
        current_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, self.registration_number)}"
        try:
            client_grant_valid = bool("client" not in self.allowed_crud_tables)
            if client_grant_valid or self.user_service.lower() != "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()

            keys_valid = bool("commercial_contact" in custom_partial_dict.keys())
            if keys_valid and self.user_service.lower() == "oc12_commercial":
                raise exceptions.CommercialCanNotUpdateClientCommercialContactException()

            client_id = self.update_app_view.get_clients_view().update_client(
                current_id, self.user_service, custom_partial_dict
            )
            message = f"Update client {client_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    client={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
            return message
        except exceptions.InsufficientPrivilegeException:
            raise exceptions.InsufficientPrivilegeException()
        except exceptions.CommercialCollaboratorIsNotAssignedToClient:
            raise exceptions.CommercialCollaboratorIsNotAssignedToClient()
        except exceptions.CustomIdMatchNothingException:
            raise exceptions.CustomIdMatchNothingException()
        except exceptions.CommercialCanNotUpdateClientCommercialContactException:
            message = self.app_dict.get_appli_dictionnary()[
                "COMMERCIAL_COLLABORATOR_CAN_NOT_UPDATE_CLIENT_COMMERCIAL_CONTACT"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    user={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
                    LOGGER.info(message)
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.InsufficientPrivilegeException()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_collaborator(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un utilisateur /collaborateur de l'entreprise.
        """
        collaborator_id = ""
        try:
            if "collaborator" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            matricule = self.update_app_view.get_collaborators_view().update_collaborator(
                custom_partial_dict
            )
            message = f"Update collaborator {matricule} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    collaborator={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

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
        user_registration_number = str(self.decoded_token["registration_number"])
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
        except exceptions.NewPasswordDoesRespectMinSpecialCharsException:
            message = self.app_dict.get_appli_dictionnary()[
                "NEW_PASSWORD_NOT_MATCH_SPECIAL_CHARS"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except exceptions.NewPasswordDoesRespectForbiddenSpecialCharsException:
            message = self.app_dict.get_appli_dictionnary()[
                "NEW_PASSWORD_NOT_MATCH_FORBIDEN_CHARS"
            ]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
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
        company_id = ""
        try:
            if "company" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            company_id = self.update_app_view.get_companies_view().update_company(
                custom_partial_dict
            )
            message = f"Update company {company_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    company={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_contract(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un contrat pour l'entreprise.
        """
        contract_id = ""
        user_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, self.registration_number)}"
        try:
            if "contract" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            contract_id = self.update_app_view.get_contracts_view().update_contract(
                self.app_view, user_id, self.user_service, custom_partial_dict
            )

            if "status" in custom_partial_dict.keys():
                message = f"Update contract {contract_id} for signature by {self.registration_number}"
            else:
                message = f"Update contract {contract_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    contract={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except exceptions.EventAttachedContractStatusCanNotBeUpdateException as event_title:
            message = self.app_dict.get_appli_dictionnary()["CONTRACT_STATUS_EVENT_HAS_TO_BE_DELETE"]
            printer.print_message("error", f"{message} {event_title}")
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
            raise exceptions.EventAttachedContractStatusCanNotBeUpdateException()
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_department(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un département /service de l'entreprise.
        """
        department_id = ""
        try:
            if "collaborator_department" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            department_id = self.update_app_view.get_departments_view().update_department(
                custom_partial_dict
            )
            message = f"Update department {department_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    department={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_event(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un évènement de l'entreprise.
        """
        user_service = str(self.decoded_token["department"]).upper()
        event_id = ""
        user_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, self.registration_number)}"
        try:
            # un membre du service commercial n'a accès qu'en lecture seule
            event_grant_valid = bool("event" not in self.allowed_crud_tables)
            if event_grant_valid or self.user_service.lower() == "oc12_commercial":
                raise exceptions.InsufficientPrivilegeException()

            if "collaborator_id" in custom_partial_dict:
                if custom_partial_dict["collaborator_id"] is not None:
                    # un membre du service Gestion doit seulement pouvoir assigner un membre du service Support.
                    # Ainsi il ne doit pas être possible d'assigner un membre du service commercial etc.
                    assigned_user_department_id = (
                        utils.get_department_name_from_collaborator_id(
                            self.app_view.session,
                            custom_partial_dict["collaborator_id"],
                        )
                    )
                    department_name = utils.get_department_name_from_id(
                        self.app_view.session, assigned_user_department_id
                    )
                    if department_name != "oc12_support":
                        raise exceptions.OnlySuportMemberCanBeAssignedToEventSupportException()
            event_id = self.update_app_view.get_events_view().update_event(
                user_id, self.user_service, custom_partial_dict
            )

            message = f"Update event {event_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    event={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except TypeError:
            message = self.app_dict.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_location(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour une localité.
        """
        location_id = ""
        try:
            if "location" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            location_id = self.update_app_view.get_locations_view().update_location(
                custom_partial_dict
            )
            message = f"Update location {location_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    client={
                        "location_id": location_id,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def update_role(self, custom_partial_dict="", user_query_filters_args=""):
        """
        Description: vue dédiée à mettre à jour un rôle pour les collaborateurs de l'entreprise.
        """
        role_id = ""
        try:
            if "collaborator_role" not in self.allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()

            role_id = self.update_app_view.get_roles_view().update_role(custom_partial_dict)
            message = f"Update role {role_id} by {self.registration_number}"
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                with logtail.context(
                    role={
                        "custom_partial_dict": custom_partial_dict,
                        "current_collaborator": self.registration_number,
                    }
                ):
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
        except Exception:
            message = self.app_dict.get_appli_dictionnary()["APPLICATION_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
