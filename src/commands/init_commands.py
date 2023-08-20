"""
Description: Commandes dédiées au démarrage de l'application
"""
import os
import sys
import subprocess
import maskpass
import click
from rich import print

try:
    from src.clients import init_console
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.admin_console import AdminConsoleClient
    from src.external_datas.make_dummy_database_creation_command import dummy_database_creation
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from clients import init_console
    from printers import printer
    from languages import language_bridge
    from clients.admin_console import AdminConsoleClient
    from external_datas.make_dummy_database_creation_command import dummy_database_creation
    from settings import settings
    from utils import utils


APP_DICT = language_bridge.LanguageBridge()
FILENAME = f"src/languages/{settings.DEFAULT_COUNTRY_SHORT}/application_dictionnary.json"

@click.command
def init_application():
    """
    Description:
    Commande dédiée à (ré)initialiser la base de données, en vue de pouvoir utiliser l'application.
    """
    try:
        if os.path.isfile(FILENAME):
            os.remove(FILENAME)
    except FileNotFoundError:
        # si le fichier de "messages" json est absent, ce n'est pas un problème, il va être recrée.
        pass
    app_dict = language_bridge.LanguageBridge()

    for db_name in settings.DATABASE_TO_CREATE:
        client_view_console = init_console.InitAppliConsole(db_name=db_name)

    utils.display_banner(app_init=True)
    print("Initialization authentication ", end="")
    printer.print_message("info", APP_DICT.get_appli_dictionnary()['ASK_FOR_ADMIN_PASSWORD'])
    print("Admin - ", end="")
    admin_pwd = maskpass.askpass()
    if not admin_pwd == f"{settings.ADMIN_PASSWORD}":
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['INVALID_ADMIN_CREDENTIALS_ERROR'])
        sys.exit(0)

    print("Initialization authentication ", end="")
    printer.print_message("info", APP_DICT.get_appli_dictionnary()['ASK_FOR_SUDO_PASSWORD'])

    print("Initialization application ", end="")
    printer.print_message("info", APP_DICT.get_appli_dictionnary()['APPLICATION_INITIALISATION'])
    for database in settings.DATABASE_TO_CREATE:
        try:
            subprocess.run(
                [f"sudo -u postgres dropdb {database}"],
                shell=True,
                check=True,
                capture_output=True,
            )

            print(f"Database {database} ",end="")
            printer.print_message("success", APP_DICT.get_appli_dictionnary()['DATABASE_DROPPED_SUCCESS'])
        except subprocess.CalledProcessError:
            print(f"Database {database} ",end="")
            printer.print_message("error", APP_DICT.get_appli_dictionnary()['DATABASE_DROPPED_FAILURE'])
        except KeyboardInterrupt:
            printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
            sys.exit(0)

    # on ne supprime qu'une fois le Account admin
    try:
        subprocess.run(
            [f"sudo -u postgres dropuser {settings.ADMIN_LOGIN}"],
            shell=True,
            check=True,
            capture_output=True,
        )
        print(f"Account {settings.ADMIN_LOGIN} ",end="")
        printer.print_message("success", APP_DICT.get_appli_dictionnary()['COLLABORATOR_DROPPED_SUCCESS'])
    except subprocess.CalledProcessError:
        print(f"Database {database} {settings.ADMIN_LOGIN} ",end="")
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['COLLABORATOR_DROPPED_FAILURE'])
    except KeyboardInterrupt:
        printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
        sys.exit(0)

    try:
        subprocess.run(
            [f"sudo -u postgres createuser -s -i -d -r -l -w {settings.ADMIN_LOGIN}"],
            shell=True,
            check=True,
            capture_output=True,
        )

        subprocess.run(
            [
                f"sudo -u postgres psql -c \"ALTER ROLE admin WITH PASSWORD '{settings.ADMIN_PASSWORD}';\""
            ],
            shell=True,
            check=True,
            capture_output=True,
        )
        print(f"Account {settings.ADMIN_LOGIN} ",end="")
        printer.print_message("success", APP_DICT.get_appli_dictionnary()['COLLABORATOR_CREATED_SUCCESS'])
    except subprocess.CalledProcessError:
        print(f"Database {database} {settings.ADMIN_LOGIN} ",end="")
        printer.print_message("info", APP_DICT.get_appli_dictionnary()['USER_ALREADY_EXIST'])
    except KeyboardInterrupt:
        printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
        sys.exit(0)

    for database in settings.DATABASE_TO_CREATE:
        try:
            subprocess.run(
                [f"sudo -u postgres createdb '{database}'"],
                shell=True,
                check=True,
                capture_output=True,
            )
        except subprocess.CalledProcessError:
            print(f"Database {database} {settings.ADMIN_LOGIN} ",end="")
            printer.print_message("info", APP_DICT.get_appli_dictionnary()['DATABASE_ALREADY_EXIST'])

        except KeyboardInterrupt:
            printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
            sys.exit(0)

        try:
            os.system(
                f"sudo su -c 'psql -c \"ALTER DATABASE {database} OWNER TO admin\"' postgres 1>/dev/null"
            )
            print(f"Database {database} ",end="")
            printer.print_message("success", APP_DICT.get_appli_dictionnary()['DATABASE_OWNER_UPDATE_SUCCESS'])
        except subprocess.CalledProcessError:
            print(f"Database {database} ",end="")
            printer.print_message("error", APP_DICT.get_appli_dictionnary()['DATABASE_OWNER_UPDATE_FAILURE'])
        except KeyboardInterrupt:
            printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
            sys.exit(0)

    for database in settings.DATABASE_TO_CREATE:
        print(f"Database {database} ",end="")
        printer.print_message("info", APP_DICT.get_appli_dictionnary()['DATABASE_UPDATING'])
        if database == "projet12":
            admin_console_client = AdminConsoleClient()
            admin_console_client.reset_db(db_name=f"{database}")
            admin_console_client.init_db()
            utils.display_postgresql_controls()
            admin_console_client.database_postinstall_tasks()
            admin_console_client.database_postinstall_alter_tables()
        else:
            admin_console_client = AdminConsoleClient(db_name=f"{database}")
            admin_console_client.reset_db(db_name=f"{database}")
            admin_console_client.init_db(db_name=f"{database}")
            admin_console_client.database_postinstall_tasks(
                db_name=f"{database}"
            )
            admin_console_client.database_postinstall_alter_tables(
                db_name=f"{database}"
            )

    # On peuple la base de données avec des données quelconques, pour le POC, en développement
    dummy_database_creation(db_name=f"dev_projet12")
    dummy_database_creation(db_name=f"test_projet12")

    # on insère en base un jeu de données supplémentaires. On interroge des API externes.
    # le résultat d'une requete à ces API est un fichier .csv
    # exemple usage fourni, est d'obtenir un fichier 'src/external_datas/csv/french_companies.csv'
    # Si accès internet désactivé (voir 'settings.INTERNET_CONNECTION') le code recherche le fichier csvfile
    # Si le fichier existe et n'est pas vide, alors l'insertion s'effectue aussi
    client_view_console.import_data_from_externals_api()
