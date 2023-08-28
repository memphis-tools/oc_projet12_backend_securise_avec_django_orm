"""
Description:
Une fonction pour peupler la base de données avec des données de DEV
"""
from datetime import datetime
try:
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from settings import settings
    from utils import utils


def dummy_database_creation(db_name="projet12"):
    """
    Description:
    Dédiée à peupler la base de données avec des données fictives
    """
    conn = utils.get_a_database_connection(
        f"{settings.ADMIN_LOGIN}",
        f"{settings.ADMIN_PASSWORD}",
        app_init=True,
        db_name=db_name,
    )
    cursor = conn.cursor()

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('ccial', 'oc12_commercial', '2022-07-31 11:34:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('gest', 'oc12_gestion', '2022-08-01 16:35:38')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('supp', 'oc12_support', '2022-08-02 11:45:02')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_department(department_id, name, creation_date)
        VALUES('dev', 'oc12_developer', '2021-02-18 17:34:27')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_role(role_id, name, creation_date)
        VALUES('man', 'MANAGER', '2022-08-03 08:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator_role(role_id, name, creation_date)
        VALUES('emp', 'EMPLOYEE', '2022-08-03 15:24:18')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe COMMERCIAL, dont 1 nommé dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('aa123456789', 'donald duck', '1', '1', '2022-08-03 07:35:23')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ab123456789', 'Bill Boquet', '1', '2', '2022-08-03 08:35:58')
    """
    cursor.execute(sql)

    # 2 membres de l'équipe GESTION, pas d'exemples dans cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ac123456789', 'daisy duck', '2', '1', '2022-08-03 08:36:15')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ad123456789', 'loulou duck', '2', '2', '2022-08-03 08:37:34')
    """
    cursor.execute(sql)

    # 3 membres de l'équipe SUPPORT, dont 2 nommés dans les exemples du cahier des charges
    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ae123456789', 'louloute duck', '3', '2', '2022-08-03 08:39:38')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('af123456789', 'Aliénor Vichum', '3', '2', '2022-08-03 08:35:14')
    """
    cursor.execute(sql)

    sql = """
        INSERT INTO collaborator(registration_number, username, department_id, role_id, creation_date)
        VALUES('ag123456789', 'Kate Hastroff', '3', '2', '2022-08-03 10:22:44')
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
                sql = (
                    f"""CREATE ROLE {user[0]} CREATEROLE LOGIN PASSWORD '{password}'"""
                )
                cursor.execute(sql)
            else:
                sql = f"""CREATE ROLE {user[0]} LOGIN PASSWORD '{password}'"""
                cursor.execute(sql)
            sql = f"""GRANT {user[1]} TO {user[0]}"""
            cursor.execute(sql)
            conn.commit()
        except Exception:
            continue

    # 3 localisations en exemple pour 3 entreprises
    sql = """
    INSERT INTO location
    (location_id, adresse, complement_adresse, code_postal, ville, region, pays, creation_date)
    VALUES
    (
    'p22240',
    '9 av Jean Moulin',
    '2 Bourg de la reine',
    '22240',
    'Plurien',
    'Bretagne',
    'France',
    '2022-01-03 08:35:14'
    )
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO location
    (location_id, adresse, complement_adresse, code_postal, ville, region, pays, creation_date)
    VALUES
    ('llb44430', 'Place de Bretagne', '', '44430', 'Le Loroux-Bottereau',
    'Pays de la Loire', 'France', '2019-07-09 14:08:10')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO location
    (location_id, adresse, complement_adresse, code_postal, ville, region, pays, creation_date)
    VALUES
    (
    'PARRV751',
    'Place de la Nation',
    'Rue du rendez-vous',
    '75011',
    'Paris',
    'Ile de France',
    'France',
    '2020-01-19 15:42:30'
    )
    """
    cursor.execute(sql)

    # 3 entreprises en exemple
    sql = """
    INSERT INTO company
    (company_id, company_name, tranche_effectif_salarie, company_registration_number,
     company_subregistration_number, location_id, creation_date, date_debut_activite)
    VALUES
    (
    'CSLLC12345',
    'Cool Startup LLC',
    '+50',
    '999222888',
    '12345',
    '1',
    '2023-08-03 08:35:14',
    '2023-02-14 15:34:58'
    )
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO company
    (company_id, company_name, tranche_effectif_salarie, company_registration_number,
     company_subregistration_number, location_id, creation_date, date_debut_activite)
    VALUES
    ('NFEPG12345', 'Nantes Free Escape Games', '-50', '999333888', '44888', '2',
    '2019-07-09 14:10:20', '2019-03-25 10:24:08')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO company
    (company_id, company_name, tranche_effectif_salarie, company_registration_number,
     company_subregistration_number, location_id, creation_date, date_debut_activite)
    VALUES ('SCOU3541', 'The Mystery Machine', '-10', '999686686', '86868', '2',
    '2021-09-12 10:15:32', '2021-12-25 20:44:03')
    """
    cursor.execute(sql)

    # 6 clients en exemples
    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('mkc111', 'MR', 'Kevin', 'Casey', 'Assistant',
    'kevin@startup.io', '067812345678', '1', '2', '2021-12-25 19:40:06', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('axs40', 'MLE', 'Alexia', 'Strak', 'Assistante',
     'a.strak@startup.io', '067812345678', '2', '2', '2020-10-15 16:12:20', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('SRODAP37', 'MR', 'Sammy', 'Rodgers', 'Assistant',
     'sammy.rodgers@tmmachine.xe', '0615684937', '3', '1', '2020-02-19 12:10:40', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('FJONIC35', 'MR', 'Fred', 'Jones', 'Ingénieur cloud computing',
     'fred.jones@tmmachine.xe', '0699248635', '3', '2', '2020-02-19 12:10:40', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('DBLATT85', 'MLE', 'Daphné', 'Blake', 'Ingénieur cloud computing',
     'daphné.blake@tmmachine.xe', '0671426385', '3', '1', '2020-02-19 12:10:40', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO client
    (client_id, civility, first_name, last_name, employee_role, email,
     telephone, company_id, commercial_contact, creation_date, last_update_date)
    VALUES
    ('VDINPR25', 'MLE', 'Velma', 'Dinkley', 'Présentatrice radio',
     'velma.dinkley@tmmachine.xe', '0695368525', '3', '2', '2020-02-19 12:10:40', '2021-12-25 19:40:06')
    """
    cursor.execute(sql)

    # 7 contrats en exemples
    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES('kc555', '999.99', '999.99', 'unsigned', '1', '2023-06-03 08:35:25')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES('ff555', '444.55', '20.99', 'signed', '1', '2022-01-16 10:40:14')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES('zz123', '72.5', '0', 'signed', '2','2021-04-15 14:40:14')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES
    ('av123', '155.60', '0', 'signed', '3','2020-06-02 10:40:14')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES
    ('aw231', '255.60', '0', 'signed', '4','2020-06-22 11:40:14')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES
    ('ax312', '355.60', '0', 'signed', '5', '2020-07-12 12:00:00')
    """
    cursor.execute(sql)

    sql = """
    INSERT INTO contract
    (contract_id, full_amount_to_pay, remain_amount_to_pay, status,
    client_id, creation_date)
    VALUES
    ('ay312', '455.60', '0', 'signed', '6', '2020-07-22 16:30:00')
    """
    cursor.execute(sql)

    # 2 localisations en exemple supplémentaires les 2 premiers évènements ci-dessous
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville,
    region, pays, creation_date)
    VALUES
    ('csb41120', '53 av. Bobet', 'Petite Avenue', '41120', 'Candé-sur-Beuvron',
    'Centre-Val de Loire', 'France', '2023-08-03 08:35:14')
    """
    cursor.execute(sql)
    sql = """
    INSERT INTO location(location_id, adresse, complement_adresse, code_postal, ville,
    region, pays, creation_date)
    VALUES
    ('ggg56110', '20 Rue de Carhaix', 'Résidence Coquelicot', '56110', 'Gourin',
    'Bretagne', 'France', '2023-08-03 08:35:14')
    """
    cursor.execute(sql)

    # 7 évènements en exemple
    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'hob2023',
        '{datetime.now()}',
        'Holiday on beach',
        '1',
        '1',
        '2023-07-25 16:00',
        '2023-07-25 22:00',
        '2',
        '500',
        'bla bla bla penser au catering',
        '5'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'geg2022',
        '{datetime.now()}',
        'Gourin escape game 2022',
        '2',
        '1',
        '2022-07-25 16:00',
        '2022-07-25 22:00',
        '2',
        '35',
        'bla bla bla penser à tout le nécessaire. Ne pas oublier de gâteaux à la crème.',
        '6'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes
    )
    VALUES(
        'geg2021',
        '{datetime.now()}',
        'Gourin escape game 2021',
        '3',
        '2',
        '2021-07-25 16:00',
        '2021-07-25 22:00',
        '2',
        '35',
        'bla bla bla penser à tout le nécessaire. Ne pas oublier de gâteaux à la crème.'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'evav123',
        '{datetime.now()}',
        'Summer Bootstrap',
        '4',
        '3',
        '2020-08-09 16:00',
        '2020-08-09 22:00',
        '3',
        '100',
        'bla bla bla penser à la musique.',
        '7'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'zawx235',
        '{datetime.now()}',
        'Summer Javascript',
        '5',
        '4',
        '2020-08-15 17:00',
        '2020-08-15 23:00',
        '3',
        '150',
        'bla bla bla penser à la corbeille de fruits.',
        '6'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'dkap520',
        '{datetime.now()}',
        'Summer OWASP',
        '6',
        '5',
        '2021-05-23 09:00',
        '2021-05-24 23:00',
        '3',
        '50',
        'bla bla bla penser aux équipements supplémentaires non prévus (ou couverts).',
        '7'
    )
    """
    cursor.execute(sql)

    sql = f"""
    INSERT INTO event(
        event_id,
        creation_date,
        title,
        contract_id,
        client_id,
        event_start_date,
        event_end_date,
        location_id,
        attendees,
        notes,
        collaborator_id
    )
    VALUES(
        'ay322',
        '{datetime.now()}',
        'Summer Python',
        '7',
        '6',
        '2022-07-23 09:00',
        '2022-07-23 23:00',
        '3',
        '100',
        'bla bla bla penser aux thermos.',
        '7'
    )
    """
    cursor.execute(sql)

    conn.commit()
    conn.close()
