"""
Un controleur avec toutes méthodes pour ajouter des données.
"""
from sqlalchemy import text
try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


class DatabaseCreateController:
    """
    Description: Toutes les méthodes pour ajouter des données.
    """

    def add_client(self, session, client):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un client.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(client)
            session.commit()

            return client.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_collaborator(self, session, collaborator):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(collaborator)

            role = collaborator.registration_number
            password = settings.DEFAULT_NEW_COLLABORATOR_PASSWORD
            department_id = collaborator.department_id
            sql = text(f"""SELECT name FROM collaborator_department WHERE id = {department_id}""")
            result = session.execute(sql).first()
            department = str(result[0]).lower()

            if department == "oc12_gestion":
                sql = text(f"""CREATE ROLE {role} CREATEROLE LOGIN PASSWORD '{password}'""")
                session.execute(sql)
            else:
                sql = text(f"""CREATE ROLE {role} LOGIN PASSWORD '{password}'""")
                session.execute(sql)

            sql = text(f"""GRANT {department} TO {role}""")
            session.execute(sql)

            session.commit()

            return collaborator.id
        except Exception as error:
            print("ERROR SIR: ")
            print(f"Error while adding: {error}")

    def add_company(self, session, company):
        """
        Description: Fonction dédiée à servir la vue lors d'un ajout d'une entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(company)
            session.commit()

            return company.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_contract(self, session, contract):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un contrat.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(contract)
            session.commit()

            return contract.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_department(self, session, department):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un department /service pour l'entreprise.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(department)
            session.commit()
            return department.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_event(self, session, event):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un évènement.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(event)
            session.commit()

            return event.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_location(self, session, location):
        """
        Description: Fonction dédiée à servir la vue lors d'un ajout d'une localité (entreprise ou évènement).
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(location)
            session.commit()

            return location.id
        except Exception as error:
            print(f"Error while adding: {error}")

    def add_role(self, session, role):
        """
        Description: Fonction dédiée à servir la vue lors de l'ajout d'un rôle pour collaborateur.
        Requête de la base de données et renvoie l'id enregistré.
        """
        try:
            session.add(role)
            session.commit()

            return role.id
        except Exception as error:
            print(f"Error while adding: {error}")
