import subprocess
import psycopg
from rich import print

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


def get_a_database_connection():
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
    conn = get_a_database_connection()
    cursor = conn.cursor()
    sql = """ALTER TABLE client ALTER COLUMN creation_date SET NOT NULL"""
    cursor.execute(sql)
    conn.commit()
    sql = """ALTER TABLE client ALTER COLUMN last_update_date SET NOT NULL"""
    cursor.execute(sql)
    conn.commit()
    sql = """ALTER TABLE client ALTER COLUMN "creation_date" SET DEFAULT CURRENT_DATE"""
    cursor.execute(sql)
    conn.commit()
    sql = """ALTER TABLE client ALTER COLUMN "last_update_date" SET DEFAULT CURRENT_DATE"""
    cursor.execute(sql)
    conn.commit()
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
    conn = get_a_database_connection()
    cursor = conn.cursor()
    sql = f"""ALTER DATABASE {settings.DATABASE_NAME} OWNER TO {settings.ADMIN_LOGIN}"""
    cursor.execute(sql)
    conn.commit()

    sql = f"""ALTER USER {settings.ADMIN_LOGIN} WITH PASSWORD '{settings.ADMIN_PASSWORD}'"""
    cursor.execute(sql)
    conn.commit()

    sql = f"""GRANT ALL PRIVILEGES ON DATABASE {settings.DATABASE_NAME} TO {settings.ADMIN_LOGIN}"""
    cursor.execute(sql)
    conn.commit()

    # Environnement de développement, on ré-initialise les ids des "collaborators", "location", etc
    sql = """TRUNCATE TABLE client RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE collaborator RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE collaborator_department RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE collaborator_role RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE event RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE location RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    sql = """TRUNCATE TABLE contract RESTART IDENTITY CASCADE"""
    cursor.execute(sql)
    conn.commit()

    conn.close()
    return True


def dummy_database_creation():
    """
    Description:
    Dédiée à peupler la base de données avec des données fictives
    """
    conn = get_a_database_connection()
    cursor = conn.cursor()

    sql = """INSERT INTO collaborator_department(name) VALUES('COMMERCIAL')"""
    cursor.execute(sql)
    conn.commit()
    sql = """INSERT INTO collaborator_department(name) VALUES('GESTION')"""
    cursor.execute(sql)
    conn.commit()
    sql = """INSERT INTO collaborator_department(name) VALUES('SUPPORT')"""
    cursor.execute(sql)
    conn.commit()
    sql = """INSERT INTO collaborator_role(name) VALUES('MANAGER')"""
    cursor.execute(sql)
    conn.commit()
    sql = """INSERT INTO collaborator_role(name) VALUES('EMPLOYEE')"""
    cursor.execute(sql)
    conn.commit()

    # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('123456789', 'applepie94', 'donald duck', '1', '1')
    """
    cursor.execute(sql)
    conn.commit()
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('234567891', 'applepie94', 'Bill Boquet', '1', '2')
    """
    cursor.execute(sql)
    conn.commit()

    # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('345678912', 'applepie94', 'daisy duck', '2', '1')
    """
    cursor.execute(sql)
    conn.commit()
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('456789123', 'applepie94', 'loulou duck', '2', '2')
    """
    cursor.execute(sql)
    conn.commit()

    # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('567891234', 'applepie94', 'loulou duck', '2', '2')
    """
    cursor.execute(sql)
    conn.commit()
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('678912345', 'applepie94', 'Aliénor Vichum', '3', '2')
    """
    cursor.execute(sql)
    conn.commit()
    sql = """
        INSERT INTO collaborator(registration_number, password, username, departement, role)
        VALUES('789123456', 'applepie94', 'Kate Hastroff', '3', '2')
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
    INSERT INTO client(information, fullname, email, telephone, company_name, commercial_contact)
    VALUES('Exemple bla bla bla', 'Kevin Casey', 'kevin@startup.io', '+678 123 456 78', 'Cool Startup LLC', '2')
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
    INSERT INTO contract(information, full_amount_to_pay, remain_amount_to_pay, status, client_id, collaborator_id)
    VALUES('Memes infos que le client ?', '999.99', '999.99', 'False', '1', '2')
    """
    cursor.execute(sql)
    conn.commit()

    sql = """
    INSERT INTO location(adresse, complement_adresse, code_postal, ville, pays)
    VALUES('53 Rue du Château', '', '41120', 'Candé-sur-Beuvron', 'France')
    """
    cursor.execute(sql)
    conn.commit()

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
