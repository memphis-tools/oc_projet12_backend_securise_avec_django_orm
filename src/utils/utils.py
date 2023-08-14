import sys
import re
import subprocess
import psycopg
from sqlalchemy import text
from rich import print
from rich.table import Table
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


def set_a_click_table_from_data(title: str, objects_queryset):
    """
    Description: (...).
    Paramètres:
    - title: chaine de caractères
    - objects_queryset: une liste, de taille 1, avec 1 string dedans.
        C'est le résultat de la requête à la base de données, chaque modèle métier est traduit /représenté par sa mth __str__
        La méthode est une pseudo représentation d'une liste avec des pseudo ensembles (attribut|valeur)
        Le queryset est donc une liste avec autant de listes incluses que de résultat trouvé
        exemple:
        [['(creation_date|12-08-2023),(contract_id|kc555),('client_id', 'Kevin Casey'),], [...]']
        C'est une pseudo représentation de ce qu'on souhaite. On va transformer chaque résultat en une liste de tuple:
        [[('creation_date', '12-08-2023'),('contract_id', 'kc555'),('client_id', 'Kevin Casey')], [...]]
    """
    rebuilt_queryset = []
    for result_object in objects_queryset:
        splited_data_list = []
        # result_object: nous permet d'atteindre la string dans la liste
        # str(result_object).split(","): la string est vue comme de type "Métier" (exemple Contrat), on force le cast en str
        for temp_attribute in str(result_object).split(","):
            # on parcourt chaque élement qui est de type str: '(creation_date|12-08-2023)'
            # on fait un slice pour retirer les parenthèses, on modifie "|" par une ",", on retire espace vide en début de string
            temp_attribute = temp_attribute[1:-1].replace("|", ",").lstrip()
            # on obtient un elément de type str: creation_date,12-08-2023
            # on l'éclate en une liste qu'on cast en tuple
            tuple_attribute = tuple(temp_attribute.split(","))
            # on ajoute à la liste splited_data_list un tuple: ('creation_date', '12-08-2023')
            splited_data_list.append(tuple_attribute)
        rebuilt_queryset.append(splited_data_list)
    # on obtient (pour chaque résultat): ['(creation_date: 12-08-2023)','(contract_id: kc555)','(client_id: Kevin Casey)',]

    headers = []
    [headers.append(attr_tuple[0].replace("(","")) for attr_tuple in splited_data_list]
    table = Table(title=title, style="blue", show_lines=True)
    for header in headers:
        if "date" in header:
            table.add_column(header.replace('_', ' '), justify="center", style="cyan", no_wrap=True)
        else:
            table.add_column(header.replace('_', ' '), justify="left", style="cyan", no_wrap=False)
    for result in rebuilt_queryset:
        values = []
        [values.append(attr_tuple[1].replace(")","")) for attr_tuple in result]
        table.add_row(*values)
    return table


def make_a_user_query_as_a_list(splited_args):
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


