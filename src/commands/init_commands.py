"""
Description: Commandes dédiées au démarrage de l'application
"""
import subprocess
import sys
import click
from rich import print

try:
    from src.clients.console import ConsoleClient
    from src.settings import settings
    from src.utils import utils
except ModuleNotFoundError:
    from clients.console import ConsoleClient
    from settings import settings
    from utils import utils


@click.command
def launch_application():
    """
    Description: commande dédiée à démarrer l'application.
    Application en cours de développement, on redémarre l'appli de zéro par défaut.
    """
    print(
        "[bold blue][START CONTROL][/bold blue] You may be first asked for your password in order to run sudo commands"
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
            [
                f"sudo -u postgres createuser '{settings.ADMIN_LOGIN}' --superuser --pwprompt"
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

    console_client = ConsoleClient()
    console_client.init_db()

    utils.display_postgresql_controls()
    utils.database_postinstall_tasks()
    utils.database_postinstall_alter_tables()

    # On peuple la base de données avec des données quelconques, pour le POC, en développement
    utils.dummy_database_creation()
