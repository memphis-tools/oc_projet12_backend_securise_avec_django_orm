"""
Description: Client en mode console, dédié aux mises à jour (ajout, modification, suppression).
"""
import sys
from datetime import datetime
from rich import print

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.models import models
    from src.views.create_views import CreateAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils import utils
    from src.validators import add_data_validators
    from src.validators.data_syntax.fr import validators
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from models import models
    from views.create_views import CreateAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils import utils
    from validators import add_data_validators
    from validators.data_syntax.fr import validators


class ConsoleClientForCreate:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la création /ajout de données.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        utils.display_banner()
        self.app_view = AppViews(db_name)
        self.create_app_view = CreateAppViews(db_name)
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    def ask_for_a_client_id(self):
        client_id = forms.submit_a_client_get_form()
        if client_id == "":
            print("Pas d'id client saisi")
            return False
        client_lookup = None
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(client_id)
            return client_lookup.id
        except Exception as error:
            print("Pas de client avec cet id.")
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
            return contract_lookup.id
        except Exception as error:
            print("Pas de contrat avec cet id.")
            return False

    def ask_for_a_company_id(self):
        company_id = forms.submit_a_company_get_form()
        if company_id == "":
            print("Pas d'id entreprise saisi")
            return False
        company_lookup = None
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(company_id)
            return company_lookup.id
        except Exception as error:
            print("Pas d'entreprise avec cet id.")
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
            return department_lookup.id
        except Exception as error:
            print("Pas de service /département avec cet id.")
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
            return event_lookup.id
        except Exception as error:
            print("Pas d'évènement avec cet id.")
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
            return location_lookup.id
        except Exception as error:
            print("Pas de localité avec cet id.")
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
            return role_lookup.id
        except Exception:
            print("Pas de role avec cet id.")
            return False

    @utils.authentication_permission_decorator
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
        registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, registration_number
        )
        try:
            if (
                "client" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if client_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(client_attributes_dict)
                b2 = add_data_validators.add_client_data_is_valid(
                    client_attributes_dict
                )
                if b1 and b2:
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
                client_id = self.create_app_view.get_clients_view().add_client(
                    models.Client(**client_attributes_dict)
                )
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
        return client_id

    @utils.authentication_permission_decorator
    def add_collaborator(self, collaborator_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator = ""
        try:
            if (
                "collaborator" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(collaborator_attributes_dict)
                b2 = add_data_validators.add_collaborator_data_is_valid(
                    collaborator_attributes_dict
                )
                if b1 and b2:
                    collaborator = models.Collaborator(**collaborator_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                collaborator_attributes_dict = forms.submit_a_collaborator_create_form()
                collaborator = models.Collaborator(**collaborator_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        return self.create_app_view.get_collaborators_view().add_collaborator(
            collaborator
        )

    @utils.authentication_permission_decorator
    def add_company(self, company_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        company = ""
        try:
            if (
                "company" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
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
                company_location_id = self.ask_for_a_location_id()
                if not company_location_id:
                    company_location_id = self.add_location()
                company_attributes_dict = forms.submit_a_company_create_form(
                    company_location_id=company_location_id
                )
                company = models.Company(**company_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        company.creation_date = datetime.now()
        return self.create_app_view.get_companies_view().add_company(company)

    @utils.authentication_permission_decorator
    def add_contract(self, contract_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un contrat pour l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        contract = ""
        try:
            if (
                "contract" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
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
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        contract.creation_date = datetime.now()
        return self.create_app_view.get_contracts_view().add_contract(contract)

    @utils.authentication_permission_decorator
    def add_department(self, department_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouveau départements /services de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        department = ""
        try:
            if (
                "collaborator_department" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if department_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(department_attributes_dict)
                b2 = add_data_validators.add_department_data_is_valid(
                    department_attributes_dict
                )
                if b1 and b2:
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
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        department.creation_date = datetime.now()
        return self.create_app_view.get_departments_view().add_department(department)

    @utils.authentication_permission_decorator
    def add_event(self, event_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un évènement de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        registration_number = str(decoded_token["registration_number"])
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        event = ""
        user_id = utils.get_user_id_from_registration_number(
            self.app_view.session, registration_number
        )
        try:
            if (
                "event" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if event_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(event_attributes_dict)
                b2 = add_data_validators.add_event_data_is_valid(event_attributes_dict)
                if b1 and b2:
                    event = models.Event(**event_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                contract_id_asked = self.ask_for_a_contract_id()
                contract_id = utils.get_contract_id_from_contract_custom_id(
                    self.app_view.session, contract_id_asked
                )
                if not contract_id:
                    raise exceptions.ContractNotFoundWithContractId()
                event_attributes_dict = forms.submit_a_event_create_form()
                event_attributes_dict["collaborator_id"] = user_id
                event_attributes_dict["contract_id"] = contract_id
                event = models.Event(**event_attributes_dict)
            event.creation_date = datetime.now()
            return self.create_app_view.get_events_view().add_event(user_id, event)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.ContractNotFoundWithContractId:
            print(
                "[bold red]Erreur[/bold red] Contrat non trouvé avec le contract_id fourni."
            )
            raise exceptions.ContractNotFoundWithContractId()
            sys.exit(0)
        except exceptions.SupportCollaboratorIsNotAssignedToEvent:
            print(
                "[bold red]Erreur[/bold red] Vous n'avez pas signé le contrat dédié à l'évènement"
            )
            raise exceptions.SupportCollaboratorIsNotAssignedToEvent()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)

    @utils.authentication_permission_decorator
    def add_location(self, location_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer une localité.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        location = ""
        try:
            if (
                "location" not in allowed_crud_tables or user_service.lower() != "oc12_commercial"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if location_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(location_attributes_dict)
                b2 = add_data_validators.add_location_data_is_valid(
                    location_attributes_dict
                )
                b3 = validators.is_complement_adresse_valid(
                    location_attributes_dict["complement_adresse"]
                )
                if b1 and b2 and b3:
                    location = models.Location(**location_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                location_id = self.ask_for_a_location_id()
                if location_id:
                    raise exceptions.LocationCustomIdAlReadyExists()
                location_attributes_dict = forms.submit_a_location_create_form(
                    location_id
                )
                location = models.Location(**location_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.LocationCustomIdAlReadyExists:
            print("[bold red]Erreur.[/bold red] Id existe déjà")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except exceptions.SuppliedDataNotMatchModel:
            print(
                "[bold red]Erreur.[/bold red] Vos données ne respecte pas le format attendu."
            )
            raise exceptions.SuppliedDataNotMatchModel()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        location.creation_date = datetime.now()
        return self.create_app_view.get_locations_view().add_location(location)

    @utils.authentication_permission_decorator
    def add_role(self, role_attributes_dict=""):
        """
        Description: vue dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        role = ""
        try:
            if (
                "collaborator_role" not in allowed_crud_tables or user_service.lower() != "oc12_gestion"
            ):
                raise exceptions.InsufficientPrivilegeException()
            if role_attributes_dict != "":
                b1 = add_data_validators.data_is_dict(role_attributes_dict)
                b2 = add_data_validators.add_role_data_is_valid(role_attributes_dict)
                if b1 and b2:
                    role = models.Collaborator_Role(**role_attributes_dict)
                else:
                    raise exceptions.SuppliedDataNotMatchModel()
            else:
                role_attributes_dict = forms.submit_a_collaborator_role_create_form()
                role = models.Collaborator_Role(**role_attributes_dict)
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]Erreur[/bold red] Vous n'êtes pas autorisé.")
            raise exceptions.InsufficientPrivilegeException()
            sys.exit(0)
        except Exception as error:
            print(f"[bold red]Erreur application[/bold red] {error}")
            sys.exit(0)
        role.creation_date = datetime.now()
        return self.create_app_view.get_roles_view().add_role(role)
