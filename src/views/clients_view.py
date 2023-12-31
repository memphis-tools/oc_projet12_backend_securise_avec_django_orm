"""
vue clients
"""
from rich.console import Console

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.exceptions import exceptions
    from src.utils import utils
    from src.settings import logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from exceptions import exceptions
    from utils import utils
    from settings import logtail_handler


LOGGER = logtail_handler.logger


class ClientsView:
    """
    Description: une classe dédiée à servir les vues pour les clients de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.session = session

    def get_clients(self, user_query_filters_args=""):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Client"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "clients", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info", self.app_dict.get_appli_dictionnary()["NO_MORE_CLIENT"]
                    )
                else:
                    raise exceptions.CustomIdMatchNothingException()
            except exceptions.QueryStructureException:
                raise exceptions.QueryStructureException()
            except TypeError:
                raise exceptions.CustomIdMatchNothingException()
            except Exception:
                raise exceptions.QueryFailureException()
        else:
            db_model_queryset = self.db_controller.get_clients(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data("clients", db_model_queryset)
                console.print(table)
                printer.print_message(
                    "info", self.app_dict.get_appli_dictionnary()["NO_MORE_CLIENT"]
                )
            else:
                raise exceptions.CustomIdMatchNothingException()
        return self.db_controller.get_clients(self.session)

    def get_client(self, client_id):
        """
        Description: vue dédiée à obtenir un client de l'entreprise.
        """
        return self.db_controller.get_client(self.session, client_id)

    def add_client(self, client):
        """
        Description: vue dédiée à enregistrer un client.
        Parameters:
        - client: une instance valide de la classe Client.
        """
        return self.db_controller.add_client(self.session, client)

    def delete_client(self, client_id):
        """
        Description: vue dédiée à supprimer un client de l'entreprise.
        Parameters:
        - client_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_client(self.session, client_id)

    def update_client(self, current_user_collaborator_id, user_service, custom_dict):
        """
        Description: vue dédiée à mettre à jour un client.
         Parameters:
         - current_user_collaborator_id: l'id (la clef primaire, 'pas un custom id')
         - user_service: chaine de caractère, le nom du service de l'utilisateur courant (exemple: oc12_commercial)
         - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        if "commercial_contact" in custom_dict.keys():
            if custom_dict["commercial_contact"] != None:
                collaborator_id = utils.get_user_id_from_registration_number(self.session, custom_dict["commercial_contact"])
                custom_dict["commercial_contact"] = collaborator_id
        return self.db_controller.update_client(
            self.session, current_user_collaborator_id, user_service, custom_dict
        )
