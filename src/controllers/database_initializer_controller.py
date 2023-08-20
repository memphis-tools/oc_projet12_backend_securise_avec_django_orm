import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse

try:
    from src.models import models
    from src.printers import printer
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from models import models
    from printers import printer
    from settings import settings
    from utils import utils


class DatabaseInitializerController:
    """
    Description:
    Le nécessaire pour initialiser la connexion à la base de données.
    On va se servir des identifiants de connexion du "role" auquel est rattaché l'utilisateur.
    Pour accéder à cette classe, il a été contrôlé la présence d'un JWT token valide (dans le PATH utilisateur).
    Toutes autres opérations que "lecture seule, GET, etc" imposeront à l'utilisateur de saisir son mot de passe.
    """
    # db_name = utils.set_database_to_get_based_on_user_path()
    def __init__(self, db_name):
        self.db_name = db_name

    def return_engine_and_session(
        self,
        user_login="",
        user_pwd="",
        decoded_token="",
        db_name="",
    ):
        """
        Description:
        Connexion à la base de données et renvoie le moteur dédié à initialiser les tables.
        Renvoie aussi de la session qui sera utilisée par la vue AppViews.
        """
        db_name=self.db_name
        try:
            if decoded_token == "":
                # l'utilisateur demande un token, c'est sa "connexion" initiale à l'application
                user_login = user_login
                user_pwd = user_pwd
            else:
                # l'utilisateur vient de demander un token, l'a obtenu et requete la bdd, on exploite le token décodé
                user_login = str(decoded_token["department"]).lower()
                dprt = str(decoded_token["department"]).upper()
                user_pwd = eval(f"settings.{dprt}_PWD")

            password_with_specialchars_escape = urllib.parse.quote_plus(user_pwd)
            engine = create_engine(
                f"postgresql+psycopg://{user_login}:{password_with_specialchars_escape}@localhost/{db_name}"
            )
        except psycopg.OperationalError as error:
            printer.print_message("error", self.app_dict.get_appli_dictionnary()['EXCEPTION_DATABASE_CONNECTION'])

        session_maker = sessionmaker(engine)
        session = session_maker()
        return (engine, session)

    def return_session(
        self,
        user_login="",
        user_pwd="",
        decoded_token="",
        db_name="",
    ):
        """
        Description:
        Connexion à la base de données et renvoie une fabrique session qui sera utilisée par la vue AppViews.
        """
        try:
            db_name = utils.set_database_to_get_based_on_user_path(db_name)
            if decoded_token == "":
                # l'utilisateur demande un token, c'est sa "connexion" initiale à l'application
                user_login = user_login
                user_pwd = user_pwd
            else:
                # l'utilisateur vient de demander un token, l'a obtenu et requete la bdd, on exploite le token décodé
                user_login = str(decoded_token["department"]).lower()
                dprt = str(decoded_token["department"]).upper()
                user_pwd = eval(f"settings.{dprt}_PWD")

            password_with_specialchars_escape = urllib.parse.quote_plus(user_pwd)
            engine = create_engine(
                f"postgresql+psycopg://{user_login}:{password_with_specialchars_escape}@localhost/{db_name}"
            )
        except psycopg.OperationalError as error:
            printer.print_message("error", self.app_dict.get_appli_dictionnary()['EXCEPTION_DATABASE_CONNECTION'])

        session_maker = sessionmaker(engine)
        session = session_maker()
        return session

    def init_db(self, engine):
        """
        Description:
        Dédiée à aider au développement. On détruit et (re)crée les tables de la base de données.
        """
        base = models.get_base()
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)

    def truncate_tables_index_for_reset_db(self, cursor):
        sql = """TRUNCATE TABLE client RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE collaborator RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE collaborator_department RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE collaborator_role RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE event RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE location RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

        sql = """TRUNCATE TABLE contract RESTART IDENTITY CASCADE"""
        cursor.execute(sql)

    def drop_more_roles_for_reset_db(self):
        """
        Description:
        Permet de mettre à jour les 2 bases de données pour la suppression des "roles services".
        exemple: le service oc12_gestion a des droits sur les 2 bdd. C'est un référencement à purger pour supprimer.
        """
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name="projet12"
        )
        cursor = conn.cursor()
        for role in ["aa123456789", "oc12_commercial", "oc12_gestion", "oc12_support"]:
            sql = f"""REASSIGN OWNED BY {role} TO postgres"""
            cursor.execute(sql)
            sql = f"""DROP OWNED BY {role}"""
            cursor.execute(sql)
            sql = f"""DROP ROLE IF EXISTS {role}"""
            cursor.execute(sql)

    def reset_db(self, engine, db_name="projet12"):
        """
        Description:
        Dédié à aider au développement. On détruit les tables de la base de données.
        """
        for db_name in settings.DATABASE_TO_CREATE:
            base = models.get_base()
            base.metadata.drop_all(engine)
            conn = utils.get_a_database_connection(
                f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=db_name
            )
            cursor = conn.cursor()
            tables_list = [
                "contract",
                "event",
                "client",
                "collaborator",
                "collaborator_department",
                "collaborator_role",
                "location",
            ]
            for table in tables_list:
                try:
                    sql = f"""TRUNCATE TABLE {table} CASCADE"""
                    cursor.execute(sql)
                except Exception:
                    continue
            if db_name == f"{settings.TEST_DATABASE_NAME}" or db_name == f"{settings.DEV_DATABASE_NAME}":
                # on va conserver le collaborateur aa123456789 pour le module de test test_jwt_authenticator
                for role in [
                    "ab123456789",
                    "ac123456789",
                    "ad123456789",
                    "ae123456789",
                    "af123456789",
                    "ag123456789",
                ]:
                    try:
                        sql = f"""REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {role}"""
                        cursor.execute(sql)
                        sql = f"""DROP ROLE IF EXISTS {role}"""
                        cursor.execute(sql)
                        sql = f"""DELETE FROM collaborator WHERE name={role}"""
                        cursor.execute(sql)
                    except Exception:
                        continue
            try:
                self.drop_more_roles_for_reset_db()
                self.truncate_tables_index_for_reset_db(cursor)
            except Exception:
                pass

            conn.commit()
            conn.close()

    def database_postinstall_task_for_test_db(
        self, db_name=f"{settings.TEST_DATABASE_NAME}"
    ):
        """
        Description:
        Sur la base de test on va maintenir un employé lambda "aa123456789" du service oc12_commercial.
        Ca permet de conserver l'éxécution des tests du module test_jwt_authenticator.py avant ceux des vues.
        """
        for db_name in settings.DATABASE_TO_CREATE:
            if db_name == f"{settings.TEST_DATABASE_NAME}" or db_name == f"{settings.DEV_DATABASE_NAME}":
                conn = utils.get_a_database_connection(
                    f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=db_name
                )
                cursor = conn.cursor()
                dummy_registration_number = "aa123456789"
                sql = f"""
                    CREATE ROLE {dummy_registration_number}
                    LOGIN PASSWORD '{settings.DEFAULT_NEW_COLLABORATOR_PASSWORD}'
                """
                try:
                    cursor.execute(sql)
                except psycopg.errors.DuplicateObject:
                    pass
                sql = f"""GRANT oc12_commercial TO {dummy_registration_number}"""
                cursor.execute(sql)
                conn.commit()
                conn.close()

    def database_postinstall_tasks(self, db_name="projet12"):
        """
        Description:
        Dédiée à mettre à jour la base de données après une création initiale.
        """
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=db_name
        )
        cursor = conn.cursor()
        for db_name in settings.DATABASE_TO_CREATE:
            if db_name == f"{settings.TEST_DATABASE_NAME}" or db_name == f"{settings.DEV_DATABASE_NAME}":
                dummy_registration_number = "aa123456789"

            sql = f"""ALTER DATABASE {db_name} OWNER TO {settings.ADMIN_LOGIN}"""
            cursor.execute(sql)

            sql = f"""ALTER USER {settings.ADMIN_LOGIN} WITH PASSWORD '{settings.ADMIN_PASSWORD}'"""
            cursor.execute(sql)

            sql = (
                f"""GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {settings.ADMIN_LOGIN}"""
            )
            cursor.execute(sql)

        for role in [
            ("oc12_commercial", f"{settings.OC12_COMMERCIAL_PWD}"),
            ("oc12_gestion", f"{settings.OC12_GESTION_PWD}"),
            ("oc12_support", f"{settings.OC12_SUPPORT_PWD}"),
        ]:
            # le privilège CREATEROLE ne sera pas hérité par défaut
            try:
                if role[0] == "oc12_gestion":
                    sql = f"""CREATE ROLE {role[0]} CREATEROLE LOGIN PASSWORD '{role[1]}'"""
                    cursor.execute(sql)
                else:
                    sql = f"""CREATE ROLE {role[0]} LOGIN PASSWORD '{role[1]}'"""
                    cursor.execute(sql)
            except Exception:
                pass

            for db_name in settings.DATABASE_TO_CREATE:
                sql = f"""GRANT CONNECT ON DATABASE {db_name} TO {role[0]}"""
                cursor.execute(sql)
            for model in [
                "client",
                "collaborator",
                "collaborator_department",
                "collaborator_role",
                "company",
                "contract",
                "event",
                "location",
            ]:
                sql = f"""GRANT SELECT ON {model} TO {role[0]}"""
                cursor.execute(sql)

        oc12_commercial_allowed_tables = [
            "client",
            "company",
            "event",
            "location",
        ]

        for table in oc12_commercial_allowed_tables:
            sql = f"""GRANT INSERT, DELETE, UPDATE ON {table} TO oc12_commercial"""
            cursor.execute(sql)
            sql = f"""GRANT USAGE ON SEQUENCE {table}_id_seq TO oc12_commercial"""
            cursor.execute(sql)
        sql = """GRANT UPDATE ON contract TO oc12_commercial"""
        cursor.execute(sql)
        sql = """GRANT UPDATE ON event TO oc12_commercial"""
        cursor.execute(sql)

        oc12_gestion_allowed_tables = [
            "collaborator",
            "collaborator_department",
            "collaborator_role",
            "contract",
            "event",
        ]
        for table in oc12_gestion_allowed_tables:
            sql = f"""GRANT INSERT, DELETE, UPDATE ON {table} TO oc12_gestion"""
            cursor.execute(sql)
            sql = f"""GRANT USAGE ON SEQUENCE {table}_id_seq TO oc12_gestion"""
            cursor.execute(sql)

        allowed_services = ["oc12_support"]
        for service in allowed_services:
            sql = f"""GRANT UPDATE ON event TO {service}"""
            cursor.execute(sql)
            sql = f"""GRANT USAGE ON SEQUENCE event_id_seq TO {service}"""
            cursor.execute(sql)

        self.database_postinstall_task_for_test_db(f"{settings.TEST_DATABASE_NAME}")
        self.database_postinstall_task_for_test_db(f"{settings.DEV_DATABASE_NAME}")

        conn.commit()
        conn.close()
        return True


    def database_postinstall_alter_tables(self, db_name="projet12"):
        """
        Description:
        Dédiée à forcer la mise à jour de valeurs par défaut.
        """
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=db_name
        )
        cursor = conn.cursor()

        sql = """ALTER TABLE client ALTER COLUMN creation_date SET NOT NULL"""
        cursor.execute(sql)

        sql = """ALTER TABLE client ALTER COLUMN last_update_date SET NOT NULL"""
        cursor.execute(sql)

        sql = """ALTER TABLE client ALTER COLUMN "creation_date" SET DEFAULT CURRENT_DATE"""
        cursor.execute(sql)

        sql = """ALTER TABLE client ALTER COLUMN "last_update_date" SET DEFAULT CURRENT_DATE"""
        cursor.execute(sql)

        sql = """ALTER TABLE contract ALTER COLUMN "creation_date" SET DEFAULT NOW()"""
        cursor.execute(sql)
        conn.commit()
        conn.close()
        return True
