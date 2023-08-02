"""
Description: Client en mode console, dédié aux mises à jour.
"""
import sys
from rich import print

try:
    from src.exceptions import exceptions
    from src.views.update_views import UpdateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
except ModuleNotFoundError:
    from exceptions import exceptions
    from views.update_views import UpdateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner


class ConsoleClientForUpdate:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la mise à jour de données.
    """

    def __init__(self, custom_id=""):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews()
        self.update_app_view = UpdateAppViews()
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    @authentication_permission_decorator
    def update_client(self, custom_partial_dict):
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
        user_registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        try:
            if "client" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_clients_view().update_client(
            custom_partial_dict
        )

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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_collaborators_view().update_collaborator(
            custom_partial_dict
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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_companies_view().update_company(
            custom_partial_dict
        )

    @authentication_permission_decorator
    def update_contract(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract_id = ""
        try:
            if "contract" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_contracts_view().update_contract(
            custom_partial_dict
        )

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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_departments_view().update_department(
            custom_partial_dict
        )

    @authentication_permission_decorator
    def update_event(self, custom_partial_dict=""):
        """
        Description: vue dédiée à mettre à jour un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event_id = ""
        try:
            if "event" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_events_view().update_event(custom_partial_dict)

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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_locations_view().update_location(
            custom_partial_dict
        )

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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_roles_view().update_role(custom_partial_dict)
