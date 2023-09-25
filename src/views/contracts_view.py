"""
vue contrats
"""
from rich.console import Console

try:
    from src.exceptions import exceptions
    from src.languages import language_bridge
    from src.printers import printer
    from src.utils import utils
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from exceptions import exceptions
    from languages import language_bridge
    from printers import printer
    from utils import utils
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class ContractsView:
    """
    Description: une classe dédiée à servir les vues pour les contrats de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.session = session

    def get_contracts(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Contract"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "contracts", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info",
                        self.app_dict.get_appli_dictionnary()["NO_MORE_CONTRACT"],
                    )
                else:
                    message = self.app_dict.get_appli_dictionnary()[
                        "DATABASE_QUERY_NO_MATCHES"
                    ]
                    printer.print_message("info", message)
                    if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                        LOGGER.info(message)
            except Exception:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_FAILURE"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
        else:
            db_model_queryset = self.db_controller.get_contracts(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data(
                    "contracts", db_model_queryset
                )
                console.print(table)
                printer.print_message(
                    "info", self.app_dict.get_appli_dictionnary()["NO_MORE_CONTRACT"]
                )
            else:
                print("Pas de contrat trouvé")

        return self.db_controller.get_contracts(self.session)

    def get_contract(self, contract_id):
        """
        Description: Vue dédiée à obtenir le contrat dont l'id est indiqué en entrée.
        Parameters:
        - contract_id: une chaine libre qui identifie un contrat.
        """
        return self.db_controller.get_contract(self.session, contract_id)

    def add_contract(self, contract):
        """
        Description: Vue dédiée à ajouter un contrat.
        Parameters:
        - contract: une instance du modèle de classe Contract.
        """
        return self.db_controller.add_contract(self.session, contract)

    def delete_contract(self, contract_id):
        """
        Description: Vue dédiée à supprimer un contrat.
        Parameters:
        - contract_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_contract(self.session, contract_id)

    def update_contract(self, app_view, current_user_collaborator_id, user_service, custom_dict):
        """
        Description: vue dédiée à mettre à jour un contrat.
        Parameters:
        - current_user_collaborator_id: l'id (la clef primaire, 'pas un custom id')
        - user_service: chaine de caractère, le nom du service de l'utilisateur courant (exemple: oc12_commercial)
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        event = self.get_attached_event(app_view, custom_dict["contract_id"])
        if "status" in custom_dict.keys() and event:
            raise exceptions.EventAttachedContractStatusCanNotBeUpdateException(event.title)
        return self.db_controller.update_contract(
            self.session, current_user_collaborator_id, user_service, custom_dict
        )

    def get_attached_event(self, app_view, contract_custom_id):
        """
        Description: dédié à chercher un évènement rattaché au contrat.
        Parameters:
        - contract_custom_id: custom_id d'un contrat
        """
        contract_id = utils.get_contract_id_from_contract_custom_id(self.session, contract_custom_id)
        event_attached = app_view.get_events_view().get_attached_event_to_contract(contract_id)
        return event_attached
