"""
Description:
Sert à initialiser la base de données, lors de l'initialisation de l'application.
On met en place les tables types, droits. Peuplement initial des base de dev et de test.
"""
import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import urllib.parse
from datetime import datetime

try:
    from src.languages import language_bridge
    from src.models import models
    from src.printers import printer
    from src.settings import settings, logtail_handler
    from src.utils import utils
except ModuleNotFoundError:
    from languages import language_bridge
    from models import models
    from printers import printer
    from settings import settings, logtail_handler
    from utils import utils


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


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
        db_name = self.db_name
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
            message = APP_DICT.get_appli_dictionnary()["EXCEPTION_DATABASE_CONNECTION"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)
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
            message = APP_DICT.get_appli_dictionnary()["EXCEPTION_DATABASE_CONNECTION"]
            printer.print_message("error", message)
            if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
                LOGGER.error(message)

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
            f"{settings.ADMIN_LOGIN}",
            f"{settings.ADMIN_PASSWORD}",
            app_init=True,
            db_name="projet12",
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
                f"{settings.ADMIN_LOGIN}",
                f"{settings.ADMIN_PASSWORD}",
                app_init=True,
                db_name=db_name,
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
            test_db_name = db_name == f"{settings.TEST_DATABASE_NAME}"
            if db_name == test_db_name or db_name == f"{settings.DEV_DATABASE_NAME}":
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
                        sql = (
                            f"""REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {role}"""
                        )
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

    def database_postinstall_task_for_test_db(self, conn):
        """
        Description:
        Sur les bases de test et dev on va maintenir un employé lambda "aa123456789" du service oc12_commercial.
        Ca permet de conserver l'éxécution des tests du module test_jwt_authenticator.py avant ceux des vues.
        """
        for db_name in settings.DATABASE_TO_CREATE:
            test_db_name = db_name == f"{settings.TEST_DATABASE_NAME}"
            if db_name == test_db_name or db_name == f"{settings.DEV_DATABASE_NAME}":
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
        return True

    def database_postinstall_tasks(self, db_name="projet12"):
        """
        Description:
        Dédiée à mettre à jour la base de données après une création initiale.
        On met en place le compte admin (qui aura les mêmes droits que le role par défaut postgres).
        On crée les services attendus par défaut, et on fixe leurs droits sur les tables.
        """
        init_db_name = db_name
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}",
            f"{settings.ADMIN_PASSWORD}",
            app_init=True,
            db_name=init_db_name,
        )

        cursor = conn.cursor()
        for db_name in settings.DATABASE_TO_CREATE:
            test_db_name = f"{settings.TEST_DATABASE_NAME}"
            if db_name == test_db_name or db_name == f"{settings.DEV_DATABASE_NAME}":
                dummy_registration_number = "aa123456789"

            sql = f"""ALTER DATABASE {db_name} OWNER TO {settings.ADMIN_LOGIN}"""
            cursor.execute(sql)

            sql = f"""ALTER USER {settings.ADMIN_LOGIN} WITH PASSWORD '{settings.ADMIN_PASSWORD}'"""
            cursor.execute(sql)

            sql = f"""GRANT ALL PRIVILEGES ON DATABASE {db_name} TO {settings.ADMIN_LOGIN}"""
            cursor.execute(sql)

        db_name = init_db_name

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
            conn.commit()

        oc12_commercial_allowed_tables = [
            "company",
            "location",
        ]

        for table in oc12_commercial_allowed_tables:
            sql = f"""GRANT INSERT, DELETE, UPDATE ON {table} TO oc12_commercial"""
            cursor.execute(sql)
            sql = f"""GRANT USAGE ON SEQUENCE {table}_id_seq TO oc12_commercial"""
            cursor.execute(sql)

        sql = """GRANT INSERT, UPDATE ON client TO oc12_commercial"""
        cursor.execute(sql)
        sql = """GRANT USAGE ON SEQUENCE client_id_seq TO oc12_commercial"""
        cursor.execute(sql)
        sql = """GRANT INSERT ON event TO oc12_commercial"""
        cursor.execute(sql)
        sql = """GRANT USAGE ON SEQUENCE event_id_seq TO oc12_commercial"""
        cursor.execute(sql)
        sql = """GRANT UPDATE ON contract TO oc12_commercial"""
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
        sql = """GRANT DELETE, UPDATE ON client TO oc12_gestion"""
        cursor.execute(sql)
        sql = """GRANT USAGE ON SEQUENCE client_id_seq TO oc12_gestion"""
        cursor.execute(sql)

        allowed_services = ["oc12_support"]
        for service in allowed_services:
            sql = f"""GRANT UPDATE ON event TO {service}"""
            cursor.execute(sql)
            sql = f"""GRANT USAGE ON SEQUENCE event_id_seq TO {service}"""
            cursor.execute(sql)

        self.database_postinstall_task_for_test_db(conn)

        conn.commit()
        conn.close()
        return True

    def database_postinstall_add_default_collaborators(self, db_name="projet12"):
        """
        Description:
        On crée des collaborateurs par défaut de chaque service de l'entreprise.
        Ca amène d'abord à créer des rôles, et les services, puis les collaborateurs.
        """
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}",
            f"{settings.ADMIN_PASSWORD}",
            app_init=True,
            db_name=db_name,
        )
        cursor = conn.cursor()
        sql = f"""
            INSERT INTO collaborator_department(department_id, name, creation_date)
            VALUES('ccial', 'oc12_commercial', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator_department(department_id, name, creation_date)
            VALUES('gest', 'oc12_gestion', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator_department(department_id, name, creation_date)
            VALUES('supp', 'oc12_support', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator_department(department_id, name, creation_date)
            VALUES('dev', 'oc12_developer', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator_role(role_id, name, creation_date)
            VALUES('man', 'MANAGER', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator_role(role_id, name, creation_date)
            VALUES('emp', 'EMPLOYEE', '{datetime.now()}')
        """
        cursor.execute(sql)

        # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('aa123456789', 'donald duck', '1', '1', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('ab123456789', 'Bill Boquet', '1', '2', '{datetime.now()}')
        """
        cursor.execute(sql)

        # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('ac123456789', 'daisy duck', '2', '1', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('ad123456789', 'loulou duck', '2', '2', '{datetime.now()}')
        """
        cursor.execute(sql)

        # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('ae123456789', 'louloute duck', '3', '2', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('af123456789', 'Aliénor Vichum', '3', '2', '{datetime.now()}')
        """
        cursor.execute(sql)

        sql = f"""
            INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
            VALUES('ag123456789', 'Kate Hastroff', '3', '2', '{datetime.now()}')
        """
        cursor.execute(sql)
        conn.commit()

        # On crée un "rôle" pour chaque utilisateur prévu. Chacun hérite des permissions de son service.
        # on crée le try/except parce qu'on ne CREATE/GRANT qu'une fois pour N bases.
        password = settings.DEFAULT_NEW_COLLABORATOR_PASSWORD
        for user in [
            ("aa123456789", "oc12_commercial"),
            ("ab123456789", "oc12_commercial"),
            ("ac123456789", "oc12_gestion"),
            ("ad123456789", "oc12_gestion"),
            ("ae123456789", "oc12_support"),
            ("af123456789", "oc12_support"),
            ("ag123456789", "oc12_support"),
        ]:
            try:
                if user[1] == "oc12_gestion":
                    sql = f"""CREATE ROLE {user[0]} CREATEROLE LOGIN PASSWORD '{password}'"""
                    cursor.execute(sql)
                else:
                    sql = f"""CREATE ROLE {user[0]} LOGIN PASSWORD '{password}'"""
                    cursor.execute(sql)
                sql = f"""GRANT {user[1]} TO {user[0]}"""
                cursor.execute(sql)
                conn.commit()
            except Exception:
                continue
        conn.commit()
        conn.close()
        return True

    def database_postinstall_alter_tables(self, db_name="projet12"):
        """
        Description:
        Dédiée à forcer la mise à jour de valeurs par défaut.
        """
        conn = utils.get_a_database_connection(
            f"{settings.ADMIN_LOGIN}",
            f"{settings.ADMIN_PASSWORD}",
            app_init=True,
            db_name=db_name,
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
