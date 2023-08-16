"""
Description: Client en mode console, dédié aux mises à jour.
"""
import sys
from rich import print

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.views.update_views import UpdateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
    from src.utils import utils
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from views.update_views import UpdateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner
    from utils import utils


class ConsoleClientForUpdate:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la mise à jour de données.
    """

    def __init__(self, custom_id="", db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews(db_name)
        self.update_app_view = UpdateAppViews(db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    @authentication_permission_decorator
    def update_client(self, custom_partial_dict, db_name=f"{settings.DATABASE_NAME}"):
        # rechercher le id de l'utilisateur courant
        # obtenir le token décodé (et valide)
        # demander mot de passe à utilisateur en cours
        # controler le mot de passe
        """
        Description: vue dédiée à mettre à jour un client de l'entreprise.
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
            return self.update_app_view.get_clients_view().update_client(
                user_collaborator_id, user_service, custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.CommercialCollaboratorIsNotAssignedToClient:
            print(
                "[bold red]Erreur[/bold red] Vous n'êtes pas le commercial du client; mise à jour non autorisée."
            )
            raise exceptions.CommercialCollaboratorIsNotAssignedToClient()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_collaborator(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator_id = ""
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_collaborators_view().update_collaborator(
                custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
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
            print("[bold red]Mot(s) de passe non saisi(s).[/bold red]")
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
            print("[bold red]Mot de passe erroné.[/bold red]")
            sys.exit(0)
        except exceptions.NewPasswordDoesRespectMinSpecialCharsException:
            print(
                "[bold red]Erreur[/bold red] Mot de passe ne respecte pas le nombre min de caractères spéciaux."
            )
            sys.exit(0)
        except exceptions.NewPasswordDoesRespectForbiddenSpecialCharsException:
            print(
                "[bold red]Nouveau mot de passe possède des caractères spéciaux interdits.[/bold red]"
            )
            sys.exit(0)
        return (
            self.update_app_view.get_collaborators_view().update_collaborator_password(
                user_registration_number, old_password, new_password
            )
        )

    @authentication_permission_decorator
    def update_company(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company_id = ""
        try:
            if "company" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_companies_view().update_company(
                custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_contract(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        r_number = str(decoded_token["registration_number"])
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract_id = ""
        user_collaborator_id = f"{utils.get_user_id_from_registration_number(self.app_view.session, r_number)}"
        try:
            if "contract" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_contracts_view().update_contract(
                user_collaborator_id, user_service, custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.CommercialCollaboratorIsNotAssignedToContract:
            print(
                "[bold red]Erreur[/bold red] Vous n'êtes pas le commercial du contrat; mise à jour non autorisée."
            )
            raise exceptions.CommercialCollaboratorIsNotAssignedToContract()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_department(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un département /service de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department_id = ""
        try:
            if "collaborator_department" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_departments_view().update_department(
                custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_event(self, custom_partial_dict=""):
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
            # dans le cas où d'un collaborateur du serivce gestion, il modifie seulement s'il est assigné.
            return self.update_app_view.get_events_view().update_event(
                user_collaborator_id, user_service, custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SupportCollaboratorIsNotAssignedToEvent:
            print(
                "[bold red]Erreur[/bold red] Vous n'êtes pas le collaborateur support associé à l'évènement."
            )
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_location(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location_id = ""
        try:
            if "location" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_locations_view().update_location(
                custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @authentication_permission_decorator
    def update_role(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role_id = ""
        try:
            if "collaborator_role" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            return self.update_app_view.get_roles_view().update_role(
                custom_partial_dict
            )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
