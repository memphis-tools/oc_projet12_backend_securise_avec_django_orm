"""
Description: Client en mode console, dédié aux mises à jour (ajout, modification, suppression).
"""
import sys
from rich import print

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.create_views import CreateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
    from src.validators import add_data_validators
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from models import models
    from views.create_views import CreateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner
    from validators import add_data_validators


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
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    def ask_for_a_client_id(self):
        client_id = forms.submit_a_client_get_form()
        if client_id == "":
            print("Pas d'id client saisi, recherche d'une entreprise")
            return False
        client_lookup = None
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(client_id)
            return client_lookup.get_dict()
        except Exception as error:
            print(f"No such client sir: {error}")
            return False

    def ask_for_a_contract_id(self):
        contract_id = forms.submit_a_contract_get_form()
        if contract_id == "":
            print("Pas d'id contrat saisi")
            return False
        contract_lookup = None
        try:
            # on propose de rechercher le contrat
            contract_lookup = self.app_view.get_contracts_view().get_contract(
                contract_id
            )
            return contract_lookup.get_dict()
        except Exception as error:
            print(f"No such contract sir: {error}")
            return False

    def ask_for_a_company_id(self):
        company_id = forms.submit_a_company_get_form()
        if company_id == "":
            print("Pas d'id entreprise saisi, recherche d'une localité")
            return False
        company_lookup = None
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(company_id)
            return company_lookup.get_dict()
        except Exception as error:
            print(f"No such company sir: {error}")
            return False

    def ask_for_a_department_id(self):
        department_id = forms.submit_a_collaborator_department_get_form()
        if department_id == "":
            print("Pas d'id département /service saisi")
            return False
        department_lookup = None
        try:
            # on propose de rechercher led département /service
            department_lookup = self.app_view.get_departments_view().get_department(
                department_id
            )
            return department_lookup.get_dict()
        except Exception as error:
            print(f"No such department sir: {error}")
            return False

    def ask_for_a_event_id(self):
        event_id = forms.submit_a_event_get_form()
        if event_id == "":
            print("Pas d'id évènement saisi")
            return False
        event_lookup = None
        try:
            # on propose de rechercher l'évènement
            event_lookup = self.app_view.get_events_view().get_event(event_id)
            return event_lookup.get_dict()
        except Exception as error:
            print(f"No such event sir: {error}")
            return False

    def ask_for_a_location_id(self):
        location_id = forms.submit_a_location_get_form()
        if location_id == "":
            print("Pas d'id localité saisi")
            return False
        location_lookup = None
        try:
            # on propose de rechercher la localité
            location_lookup = self.app_view.get_locations_view().get_location(
                location_id
            )
            return location_lookup.get_dict()
        except Exception as error:
            print(f"No such location sir: {error}")
            return False

    def ask_for_a_role_id(self):
        role_id = forms.submit_a_collaborator_role_get_form()
        if role_id == "":
            print("Pas d'id role saisi")
            return False
        role_lookup = None
        try:
            # on propose de rechercher le role
            role_lookup = self.app_view.get_roles_view().get_role(role_id)
            return role_lookup.get_dict()
        except Exception as error:
            print(f"No such role sir: {error}")
            return False

    @authentication_permission_decorator
    def add_client(self, client_attributes_dict=""):
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
        user_registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        try:
            if "client" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if client_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(client_attributes_dict)
                b2 = add_data_validators.add_client_data_is_valid(
                    client_attributes_dict
                )
                if b1 and b2:
                    # client = models.Client(**client_attributes_dict)
                    client_id = self.create_app_view.get_clients_view().add_client(
                        models.Client(**client_attributes_dict)
                    )
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                client_queryset = self.ask_for_a_client_id()
                if not client_queryset:
                    # pas de client trouvé, on commence par demander l'entreprise à enregistrer.
                    company_queryset = self.ask_for_a_company_id()
                    if not company_queryset:
                        # pas d'entreprise trouvée, on commence par demander la localité à enregistrer.
                        location_queryset = self.ask_for_a_location_id()
                        if not location_queryset:
                            # pas de localité trouvée,
                            # on entame le dialogue pour enregistrer localité, entreprise, et client.
                            location_attributes_dict = (
                                forms.submit_a_location_create_form()
                            )
                            company_attributes_dict = (
                                forms.submit_a_company_create_form()
                            )
                            client_attributes_dict = forms.submit_a_client_create_form()

                            loc_id = (
                                self.create_app_view.get_locations_view().add_location(
                                    models.Location(**location_attributes_dict)
                                )
                            )
                            company_attributes_dict["location_id"] = loc_id
                            comp_id = (
                                self.create_app_view.get_companies_view().add_company(
                                    models.Company(**company_attributes_dict)
                                )
                            )
                            client_attributes_dict["company_id"] = comp_id
                            client_id = (
                                self.create_app_view.get_clients_view().add_client(
                                    models.Client(**client_attributes_dict)
                                )
                            )
                        else:
                            loc_id = location_queryset["id"]
                            company_attributes_dict = (
                                forms.submit_a_company_create_form()
                            )
                            client_attributes_dict = forms.submit_a_client_create_form()
                            company_attributes_dict["location_id"] = loc_id
                            comp_id = (
                                self.create_app_view.get_companies_view().add_company(
                                    models.Company(**company_attributes_dict)
                                )
                            )
                            client_attributes_dict["company_id"] = id
                            client_id = (
                                self.create_app_view.get_clients_view().add_client(
                                    models.Client(**client_attributes_dict)
                                )
                            )
                    else:
                        company_id = company_queryset["id"]
                        client_attributes_dict = forms.submit_a_client_create_form()
                        client_attributes_dict["company_id"] = company_id
                        client_id = self.create_app_view.get_clients_view().add_client(
                            models.Client(**client_attributes_dict)
                        )
                else:
                    print(f"[INFO] all good client found: {client_queryset}")

        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
        return client_id

    @authentication_permission_decorator
    def add_collaborator(self, collaborator_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator = ""
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(collaborator_attributes_dict)
                b2 = add_data_validators.add_collaborator_data_is_valid(
                    collaborator_attributes_dict
                )
                if b1 and b2:
                    collaborator = models.User(**collaborator_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                collaborator_attributes_dict = forms.submit_a_collaborator_create_form()
                collaborator = models.User(**collaborator_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_collaborators_view().add_collaborator(
            collaborator
        )

    @authentication_permission_decorator
    def add_company(self, company_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company = ""
        try:
            if "company" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if company_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(company_attributes_dict)
                b2 = add_data_validators.add_company_data_is_valid(
                    company_attributes_dict
                )
                if b1 and b2:
                    company = models.Company(**company_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                company_attributes_dict = forms.submit_a_company_create_form()
                company = models.Company(**company_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_companies_view().add_company(company)

    @authentication_permission_decorator
    def add_contract(self, contract_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract = ""
        try:
            if "contract" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if contract_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(contract_attributes_dict)
                b2 = add_data_validators.add_contract_data_is_valid(
                    contract_attributes_dict
                )
                if b1 and b2:
                    contract = models.Contract(**contract_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                contract_attributes_dict = forms.submit_a_contract_create_form()
                contract = models.Contract(**contract_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_contracts_view().add_contract(contract)

    @authentication_permission_decorator
    def add_department(self, department_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department = ""
        try:
            if "collaborator_department" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if department_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(department_attributes_dict)
                b2 = add_data_validators.add_department_data_is_valid(
                    department_attributes_dict
                )
                if b1 and b2:
                    department = models.UserDepartment(**department_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                department_attributes_dict = (
                    forms.submit_a_collaborator_department_create_form()
                )
                department = models.UserDepartment(**department_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_departments_view().add_department(department)

    @authentication_permission_decorator
    def add_event(self, event_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event = ""
        try:
            if "event" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if event_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(event_attributes_dict)
                b2 = add_data_validators.add_event_data_is_valid(event_attributes_dict)
                if b1 and b2:
                    event = models.Event(**event_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                event_attributes_dict = forms.submit_a_event_create_form()
                event = models.Event(**event_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_events_view().add_event(event)

    @authentication_permission_decorator
    def add_location(self, location_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location = ""
        try:
            if "location" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if location_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(location_attributes_dict)
                b2 = add_data_validators.add_location_data_is_valid(
                    location_attributes_dict
                )
                if b1 and b2:
                    location = models.Location(**location_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                location_attributes_dict = forms.submit_a_location_create_form()
                location = models.Location(**location_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_locations_view().add_location(location)

    @authentication_permission_decorator
    def add_role(self, role_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role = ""
        try:
            if "collaborator_role" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if role_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(role_attributes_dict)
                b2 = add_data_validators.add_role_data_is_valid(role_attributes_dict)
                if b1 and b2:
                    role = models.UserRole(**role_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                role_attributes_dict = forms.submit_a_collaborator_role_create_form()
                role = models.UserRole(**role_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.create_app_view.get_roles_view().add_role(role)
