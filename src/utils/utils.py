import sys
import subprocess
import psycopg
from rich import print
from functools import wraps
import jwt
import pyfiglet
from termcolor import colored, cprint
from werkzeug.security import generate_password_hash, check_password_hash

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


def authentication_permission_decorator(func):
    @wraps(func)
    def check_user_token(*args, **kwargs):
        try:
            if args[0].jwt_view.does_a_valid_token_exist():
                return func(*args, **kwargs)
            print("[bold red]Access forbidden without valid token[/bold red]")
            sys.exit(0)
        except jwt.exceptions.InvalidSignatureError:
            print("[bold red]Access forbidden without valid token[/bold red]")
            sys.exit(0)

    return check_user_token


def authorization_permission_decorator(func):
    """
    Description: (...).
    """
    pass


def display_banner():
    """
    Description: Afficher la bannière.
    """
    text = f"{settings.APP_FIGLET_TITLE}"
    cprint(colored(pyfiglet.figlet_format(text, font="digital", width=100), "cyan"))


def generate_password_hash_from_input(password):
    """
    Description: Permettre un hachage et salage du mot de passe utilisateur en base.
    """
    hashed_and_salted = generate_password_hash(password, "pbkdf2:sha256", salt_length=8)
    return hashed_and_salted


def check_password_hash_from_input(db_user_password, password):
    """
    Description:
    Comparer le mot de passe saisi lors d'une authentification avec celui en base de données.
    """
    return check_password_hash(db_user_password, password)


def get_a_database_connection(user_name, user_pwd):
    """
    Description:
    Dédiée à obtenir un curseur pour interragir avec le SGBD.
    """
    conn = psycopg.connect(
        dbname=f"{settings.DATABASE_NAME}",
        user=f"{settings.ADMIN_LOGIN}",
        password=f"{settings.ADMIN_PASSWORD}",
        host=f"{settings.DATABASE_HOST}",
        port=f"{settings.DATABASE_PORT}",
    )
    conn.autocommit = True
    return conn


def display_postgresql_controls():
    """
    Description:
    Controles spécifiques à une distribution Linux, et à Postgresql.
    """
    try:
        execution_code = subprocess.run(
            ["systemctl", "is-active", "postgresql"],
            shell=True,
            check=True,
            capture_output=True,
        )
        if execution_code.returncode == 0:
            print(
                "[bold green][START CONTROL][/bold green] service postgresql is active"
            )
        else:
            raise subprocess.CalledProcessError()
    except subprocess.CalledProcessError as error:
        print(f"[bold red] error:[/bold red] {error}")

    try:
        subprocess.run(["id", "postgres"], shell=True, check=True, capture_output=True)
        print("[bold green][START CONTROL][/bold green] user postgres exists")
    except subprocess.CalledProcessError as error:
        print(f"[START CONTROL] error: {error}")

    return True


def database_postinstall_alter_tables():
    """
    Description:
    Dédiée à forcer la mise à jour de valeurs par défaut.
    """
    conn = get_a_database_connection(f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}")
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


def database_postinstall_tasks():
    """
    Description:
    Dédiée à mettre à jour la base de données après une création initiale.
    """
    conn = get_a_database_connection(f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}")
    cursor = conn.cursor()

    sql = f"""ALTER DATABASE {settings.DATABASE_NAME} OWNER TO {settings.ADMIN_LOGIN}"""
    cursor.execute(sql)

    sql = f"""ALTER USER {settings.ADMIN_LOGIN} WITH PASSWORD '{settings.ADMIN_PASSWORD}'"""
    cursor.execute(sql)

    sql = f"""GRANT ALL PRIVILEGES ON DATABASE {settings.DATABASE_NAME} TO {settings.ADMIN_LOGIN}"""
    cursor.execute(sql)

    # Environnement de développement, on ré-initialise les ids des "collaborators", "location", etc
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

    # on crée un "role" pour chaque départements de l'entreprise

    # VOIR SI DROP A CONSERVER POST POC
    # d'abord on se débarasse de précédentes données de POC
    try:
        for role in [
            "aa123456789",
            "ab123456789",
            "ac123456789",
            "ad123456789",
            "ae123456789",
            "af123456789",
            "ag123456789"
        ]:
            sql = f"""REVOKE ALL ON ALL TABLES IN SCHEMA public FROM {role}"""
            cursor.execute(sql)
            conn.commit()
            sql = f"""DROP ROLE IF EXISTS {role}"""
            cursor.execute(sql)
        conn.commit()
    except:
        pass

    for role in ["oc12_commercial", "oc12_gestion", "oc12_support"]:
        sql = f"""DROP ROLE IF EXISTS {role}"""
        cursor.execute(sql)
        conn.commit()

    for role in [
        ("oc12_commercial", f"{settings.OC12_COMMERCIAL_PWD}"),
        ("oc12_gestion", f"{settings.OC12_GESTION_PWD}"),
        ("oc12_support", f"{settings.OC12_SUPPORT_PWD}")
    ]:
        sql = f"""CREATE ROLE {role[0]} LOGIN PASSWORD '{role[1]}'"""
        cursor.execute(sql)
        sql = f"""GRANT CONNECT ON DATABASE projet12 TO {role[0]}"""
        cursor.execute(sql)
        # voir si on peut exclure la table collaborator et collaborator_department
        # attention ils sont utilisés pour la mécanique de controle des autorisations
        for model in ["client", "collaborator", "collaborator_department", "contract", "event", "location"]:
            sql = f"""GRANT SELECT ON {model} TO {role[0]}"""
            cursor.execute(sql)

    conn.commit()
    conn.close()
    return True

