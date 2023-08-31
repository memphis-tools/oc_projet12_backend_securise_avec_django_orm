"""
Description:
Console dédiée aux commandes infos
"""

try:
    from src.languages import language_bridge
    from src.printers import printer
    from src.controllers import infos_data_controller
    from src.controllers.infos_update_password_controller import (
        display_info_password_policy,
    )
    from src.settings import settings, logtail_handler
    from src.utils import utils
    from src.views.crud_views.views import AppViews
    from src.views.jwt_view import JwtView
except ModuleNotFoundError:
    from languages import language_bridge
    from printers import printer
    from controllers import infos_data_controller
    from controllers.infos_update_password_controller import (
        display_info_password_policy,
    )
    from settings import settings, logtail_handler
    from utils import utils
    from views.crud_views.views import AppViews
    from views.jwt_view import JwtView


LOGGER = logtail_handler.logger


class InformationConsoleClient:
    """
    Description: la classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self, db_name=f"{settings.DATABASE_NAME}"):
        """
        Description:
        On instancie la classe avec les vues qui permettront tous débranchements et actions.
        """
        db_name = utils.set_database_to_get_based_on_user_path(db_name=db_name)
        self.app_dict = language_bridge.LanguageBridge()
        self.app_view = AppViews(db_name=db_name)
        self.jwt_view = JwtView(self.app_view)

    @utils.authentication_permission_decorator
    def display_info_password_policy(self):
        """
        Description:
        Retourner la politique de mot de passe.
        """
        try:
            display_info_password_policy()
        except Exception as error:
            message = self.app_dict.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

    @utils.authentication_permission_decorator
    def display_info_data_medium_window_for_metiers(self):
        """
        Description:
        Ouvrir la popup dédiée.
        """
        infos_data_controller.display_info_data_medium_window("metiers")

    @utils.authentication_permission_decorator
    def display_info_data_medium_window_for_complement_adresse(self):
        """
        Description:
        Ouvrir la popup dédiée.
        """
        infos_data_controller.display_info_data_thin_window("types_voies")
