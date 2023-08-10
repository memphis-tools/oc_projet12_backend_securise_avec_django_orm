"""
vue collaborateurs
"""
try:
    from src.utils import utils
    from src.settings import settings
    from src.validators import update_data_validators
except ModuleNotFoundError:
    from utils import utils
    from settings import settings
    from validators import update_data_validators


class CollaboratorsView:
    """
    Description: une classe dédiée à servir les vues pour les collaborateurs de l'entreprise.
    """

    def __init__(self, db_controller, db_initializer, session):
        """
        Description: vue dédiée à instancier avec les paramètres transmis par l'AppView
        """
        self.db_controller = db_controller
        self.db_initializer = db_initializer
        self.session = session

    def get_collaborators(self):
        """
        Description: vue dédiée à "méthode GET".
        """
        return self.db_controller.get_collaborators(self.session)

    def get_collaborator(self, collaborator_id):
        """
        Description: Vue dédiée à obtenir le collaborateur dont l'id est indiqué en entrée.
        Parameters:
        - collaborator_id: une chaine libre qui identifie un collaborateur.
        """
        return self.db_controller.get_collaborator(self.session, collaborator_id)

    def add_collaborator(self, collaborator):
        """
        Description: Vue dédiée à ajouter un collaborateur de l'entreprise.
        Parameters:
        - collaborator: une instance du modèle de classe User.
        """
        return self.db_controller.add_collaborator(self.session, collaborator)

    def delete_collaborator(self, collaborator_id):
        """
        Description: Vue dédiée à supprimer un collaborateur de l'entreprise.
        Parameters:
        - collaborator_id: id de l'objet (la clef primaire).
        """
        return self.db_controller.delete_collaborator(self.session, collaborator_id)

    def update_collaborator(self, custom_dict):
        """
        Description: vue dédiée à mettre à jour un collaborateur.
        Parameters:
        - custom_dict: un dictionnaire avec l'id et des données optionnelles.
        """
        return self.db_controller.update_collaborator(self.session, custom_dict)

    def update_collaborator_password(self, user_registration_number, old_password, new_password):
        """
        Description:
        Dédiée à mettre à jour le mot de passe d'un collaborateur.
        Parameters:
        - user_registration_number: chaine de caractères, le matricule de l'employé /du collaborateur.
        - old_password: chaine de caractères, l'ancien mot de passe de l'utilisateur /du collaborateur.
        - new_password: chaine de caractères, le nouveau mot de passe de l'utilisateur /du collaborateur.
        """
        conn = utils.get_a_database_connection(
            user_name=user_registration_number,
            user_pwd=old_password
        )
        return self.db_controller.update_collaborator_password(
            conn,
            user_registration_number,
            new_password
        )

    def old_collaborator_password_is_valid(
        self,
        user_registration_number,
        old_password,
        ):
        """
        Description:
        Dédiée à vérifier le mot de passe courant d'un collaborateur de l'entreprise.
        """
        return update_data_validators.old_collaborator_password_is_valid(
            user_registration_number,
            old_password,
        )

    def new_collaborator_password_is_valid(self, new_password):
        """
        Description:
        Dédiée à vérifier le nouveau mot de passe d'un collaborateur de l'entreprise.
        """
        return update_data_validators.new_collaborator_password_is_valid(new_password)
