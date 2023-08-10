import sys
import subprocess
import psycopg
from sqlalchemy import text
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
        except KeyError:
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


def get_a_database_connection(user_name="", user_pwd="", db_name=f"{settings.DATABASE_NAME}"):
    """
    Description:
    Dédiée à obtenir un curseur pour interragir avec le SGBD.
    """
    if user_name != "" and user_pwd != "":
        user = user_name
        password = user_pwd
    else:
        user = f"{settings.ADMIN_LOGIN}"
        password = f"{settings.ADMIN_PASSWORD}"
    conn = psycopg.connect(
        dbname=db_name,
        user=user,
        password=password,
        host=f"{settings.DATABASE_HOST}",
        port=f"{settings.DATABASE_PORT}",
    )
    conn.autocommit = True
    return conn


def get_department_name_from_id(session, department_id):
    """
    Description:
    Récupérer le nom du service /département à partir de l'id.
    C'est un besoin récurrent lors de la mise à jour des collaborateurs.
    Leur attribut department est la clef étrangère de celui-ci.
    Paramètres:
    - session: une session ouverte sur la base de données
    - department_id: entier, clef primaire d'un service /department
    """
    sql = text(f"""SELECT name FROM collaborator_department WHERE id = '{department_id}'""")
    result = session.execute(sql).first()
    department_name = str(result[0]).lower()
    return department_name


def get_department_id_from_name(session, department_name):
    """
    Description:
    Récupérer le id du service /département à partir du nom.
    C'est un besoin récurrent lors de la mise à jour des collaborateurs.
    Paramètres:
    - session: une session ouverte sur la base de données
    - department_name: chaine de caractères qui doit être un service existant
    """
    sql = text(f"""SELECT id FROM collaborator_department WHERE name='{department_name}'""")
    result = session.execute(sql).first()
    department_id = str(result[0]).lower()
    return department_id


def update_grant_for_collaborator(session, registration_number, current_department_name, new_department_name):
    """
    Description:
    Sert lors de la mise à jour du service d'un collaborateur.
    Il doit hériter des droits du 'role' (sens postgresql) parent.
    Il doit perdre les droits du 'role' précedemment parent.
    Pour l'ajout au service gestion il faut explicitement donner le privilège CREATEROLE.
    Paramètres:
    - session: une session ouverte sur la base de données
    - registration_number: chaine de caractères qui correspond à un matricule employé /collaborateur
    - current_department_name: chaine de caractères qui doit être un service existant
    - new_department_name: chaine de caractères qui doit être un service existant
    """
    sql = text(f"""REVOKE {current_department_name} FROM {registration_number}""")
    session.execute(sql)
    sql = text(f""" GRANT {new_department_name} TO {registration_number}""")
    session.execute(sql)
    if current_department_name == "oc12_gestion":
        sql = text(f"""ALTER ROLE {registration_number} NOCREATEROLE""")
        session.execute(sql)
    if new_department_name == "oc12_gestion":
        sql = text(f"""ALTER ROLE {registration_number} CREATEROLE""")
        session.execute(sql)
    return True


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


def dummy_database_creation(db_name="projet12"):
    """
    Description:
    Dédiée à peupler la base de données avec des données fictives
    """
    conn = get_a_database_connection(
        f"{settings.ADMIN_LOGIN}", f"{settings.ADMIN_PASSWORD}", db_name=db_name
    )
    cursor = conn.cursor()

    sql = """INSERT INTO collaborator_department(department_id, name) VALUES('ccial', 'oc12_commercial')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_department(department_id, name) VALUES('gest', 'oc12_gestion')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_department(department_id, name) VALUES('supp', 'oc12_support')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_role(role_id, name) VALUES('man', 'MANAGER')"""
    cursor.execute(sql)

    sql = """INSERT INTO collaborator_role(role_id, name) VALUES('emp', 'EMPLOYEE')"""
    cursor.execute(sql)

    # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('aa123456789', 'donald duck', '1', '1')
    """
    try:
        cursor.execute(sql)
    except:
        pass

    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ab123456789', 'Bill Boquet', '1', '2')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ac123456789', 'daisy duck', '2', '1')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ad123456789', 'loulou duck', '2', '2')
    """
    cursor.execute(sql)

    # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ae123456789', 'louloute duck', '3', '2')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('af123456789', 'Aliénor Vichum', '3', '2')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department, role)
        VALUES('ag123456789', 'Kate Hastroff', '3', '2')
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
        except:
            continue

    # 1 localisation en exemple pour une entreprise
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays)
    VALUES('p22240', '9 avenue de la bonbonière', '', '22240', 'Plurien', 'France')
    """
    cursor.execute(sql)

    # 1 entreprise en exemple
    sql = """
    INSERT INTO company
    (company_id, company_name, company_registration_number, company_subregistration_number, location_id)
    VALUES ('CSLLC12345', 'Cool Startup LLC', '777222888', '12345', '1')
    """
    cursor.execute(sql)

    # 2 client en exemples
    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email, telephone, company_id, commercial_contact)
    VALUES('mkc111', 'MR', 'Kevin', 'Casey', 'Press Officer', 'kevin@startup.io', '067812345678', '1', '2')
    """
    cursor.execute(sql)

    # 2 contrat en exemples
    sql = """
    INSERT INTO contract(contract_id, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id)
    VALUES('kc555', '999.99', '999.99', 'False', '1', '1')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO contract(contract_id, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id)
    VALUES('ff555', '444.55', '20.99', 'True', '1', '2')
    """
    cursor.execute(sql)

    # 1 localisation en exemple pour un évènement
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays)
    VALUES('csb41120', '53 Rue du Château', '', '41120', 'Candé-sur-Beuvron', 'France')
    """
    cursor.execute(sql)

    # 1 évènement en exemple
    sql = """
    INSERT INTO event(
        event_id,
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
        'hob2023',
        'Holiday on beach',
        '1',
        '1',
        '5',
        '2023-07-25 16:00:00.000000',
        '2023-07-25 22:00:00.000000',
        '2',
        '500',
        'bla bla bla penser au catering'
    )
    """
    cursor.execute(sql)

    conn.commit()
    conn.close()
