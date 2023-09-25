"""
Description:
vue évènements
"""
from rich.console import Console

try:
    from src.languages import language_bridge
    from src.exceptions import exceptions
    from src.printers import printer
    from src.utils import utils
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from languages import language_bridge
    from exceptions import exceptions
    from printers import printer
    from utils import utils
    from settings import settings, logtail_handler


LOGGER = logtail_handler.logger


class EventsView:
    """
    Description: une classe dédiée à servir les vues pour les évènements de l'entreprise.
    """

    def __init__(self, db_controller, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.app_dict = language_bridge.LanguageBridge()
        self.db_controller = db_controller
        self.session = session

    def get_events(self, user_query_filters_args=""):
        """
        Description: vue dédiée à "méthode GET".
        """
        console = Console()
        if len(user_query_filters_args) > 0:
            try:
                db_model_queryset = self.db_controller.get_filtered_models(
                    self.session, user_query_filters_args[0], "Event"
                )
                if len(db_model_queryset) > 0:
                    table = utils.set_a_click_table_from_data(
                        "events", db_model_queryset
                    )
                    console.print(table)
                    printer.print_message(
                        "info", self.app_dict.get_appli_dictionnary()["NO_MORE_EVENT"]
                    )
                else:
                    message = self.app_dict.get_appli_dictionnary()[
                        "DATABASE_QUERY_NO_MATCHES"
                    ]
                    printer.print_message("info", message)
                    if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                        LOGGER.info(message)
                    raise exceptions.CustomIdMatchNothingException()
            except TypeError:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_NO_MATCHES"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
                raise exceptions.CustomIdMatchNothingException()
            except Exception:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_FAILURE"
                ]
                printer.print_message("error", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.error(message)
                raise exceptions.QueryFailureException()
        else:
            db_model_queryset = self.db_controller.get_events(self.session)
            if len(db_model_queryset) > 0:
                table = utils.set_a_click_table_from_data("events", db_model_queryset)
                console.print(table)
                printer.print_message(
                    "info", self.app_dict.get_appli_dictionnary()["NO_MORE_EVENT"]
                )
            else:
                message = self.app_dict.get_appli_dictionnary()[
                    "DATABASE_QUERY_NO_MATCHES"
                ]
                printer.print_message("info", message)
                if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                    LOGGER.info(message)
                raise exceptions.CustomIdMatchNothingException()

        return self.db_controller.get_events(self.session)

    def get_attached_event_to_contract(self, contract_id):
        """
        Description: Vue dédiée à obtenir l'évènement dont le contract_id est indiqué en entrée.
        Parameters:
        - contract_id: une chaine libre qui identifie un contrat.
        """
        return self.db_controller.get_attached_event(self.session, contract_id)

    def get_event(self, event_id):
        """
        Description: Vue dédiée à obtenir l'évènement dont l'id est indiqué en entrée.
        Parameters:
        - event_id: une chaine libre qui identifie un évènement.
        """
        return self.db_controller.get_event(self.session, event_id)

    def add_event(self, current_user_collaborator_id, event):
        """
        Description: Vue dédiée à ajouter un évènement.
        Parameters:
        - event: une instance du modèle de classe Event.
        """
        return self.db_controller.add_event(
            self.session, current_user_collaborator_id, event
        )

    def delete_event(self, event_id):
        """
        Description: Vue dédiée à supprimer un évènement.
        Parameters:
        - event_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_event(self.session, event_id)

    def update_event(self, current_user_collaborator_id, user_service, custom_dict):
        """
        Description: vue dédiée à mettre à jour un évènement.
        Parameters:
        - current_user_collaborator_id: l'id (la clef primaire, 'pas un custom id')
        - user_service: chaine de caractère, le nom du service de l'utilisateur courant (exemple: oc12_commercial)
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_event(
            self.session, current_user_collaborator_id, user_service, custom_dict
        )