def rebuild_filter_query(user_query_filters_args, filtered_db_model):
    """
    Description:
    Fonction utilisée lorsque l'utilisateur demande une vue filtrée.
    On construit une reqûte SQL au travers des arguments précisés par l'utilisateur.
    On peut ajouter des filtres avec 2 opérateurs logique "et, ou".
    - user_query_filters_args: chaine de caractère avec 1 ou plusieurs filtres.
        Exemple pour contrats: "status=signed et remain_amount_to_pay =>0"
    """
    user_query_as_a_list = []
    filter_to_apply_rebuilt_query = ""
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
        user_query_as_a_list = make_a_user_query_as_a_list(splited_args)
    for subquery_tuple in user_query_as_a_list:
        if len(subquery_tuple) > 1:
            item_key, item_value, item_operator = subquery_tuple
            if item_key == 'creation_date':
                str_date = item_value.split("-")
                item_value = str_date[2] + "-" + str_date[1] + "-" + str_date[0]
            # filtered_db_model: Contract, Collaborator_Role, Client etc
            # Le nom doit être celui de la table (__tablename__) du modèle.
            # exemple: si filtered_db_model=='Contract' on aura 'contract.creation_date' en requête
            filter_to_apply_rebuilt_query += f"({filtered_db_model}.{item_key}{item_operator}'{item_value}')"
        else:
            filter_to_apply_rebuilt_query += f" {subquery_tuple[0]} "
    return filter_to_apply_rebuilt_query


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

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('ccial', 'oc12_commercial', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('gest', 'oc12_gestion', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('supp', 'oc12_support', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_role(role_id, name, creation_date)
        VALUES('man', 'MANAGER', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_role(role_id, name, creation_date)
        VALUES('emp', 'EMPLOYEE', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('aa123456789', 'donald duck', '1', '1', '2022-08-02 09:35:14')
    """
    try:
        cursor.execute(sql)
    except:
        pass

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ab123456789', 'Bill Boquet', '1', '2', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ac123456789', 'daisy duck', '2', '1', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ad123456789', 'loulou duck', '2', '2', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ae123456789', 'louloute duck', '3', '2', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('af123456789', 'Aliénor Vichum', '3', '2', '2022-08-02 09:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ag123456789', 'Kate Hastroff', '3', '2', '2022-08-02 09:35:14')
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

    # 2 localisations en exemple pour 2 entreprises
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays, creation_date)
    VALUES('p22240', '9 avenue de la bonbonière', '', '22240', 'Plurien', 'France', '2022-01-02 09:35:14')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays, creation_date)
    VALUES('llb44430', 'Place de la Bretagne', '', '44430', 'Le Loroux-Bottereau', 'France', '2019-07-09 14:08:10')
    """
    cursor.execute(sql)

    # 2 entreprises en exemple
    sql = """
    INSERT INTO company
    (company_id, company_name, company_registration_number, company_subregistration_number, location_id, creation_date)
    VALUES ('CSLLC12345', 'Cool Startup LLC', '777222888', '12345', '1', '2023-08-02 09:35:14')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO company
    (company_id, company_name, company_registration_number, company_subregistration_number, location_id, creation_date)
    VALUES ('NFEPG12345', 'Nantes Free Escape Games', '865333888', '44888', '2', '2019-07-09 14:10:20')
    """
    cursor.execute(sql)

    # 2 clients en exemples
    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email, telephone, company_id, commercial_contact, creation_date)
    VALUES('mkc111', 'MR', 'Kevin', 'Casey', 'Press Officer', 'kevin@startup.io', '067812345678', '1', '2', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email, telephone, company_id, commercial_contact, creation_date)
    VALUES('axs40', 'MLE', 'Alexia', 'Strak', 'Accountancy Officer', 'a.strak@startup.io', '067812345678', '2', '2', '2020-10-15 16:12:20')
    """
    cursor.execute(sql)

    # 3 contrats en exemples
    sql = """
    INSERT INTO contract(contract_id, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id, creation_date)
    VALUES('kc555', '999.99', '999.99', 'unsigned', '1', '1', '2023-06-02 09:35:25')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id, creation_date)
    VALUES('ff555', '444.55', '20.99', 'signed', '1', '2', '2022-01-16 10:40:14')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id, creation_date)
    VALUES('zz123', '72.5', '0', 'signed', '2', '1','2021-04-15 14:40:14')
    """
    cursor.execute(sql)

    # 2 localisations en exemple pour 2 évènement
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays, creation_date)
    VALUES('csb41120', '53 Rue du Château', '', '41120', 'Candé-sur-Beuvron', 'France', '2023-08-02 09:35:14')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville, pays, creation_date)
    VALUES('ggg56110', '20 Rue de Carhaix', '', '56110', 'Gourin', 'France', '2023-08-02 09:35:14')
    """
    cursor.execute(sql)

    # 3 évènements en exemple
    sql = """
    INSERT INTO event(
        event_id,
        creation_date,
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
        '2023-07-03 10:35:22',
        'Holiday on beach',
        '1',
        '1',
        '5',
        '2023-07-25 16:00',
        '2023-07-25 22:00',
        '1',
        '500',
        'bla bla bla penser au catering'
    )
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO event(
        event_id,
        creation_date,
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
        'geg2022',
        '2022-02-15 08:32:15',
        'Gourin escape game 2022',
        '2',
        '1',
        '2',
        '2022-07-25 16:00',
        '2022-07-25 22:00',
        '2',
        '35',
        'bla bla bla penser à tout le nécessaire. Ne pas oublier de gâteaux à la crème.'
    )
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO event(
        event_id,
        creation_date,
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
        'geg2021',
        '2021-07-03 14:25:10',
        'Gourin escape game 2021',
        '3',
        '2',
        '1',
        '2021-07-25 16:00',
        '2021-07-25 22:00',
        '2',
        '35',
        'bla bla bla penser à tout le nécessaire. Ne pas oublier de gâteaux à la crème.'
    )
    """
    cursor.execute(sql)

    conn.commit()
    conn.close()