def dummy_database_creation():
    """
    Description:
    Dédiée à peupler la base de données avec des données fictives
    """
    conn = get_a_database_connection(f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}")
    cursor = conn.cursor()

    sql = """INSERT INTO collaborator_department(name) VALUES('OC12_COMMERCIAL')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_department(name) VALUES('OC12_GESTION')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_department(name) VALUES('OC12_SUPPORT')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_role(name) VALUES('MANAGER')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_role(name) VALUES('EMPLOYEE')"""
    cursor.execute(sql)

    # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('aa123456789', 'donald duck', '1', '1')
    """
    cursor.execute(sql)

    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ab123456789', 'Bill Boquet', '1', '2')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ac123456789', 'daisy duck', '2', '1')
    """
    cursor.execute(sql)

    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ad123456789', 'loulou duck', '2', '2')
    """
    cursor.execute(sql)

    # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ae123456789', 'louloute duck', '2', '2')
    """
    cursor.execute(sql)

    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('af123456789', 'Aliénor Vichum', '3', '2')
    """
    cursor.execute(sql)

    sql = f"""
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ag123456789', 'Kate Hastroff', '3', '2')
    """
    cursor.execute(sql)

    conn.commit()

    # On crée un "rôle" pour chaque utilisateur prévu. Chacun hérite des permissions de son service.
    for user in [
        ("aa123456789", "oc12_commercial"),
        ("ab123456789", "oc12_commercial"),
        ("ac123456789", "oc12_gestion"),
        ("ad123456789", "oc12_gestion"),
        ("ae123456789", "oc12_support"),
        ("af123456789", "oc12_support"),
        ("ag123456789", "oc12_support")
    ]:
        sql = f"""CREATE ROLE {user[0]} LOGIN PASSWORD 'applepie94'"""
        cursor.execute(sql)
        sql = f"""GRANT {user[1]} TO {user[0]}"""
        cursor.execute(sql)
        conn.commit()

    # 1 client en exemple
    sql = """
    INSERT INTO client(information, fullname, email, telephone, company_name, commercial_contact)
    VALUES('Exemple bla bla bla', 'Kevin Casey', 'kevin@startup.io', '+678 123 456 78', 'Cool Startup LLC', '2')
    """
    cursor.execute(sql)

    # 1 contrat en exemple
    sql = """
    INSERT INTO contract(information, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id)
    VALUES('Memes infos que le client ?', '999.99', '999.99', 'False', '1', '2')
    """
    cursor.execute(sql)

    # 1 localisation en exemple
    sql = """
    INSERT INTO location(adresse, complement_adresse, code_postal, ville, pays)
    VALUES('53 Rue du Château', '', '41120', 'Candé-sur-Beuvron', 'France')
    """
    cursor.execute(sql)

    # 1 évènement en exemple
    sql = """
    INSERT INTO event(
        title,
        contract_id,
        client_id,
        collaborator_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes
    )
    VALUES(
        'Holiday on beach',
        '1',
        '1',
        '5',
        '2023-07-25 16:00:00.000000',
        '2023-07-25 22:00:00.000000',
        '1',
        '500',
        'bla bla bla penser au catering'
    )
    """
    cursor.execute(sql)

    conn.commit()
    conn.close()
