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
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.admin_console import AdminConsoleClient
    from src.commands.dummy_database_creation_command import dummy_database_creation
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.admin_console import AdminConsoleClient
    from commands.dummy_database_creation_command import dummy_database_creation
    from settings import settings
    from utils import utils


APP_DICT = language_bridge.LanguageBridge()


@click.command
def init_application():
    """
    Description:
    Commande dédiée à (ré)initialiser la base de données, en vue de pouvoir utiliser l'application.
    """

    app_dict = language_bridge.LanguageBridge()
    # On génère le fichier de messages dans le langage attendu par l'administrateur
    app_dict.generate_env_messages()

    utils.display_banner()
    printer.print_message("info", APP_DICT.get_appli_dictionnary()['ASK_FOR_ADMIN_PASSWORD'])
    print("Admin - ", end="")
    admin_pwd = maskpass.askpass()
    if not admin_pwd == f"{settings.ADMIN_PASSWORD}":
        printer.print_message("error", APP_DICT.get_appli_dictionnary()['INVALID_ADMIN_CREDENTIALS_ERROR'])
        sys.exit(0)

    printer.print_message("info", APP_DICT.get_appli_dictionnary()['ASK_FOR_SUDO_PASSWORD'])

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

        try:
            subprocess.run(
                [f"sudo -u postgres dropuser {database}"],
                shell=True,
                check=True,
                capture_output=True,
            )
            print(f"Database {database} ",end="")
            printer.print_message("success", APP_DICT.get_appli_dictionnary()['COLLABORATOR_DROPPED_SUCCESS'])
        except subprocess.CalledProcessError:
            print(f"Database {database} ",end="")
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
                "sudo su -c 'psql -c \"ALTER DATABASE projet12 OWNER TO admin\"' postgres"
            )
            print(f"Database {database}{settings.ADMIN_LOGIN} ",end="")
            printer.print_message("success", APP_DICT.get_appli_dictionnary()['DATABASE_OWNER_UPDATE_SUCCESS'])
        except subprocess.CalledProcessError:
            print(f"Database {database}{settings.ADMIN_LOGIN} ",end="")
            printer.print_message("error", APP_DICT.get_appli_dictionnary()['DATABASE_OWNER_UPDATE_FAILURE'])
        except KeyboardInterrupt:
            printer.print_message("info", APP_DICT.get_appli_dictionnary()['INIT_ABORTED'])
            sys.exit(0)

    admin_console_client = AdminConsoleClient()
    admin_console_client.init_db()
    utils.display_postgresql_controls()
    admin_console_client.database_postinstall_tasks()
    admin_console_client.database_postinstall_alter_tables()
    admin_console_client = AdminConsoleClient(db_name=f"{settings.TEST_DATABASE_NAME}")
    admin_console_client.reset_db(db_name=f"{settings.TEST_DATABASE_NAME}")
    admin_console_client.init_db(db_name=f"{settings.TEST_DATABASE_NAME}")
    admin_console_client.database_postinstall_tasks(
        db_name=f"{settings.TEST_DATABASE_NAME}"
    )
    admin_console_client.database_postinstall_alter_tables(
        db_name=f"{settings.TEST_DATABASE_NAME}"
    )

    # On peuple la base de données avec des données quelconques, pour le POC, en développement
    dummy_database_creation(db_name=f"{settings.TEST_DATABASE_NAME}")
