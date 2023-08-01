"""
Description: Client en mode console, dédié aux mises à jour.
"""
import sys
from rich import print

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.update_views import UpdateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
    from src.validators import add_data_validators
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from models import models
    from views.update_views import UpdateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner
    from validators import add_data_validators


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
    def update_client(self, client_partial_dict):
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
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_clients_view().update_client(client_partial_dict)

    @authentication_permission_decorator
    def update_collaborator(self, collaborator_custom_id=""):
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
            if collaborator_custom_id != "":
                collaborator_id = self.ask_for_a_collaborator_id(collaborator_custom_id)["id"]
            else:
                collaborator_id =self.ask_for_a_collaborator_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_collaborators_view().update_collaborator(
            collaborator_id
        )

    @authentication_permission_decorator
    def update_company(self, company_custom_id=""):
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
            if company_custom_id != "":
                company_id = self.ask_for_a_company_id(company_custom_id)["id"]
            else:
                company_id = self.ask_for_a_company_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_companies_view().update_company(company_id)

    @authentication_permission_decorator
    def update_contract(self, contract_custom_id=""):
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
            if contract_custom_id != "":
                contract_id = self.ask_for_a_contract_id(contract_custom_id)["id"]
            else:
                contract_id = self.ask_for_a_contract_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_contracts_view().update_contract(contract_id)

    @authentication_permission_decorator
    def update_department(self, department_custom_id=""):
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
            if department_custom_id != "":
                department_id = self.ask_for_a_department_id(department_custom_id)["id"]
            else:
                department_id = self.ask_for_a_department_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_departments_view().update_department(department_id)

    @authentication_permission_decorator
    def update_event(self, event_custom_id=""):
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
            if event_custom_id != "":
                event_id = self.ask_for_a_event_id(event_custom_id)["id"]
            else:
                event_id = self.ask_for_a_event_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_events_view().update_event(event_id)

    @authentication_permission_decorator
    def update_location(self, location_custom_id=""):
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
            if location_custom_id != "":
                location_id = self.ask_for_a_location_id(location_custom_id)["id"]
            else:
                location_id = self.ask_for_a_location_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_locations_view().update_location(location_id)

    @authentication_permission_decorator
    def update_role(self, role_custom_id=""):
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
            if role_custom_id != "":
                role_id = self.ask_for_a_role_id(role_custom_id)["id"]
            else:
                role_id = self.ask_for_a_role_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print(f"[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.update_app_view.get_roles_view().update_role(role_id)
