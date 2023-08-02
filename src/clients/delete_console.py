"""
Description: Client en mode console, dédié aux mises à jour pour suppression.
"""
import sys
from rich import print

try:
    from src.exceptions import exceptions
    from src.forms import forms
    from src.views.delete_views import DeleteAppViews
    from src.views.views import AppViews
    from src.views.jwt_view import JwtView
    from src.settings import settings
    from src.utils.utils import authentication_permission_decorator, display_banner
except ModuleNotFoundError:
    from exceptions import exceptions
    from forms import forms
    from views.delete_views import DeleteAppViews
    from views.views import AppViews
    from views.jwt_view import JwtView
    from settings import settings
    from utils.utils import authentication_permission_decorator, display_banner


class ConsoleClientForDelete:
    """
    Description: la classe dédiée à l'usage d'un client en mode console, pour la création /ajout de données.
    """

    def __init__(self, custom_id=""):
        """
        Description: on instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        display_banner()
        self.app_view = AppViews()
        self.delete_app_view = DeleteAppViews()
        self.jwt_view = JwtView(self.app_view)
        # le module est appelé dynamiquement et n'est pas vu par flake8.
        # déclaration faite pour éviter une erreur dans le rapport flake8.
        settings.APP_FIGLET_TITLE

    def ask_for_a_client_id(self, custom_id=""):
        client_id = ""
        if custom_id == "":
            client_id = forms.submit_a_client_get_form()
            if client_id == "":
                print("Pas d'id client saisi")
                return False
            client_lookup = None
        else:
            client_id = custom_id
        try:
            # on propose de rechercher le client
            client_lookup = self.app_view.get_clients_view().get_client(client_id)
            return client_lookup.get_dict()
        except Exception as error:
            print(f"No such client sir: {error}")
            return False

    def ask_for_a_contract_id(self, custom_id=""):
        if custom_id == "":
            contract_id = forms.submit_a_contract_get_form()
            if contract_id == "":
                print("Pas d'id contrat saisi")
                return False
            contract_lookup = None
        else:
            contract_id = custom_id
        try:
            # on propose de rechercher le contrat
            contract_lookup = self.app_view.get_contracts_view().get_contract(
                contract_id
            )
            return contract_lookup.get_dict()
        except Exception as error:
            print(f"No such contract sir: {error}")
            return False

    def ask_for_a_collaborator_id(self, custom_id=""):
        if custom_id == "":
            collaborator_id = forms.submit_a_collaborator_get_form()
            if collaborator_id == "":
                print("Pas d'id collaborateur saisi")
                return False
            collaborator_lookup = None
        else:
            collaborator_id = custom_id
        try:
            # on propose de rechercher le collaborateur
            collaborator_lookup = (
                self.app_view.get_collaborators_view().get_collaborator(collaborator_id)
            )
            return collaborator_lookup.get_dict()
        except Exception as error:
            print(f"No such collaborator sir: {error}")
            return False

    def ask_for_a_company_id(self, custom_id=""):
        if custom_id == "":
            company_id = forms.submit_a_company_get_form()
            if company_id == "":
                print("Pas d'id entreprise saisi")
                return False
            company_lookup = None
        else:
            company_id = custom_id
        try:
            # on propose de rechercher l'entreprise
            company_lookup = self.app_view.get_companies_view().get_company(company_id)
            return company_lookup.get_dict()
        except Exception as error:
            print(f"No such company sir: {error}")
            return False

    def ask_for_a_department_id(self, custom_id=""):
        if custom_id == "":
            department_id = forms.submit_a_collaborator_department_get_form()
            if department_id == "":
                print("Pas d'id département /service saisi")
                return False
            department_lookup = None
        else:
            department_id = custom_id
        try:
            # on propose de rechercher led département /service
            department_lookup = self.app_view.get_departments_view().get_department(
                department_id
            )
            return department_lookup.get_dict()
        except Exception as error:
            print(f"No such department sir: {error}")
            return False

    def ask_for_a_event_id(self, custom_id=""):
        if custom_id == "":
            event_id = forms.submit_a_event_get_form()
            if event_id == "":
                print("Pas d'id évènement saisi")
                return False
            event_lookup = None
        else:
            event_id = custom_id
        try:
            # on propose de rechercher l'évènement
            event_lookup = self.app_view.get_events_view().get_event(event_id)
            return event_lookup.get_dict()
        except Exception as error:
            print(f"No such event sir: {error}")
            return False

    def ask_for_a_location_id(self, custom_id=""):
        if custom_id == "":
            location_id = forms.submit_a_location_get_form()
            if location_id == "":
                print("Pas d'id localité saisi")
                return False
            location_lookup = None
        else:
            location_id = custom_id
        try:
            # on propose de rechercher la localité
            location_lookup = self.app_view.get_locations_view().get_location(
                location_id
            )
            return location_lookup.get_dict()
        except Exception as error:
            return False

    def ask_for_a_role_id(self, custom_id=""):
        if custom_id == "":
            role_id = forms.submit_a_collaborator_role_get_form()
            if role_id == "":
                print("Pas d'id role saisi")
                return False
            role_lookup = None
        else:
            role_id = custom_id
        try:
            # on propose de rechercher le role
            role_lookup = self.app_view.get_roles_view().get_role(role_id)
            return role_lookup.get_dict()
        except Exception as error:
            print(f"No such role sir: {error}")
            return False

    @authentication_permission_decorator
    def delete_client(self, client_custom_id=""):
        # rechercher le id de l'utilisateur courant
        # obtenir le token décodé (et valide)
        # demander mot de passe à utilisateur en cours
        # controler le mot de passe
        """
        Description: vue dédiée à supprimer un client de l'entreprise.
        """
        client_id = ""
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        user_registration_number = str(decoded_token["registration_number"])
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        try:
            if "client" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if client_custom_id != "":
                client_id = self.ask_for_a_client_id(client_custom_id)["id"]
            else:
                client_id = self.ask_for_a_client_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_clients_view().delete_client(client_id)

    @authentication_permission_decorator
    def delete_collaborator(self, collaborator_custom_id=""):
        """
        Description: vue dédiée à enregistrer un nouvel utilisateur /collaborateur de l'entreprise.
        """
        decoded_token = self.jwt_view.get_decoded_token()
        user_service = str(decoded_token["department"]).upper()
        allowed_crud_tables = eval(f"settings.{user_service}_CRUD_TABLES")
        collaborator_id = ""
        try:
            if "collaborator" not in allowed_crud_tables:
                raise exceptions.InsufficientPrivilegeException()
            if collaborator_custom_id != "":
                collaborator_id = self.ask_for_a_collaborator_id(
                    collaborator_custom_id
                )["id"]
            else:
                collaborator_id = self.ask_for_a_collaborator_id()["id"]
        except exceptions.InsufficientPrivilegeException:
            print("[bold red]You are not authorized.[/bold red]")
            sys.exit(0)
        except TypeError as error:
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_collaborators_view().delete_collaborator(
            collaborator_id
        )

    @authentication_permission_decorator
    def delete_company(self, company_custom_id=""):
        """
        Description: vue dédiée à enregistrer une entreprise sans client, mais avec une localité nécessaire.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_companies_view().delete_company(company_id)

    @authentication_permission_decorator
    def delete_contract(self, contract_custom_id=""):
        """
        Description: vue dédiée à enregistrer un contrat pour l'entreprise.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_contracts_view().delete_contract(contract_id)

    @authentication_permission_decorator
    def delete_department(self, department_custom_id=""):
        """
        Description: vue dédiée à enregistrer un nouveau départements /services de l'entreprise.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_departments_view().delete_department(
            department_id
        )

    @authentication_permission_decorator
    def delete_event(self, event_custom_id=""):
        """
        Description: vue dédiée à enregistrer un évènement de l'entreprise.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_events_view().delete_event(event_id)

    @authentication_permission_decorator
    def delete_location(self, location_custom_id=""):
        """
        Description: vue dédiée à enregistrer une localité.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_locations_view().delete_location(location_id)

    @authentication_permission_decorator
    def delete_role(self, role_custom_id=""):
        """
        Description: vue dédiée à enregistrer un nouveau rôle pour les collaborateurs de l'entreprise.
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
            print("[bold red]Id non trouvé.[/bold red]")
            sys.exit(0)
        except Exception as error:
            print(f"[ERROR SIR]: {error}")
            sys.exit(0)
        return self.delete_app_view.get_roles_view().delete_role(role_id)
