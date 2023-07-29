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
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from clients.admin_console import AdminConsoleClient
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
    try:
        subprocess.run(
            [f"sudo -u postgres dropdb {settings.DATABASE_NAME}"],
            shell=True,
            check=True,
            capture_output=True,
        )
        print(
            f"[bold green][START CONTROL][/bold green] Database {settings.DATABASE_NAME} droped"
        )
    except subprocess.CalledProcessError:
        print(
            f"[bold red][START CONTROL][/bold red] Can not drop database {settings.DATABASE_NAME}, it does not exist"
        )
    except KeyboardInterrupt:
        print("[bold green][START CONTROL][/bold green] Launch application aborted")
        sys.exit(0)

    try:
        subprocess.run(
            [f"sudo -u postgres dropuser {settings.ADMIN_LOGIN}"],
            shell=True,
            check=True,
            capture_output=True,
        )
        print(
            f"[bold green][START CONTROL][/bold green] User {settings.ADMIN_LOGIN} droped"
        )
    except subprocess.CalledProcessError:
        print(
            f"[bold red][START CONTROL][/bold red] Can not drop user {settings.ADMIN_LOGIN}, he does not exist"
        )
    except KeyboardInterrupt:
        print("[bold green][START CONTROL][/bold green] Application startup aborted")
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

    try:
        subprocess.run(
            [f"sudo -u postgres createdb '{settings.DATABASE_NAME}'"],
            shell=True,
            check=True,
            capture_output=True,
        )
    except subprocess.CalledProcessError:
        print(
            f"[bold green][START CONTROL][/bold green] database '{settings.DATABASE_NAME}' already exists"
        )
    except KeyboardInterrupt:
        print("[bold green][START CONTROL][/bold green] Application startup aborted")
        sys.exit(0)

    try:
        os.system(
            "sudo su -c 'psql -c \"ALTER DATABASE projet12 OWNER TO admin\"' postgres"
        )
        print(
            f"[bold green][START CONTROL][/bold green] {settings.DATABASE_NAME} owner is now {settings.ADMIN_LOGIN}"
        )
    except subprocess.CalledProcessError:
        print(
            f"[bold red][START CONTROL][/bold red] Can not ALTER {settings.DATABASE_NAME} owner"
        )
    except KeyboardInterrupt:
        print("[bold green][START CONTROL][/bold green] Application startup aborted")
        sys.exit(0)

    admin_console_client = AdminConsoleClient()
    admin_console_client.init_db()
    utils.display_postgresql_controls()
    utils.database_postinstall_tasks()
    utils.database_postinstall_alter_tables()

    # On peuple la base de données avec des données quelconques, pour le POC, en développement
    utils.dummy_database_creation()
