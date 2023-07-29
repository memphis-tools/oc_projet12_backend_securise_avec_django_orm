"""
Description: Client en mode console, dédié aux mises à jour (ajout, modification, suppression).
"""
import sys
from functools import wraps
import maskpass
import jwt
import pyfiglet
from rich import print
import pkg_resources

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.create_views import CreateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from models import models
    from views.create_views import CreateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner


class ConsoleClientForCreate:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la création /ajout de données.
    """

    def __init__(self):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews()
        self.create_app_view = CreateAppViews()
        self.jwt_view = JwtView(self.app_view)

    def ask_for_a_client_id(self):
        print("TRY TO SUBMIT CLIENT FORM SIR")
        client_id = forms.submit_a_client_get_form()
        client_lookup = None
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(client_id)
            return client_lookup
        except Exception:
            print("No such client sir")
            return False

    def ask_for_a_company_id(self):
        company_id = forms.submit_a_company_get_form()
        company_lookup = None
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(company_id)
            return company_lookup
        except Exception:
            print("No such company sir")
            return False

    def ask_for_a_location_id(self):
        location_id = forms.submit_a_company_get_form()
        location_lookup = None
        try:
            # on propose de rechercher la localité
            location_lookup = self.app_view.get_locations_view().get_location(location_id)
            return location_lookup
        except Exception:
            print("No such location sir")
            return False

    @authentication_permission_decorator
    def add_client(self):
        # rechercher le id de l'utilisateur courant
            # obtenir le token décodé (et valide)
            # demander mot de passe à utilisateur en cours
            # controler le mot de passe
        """
        Description: vue dédiée à créer un client de l'entreprise.
        """
        client_id = ""
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        try:
            if "client" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            client_queryset = self.ask_for_a_client_id()
            if not client_queryset:
                # pas de client trouvé, on commence par demander l'entreprise à enregistrer.
                company_queryset = self.ask_for_a_company_id()
                if not company_queryset:
                    # pas d'entreprise trouvée, on commence par demander la localité à enregistrer.
                    location_queryset = self.ask_for_a_location_id()
                    if not location_queryset:
                        # pas de localité trouvée, on entame le dialogue pour enregistrer localité, entreprise, et client.
                        location_attributes_dict = forms.submit_a_location_create_form()
                        company_attributes_dict = forms.submit_a_company_create_form()
                        client_attributes_dict = forms.submit_a_client_create_form()

                        location_id = self.create_app_view.get_locations_view().add_location(models.Location(**location_attributes_dict))
                        company_attributes_dict["location_id"] = location_id
                        company_id = self.create_app_view.get_companies_view().add_company(models.Company(**company_attributes_dict))
                        client_attributes_dict["company_id"] = company_id
                        client_id = self.create_app_view.get_clients_view().add_client(models.Client(**client_attributes_dict))
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
        return client_id

    @authentication_permission_decorator
    def add_collaborators(self):
        """
        Description: vue dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator = {}
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            collaborator_attributes_dict = forms.submit_a_collaborator_create_form()
            collaborator = models.User(**collaborator_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.app_view.get_collaborators_view().add_collaborator()

    @authentication_permission_decorator
    def add_company(self):
        """
        Description: vue dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company = {}
        try:
            if "company" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            company_attributes_dict = forms.submit_a_company_create_form()
            company = models.Company(**company_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_companies_view().add_company(company)

    @authentication_permission_decorator
    def add_contract(self):
        """
        Description: vue dédiée à enregistrer un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract = {}
        try:
            if "contract" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            # Do something sir
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.app_view.get_contracts_view().add_contract(contract)

    @authentication_permission_decorator
    def add_department(self):
        """
        Description: vue dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department = {}
        try:
            if "collaborator_department" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            # Do something sir
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.app_view.get_departments_view().add_department(department)

    @authentication_permission_decorator
    def add_event(self):
        """
        Description: vue dédiée à enregistrer un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event = {}
        try:
            if "event" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            # Do something sir
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.app_view.get_events_view().add_event(event)

    @authentication_permission_decorator
    def add_location(self):
        """
        Description: vue dédiée à enregistrer une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location = {}
        try:
            if "location" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            location_attributes_dict = forms.submit_a_location_create_form()
            location = models.Location(**location_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_locations_view().add_location(location)

    @authentication_permission_decorator
    def add_role(self):
        """
        Description: vue dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role = {}
        try:
            if "collaborator_role" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            # Do something sir
        except exceptions.InsufficientPrivilegeException:
            print(f"[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.app_view.get_roles_view().add_role(role)
