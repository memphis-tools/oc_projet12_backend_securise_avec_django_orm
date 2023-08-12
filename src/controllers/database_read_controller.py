"""
Un controleur avec toutes méthodes GET.
"""
import re
from sqlalchemy import and_, or_, not_, text
try:
    from src.models import models
except ModuleNotFoundError:
    from models import models


class DatabaseReadController:
    """
    Description: Toutes les méthodes GET.
    """

    def get_client(self, session, client_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'un client.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        Paramètres:
        - client_id: c'est le custom id (chaine libre)
        """
        try:
            db_client_queryset = (
                session.query(models.Client).filter_by(client_id=client_id).first()
            )

            return db_client_queryset
        except Exception as error:
            print(f"Client not found: {error}")

    def get_clients(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des clients de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Client.
        """
        db_collaborators_clients = session.query(models.Client).all()

        return db_collaborators_clients

    def get_collaborator(self, session, registration_number):
        """
        Description:
        Fonction dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(models.User)
                .filter_by(registration_number=registration_number)
                .first()
            )

            return db_collaborator_queryset
        except Exception as error:
            print(f"User or Department not found: {error}")

    def get_collaborator_join_department(self, session, registration_number):
        """
        Description:
        Méthode dédiée à servir la vue lors d'une requête d'un utilisateur de l'entreprise pour la création du token.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        Paramètres:
        - registration_number: c'est le matricule employé.
        """
        try:
            db_collaborator_queryset = (
                session.query(models.User, models.UserDepartment)
                .filter(models.User.department == models.UserDepartment.id)
                .filter_by(registration_number=registration_number)
                .first()
            )


            return db_collaborator_queryset
        except Exception as error:
            print(f"User or Department not found: {error}")

    def get_collaborators(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des utilisateurs de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle User.
        """
        db_collaborators = session.query(models.User).all()

        return db_collaborators

    def get_company(self, session, company_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'une entreprise cliente.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        try:
            db_company_queryset = (
                session.query(models.Company)
                # session.query(models.Company, models.Location)
                # .filter(models.Company.location_id == models.Location.id)
                .filter_by(company_id=company_id).first()
            )

            return db_company_queryset
        except Exception as error:
            print(f"Company not found: {error}")

    def get_companies(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des entreprises clientes de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Company.
        """
        db_companies = session.query(models.Company).all()

        return db_companies

    def get_contract(self, session, contract_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'un contrat de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        Paramètres:
        - contract_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_contract = (
                session.query(models.Contract)
                .filter_by(contract_id=contract_id)
                .first()
            )

            return db_collaborators_contract
        except Exception as error:
            print(f"Department not found: {error}")

    @classmethod
    def make_a_user_query_as_a_list(cls, splited_args):
        """
        Description:
        Fonction dédiée à déconstruire les arguments de filtres données par l'utilisateur.
        Elle est seulement utilisée par la fonction "get_filtered_contracts".
        """
        LOGICAL_OPERATORS_TAB_DICT = {
            "et": "AND",
            "ou": "OR"
        }
        user_query_as_a_list = []
        for arg in splited_args:
            arg_to_list = []
            if '=' in arg and not any(['<' in arg, '>' in arg]):
                arg_to_list = re.split('=', f"{arg}")
                arg_to_list.append('=')
            elif '>' in arg and '=' in arg:
                operator_index = arg.index("=")
                arg_to_list.append(arg[0:operator_index])
                arg_to_list.append(arg[operator_index+2:len(arg)+1])
                arg_to_list.append(">=")
            elif '>' in arg:
                arg_to_list = re.split('>', f"{arg}")
                arg_to_list.append('>')
            elif '<' in arg and '=' in arg:
                arg_to_list = re.split('<=', f"{arg}")
                arg_to_list.append('<=')
            elif '<' in arg:
                arg_to_list = re.split('<', f"{arg}")
                arg_to_list.append('<')
            elif arg in LOGICAL_OPERATORS_TAB_DICT:
                arg_to_list.append(LOGICAL_OPERATORS_TAB_DICT[arg])
            arg_tuple = tuple(arg_to_list)
            user_query_as_a_list.append(arg_tuple)
        return user_query_as_a_list


    def get_filtered_contracts(self, session, user_query_filters_args):
        """
        Description:
        Fonction dédiée à servir la vue lors d'une requête filtrée des contrats de l'entreprise.
        On peut ajouter des filtres avec 2 opérateurs logique "et, ou".
        """

        user_query_as_a_list = []
        filter_to_apply = ""
        try:
            # on va retirer tous les espaces possibles autour des opérateurs
            pattern_for_space_around_comparison_ops = re.compile(r'( *=> *| *<= *)')
            striped_operators = re.search(pattern_for_space_around_comparison_ops, user_query_filters_args)
            user_query_filters_args = user_query_filters_args.replace(striped_operators.group(), striped_operators.group().strip())
        except AttributeError:
            # pas d'espace autour des opérateurs, on ne fait rien
            pass

        # on éclate dans une liste chaque "triplet" (l'argument, l'opérateur, la valeur)
        splited_args = user_query_filters_args.split(" ")

        # on va déconstruire les arguments donnés par l'utilisateur dans une liste de tuple
        # elle aura une forme de type: [('status', 'signed', '='), ('AND',), ('remain_amount_to_pay', '0', '>=')]
        if len(splited_args) > 0:
            user_query_as_a_list = self.make_a_user_query_as_a_list(splited_args)
        for subquery_tuple in user_query_as_a_list:
            if len(subquery_tuple) > 1:
                item_key, item_value, item_operator = subquery_tuple
                if item_key == 'creation_date':
                    str_date = item_value.split("-")
                    item_value = str_date[2] + "-" + str_date[1] + "-" + str_date[0]
                filter_to_apply += f"(Contract.{item_key}{item_operator}'{item_value}')"
            else:
                filter_to_apply += f" {subquery_tuple[0]} "

        try:
            db_contracts = (
                session.query(models.Contract)
                .join(models.Client, models.Contract.client_id == models.Client.id)
                .join(models.Event, models.Contract.id == models.Event.contract_id)
                .filter(text(filter_to_apply))
                .all()
            )
            return db_contracts
        except Exception as error:
            print(f"Requête en échec: {error}")


    def get_contracts(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des contrats de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Contract.
        """
        db_collaborators_contracts = session.query(models.Contract).all()
        return db_collaborators_contracts

    def get_department(self, session, department_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'un département /service de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserDepartment.
        Paramètres:
        - department_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_department = (
                session.query(models.UserDepartment)
                .filter_by(department_id=department_id)
                .first()
            )

            return db_collaborators_department
        except Exception as error:
            print(f"Department not found: {error}")

    def get_departments(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des départements /services de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserDepartment.
        """
        db_collaborators_department = session.query(models.UserDepartment).all()

        return db_collaborators_department

    def get_event(self, session, event_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'un évènement de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        Paramètres:
        - event_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_event = (
                session.query(models.Event).filter_by(event_id=event_id).first()
            )

            return db_collaborators_event
        except Exception as error:
            print(f"Event not found: {error}")

    def get_events(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des évènements de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Event.
        """
        db_collaborators_events = session.query(models.Event).all()

        return db_collaborators_events

    def get_location(self, session, location_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        Paramètres:
        - location_id: chaine de caractères (ce n'est pas l'id integer pour la clef primaire).
        """
        try:
            db_locations_queryset = (
                session.query(models.Location)
                .filter_by(location_id=location_id)
                .first()
            )

            return db_locations_queryset
        except Exception as error:
            print(f"Location not found: {error}")

    def get_locations(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des localisations des évènements.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle Location.
        """
        db_collaborators_locations = session.query(models.Location).all()

        return db_collaborators_locations

    def get_role(self, session, role_id):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête d'un rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserRole.
        Paramètres:
        - role_id: c'est le custom id (chaine libre)
        """
        try:
            db_collaborators_role = (
                session.query(models.UserRole).filter_by(role_id=role_id).first()
            )

            return db_collaborators_role
        except Exception as error:
            print(f"Role not found: {error}")

    def get_roles(self, session):
        """
        Description:
		Méthode dédiée à servir la vue lors d'une requête des rôles du personnel de l'entreprise.
        Requête de la base de données et renvoie du résultat selon "str/repr" du modèle UserRole.
        """
        db_collaborators_role = session.query(models.UserRole).all()

        return db_collaborators_role
