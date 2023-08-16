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
    from src.clients.admin_console import AdminConsoleClient
    from src.commands.dummy_database_creation_command import dummy_database_creation
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from clients.admin_console import AdminConsoleClient
    from commands.dummy_database_creation_command import dummy_database_creation
    from settings import settings
    from utils import utils


@click.command
def init_application():
    """
    Description:
    Commande dédiée à (ré)initialiser la base de données, en vue de pouvoir utiliser l'application.
    """

    utils.display_banner()
    print(
        "[bold blue][START CONTROL][/bold blue] First supply the application admin password."
    )
    print("Admin - ", end="")
    admin_pwd = maskpass.askpass()
    if not admin_pwd == f"{settings.ADMIN_PASSWORD}":
        raise Exception("[bold red]Wrong credentials[/bold red]")

    print(
        "[bold blue][START CONTROL][/bold blue] Next you may have to type your password to run sudo commands"
    )

    for database in settings.DATABASE_TO_CREATE:
        try:
            subprocess.run(
                [f"sudo -u postgres dropdb {database}"],
                shell=True,
                check=True,
                capture_output=True,
            )
            print(
                f"[bold green][START CONTROL][/bold green] Database {database} droped"
            )
        except subprocess.CalledProcessError:
            print(
                f"[bold red][START CONTROL][/bold red] Can not drop database {database}, it does not exist"
            )
        except KeyboardInterrupt:
            print("[bold green][START CONTROL][/bold green] Launch application aborted")
            sys.exit(0)

        try:
            subprocess.run(
                [f"sudo -u postgres dropuser {database}"],
                shell=True,
                check=True,
                capture_output=True,
            )
            print(
                f"[bold green][START CONTROL][/bold green] Collaborator {database} droped"
            )
        except subprocess.CalledProcessError:
            print(
                f"[bold red][START CONTROL][/bold red] Can not drop user {database}, he does not exist"
            )
        except KeyboardInterrupt:
            print(
                "[bold green][START CONTROL][/bold green] Application startup aborted"
            )
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
        print(
            f"[bold green][START CONTROL][/bold green] user '{settings.ADMIN_LOGIN}' already exists"
        )
    except KeyboardInterrupt:
        print("[bold green][START CONTROL][/bold green] Application startup aborted")
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
            print(
                f"[bold green][START CONTROL][/bold green] database '{database}' already exists"
            )
        except KeyboardInterrupt:
            print(
                "[bold green][START CONTROL][/bold green] Application startup aborted"
            )
            sys.exit(0)

        try:
            os.system(
                "sudo su -c 'psql -c \"ALTER DATABASE projet12 OWNER TO admin\"' postgres"
            )
            print(
                f"[bold green][START CONTROL][/bold green] {database} owner is now {settings.ADMIN_LOGIN}"
            )
        except subprocess.CalledProcessError:
            print(
                f"[bold red][START CONTROL][/bold red] Can not ALTER {database} owner"
            )
        except KeyboardInterrupt:
            print(
                "[bold green][START CONTROL][/bold green] Application startup aborted"
            )
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
