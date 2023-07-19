import subprocess
import sys
import click
from rich import print

try:
    from src.settings import settings
    from src.controllers.initializer_controller import DatabaseInitializerController
    from src.controllers.get_controllers import DatabaseGETController
    from src.views.views import AppViews
    from src.utils import utils
except ModuleNotFoundError:
    from settings import settings
    from controllers.initializer_controller import DatabaseInitializerController
    from controllers.get_controllers import DatabaseGETController
    from views.views import AppViews
    from utils import utils


class ConsoleClient:
    """
    Description: La classe dédiée à l'usage d'un client en mode console.
    """

    def __init__(self):
        self.db_controller = DatabaseGETController()
        self.db_initializer = DatabaseInitializerController()
        self.app_view = AppViews(self.db_controller, self.db_initializer)

    def init_db(self):
        """
        Description: vue dédiée à instancier la base de données et la vue qui permettra d'utiliser l'application.
        """
        self.app_view.init_db()

    def get_clients(self):
        """
        Description: vue dédiée à obtenir les clients de l'entreprise.
        """
        return self.app_view.get_clients()

    def get_collaborators(self):
        """
        Description: vue dédiée à obtenir les utilisateurs /collaborateurs de l'entreprise.
        """
        return self.app_view.get_collaborators()

    def get_contracts(self):
        """
        Description: vue dédiée à obtenir les contrats de l'entreprise.
        """
        return self.app_view.get_contracts()

    def get_departments(self):
        """
        Description: vue dédiée à obtenir les départements /services de l'entreprise.
        """
        return self.app_view.get_departments()

    def get_events(self):
        """
        Description: vue dédiée à obtenir les évènements de l'entreprise.
        """
        return self.app_view.get_events()

    def get_locations(self):
        """
        Description: vue dédiée à obtenir les localisations des évènements de l'entreprise.
        """
        return self.app_view.get_locations()

    def get_roles(self):
        """
        Description: vue dédiée à obtenir les rôles prévus pour les collaborateurs de l'entreprise.
        """
        return self.app_view.get_roles()


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


@click.command
def get_clients():
    """
    Description: commande dédiée à récupérer les clients de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_clients())


@click.command
def get_collaborators():
    """
    Description: commande dédiée à récupérer les utilisateurs /collaborateurs de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_collaborators())


@click.command
def get_contracts():
    """
    Description: commande dédiée à récupérer les contrats de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_contracts())


@click.command
def get_departments():
    """
    Description: commande dédiée à récupérer les départements /services de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_departments())


@click.command
def get_events():
    """
    Description: commande dédiée à récupérer les évènements organisés par l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_events())


@click.command
def get_locations():
    """
    Description: commande dédiée à récupérer les localisations des évènements.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_locations())


@click.command
def get_roles():
    """
    Description: commande dédiée à récupérer les roles des utilisateurs /collaborateurs de l'entreprise.
    """
    console_client = ConsoleClient()
    print(console_client.app_view.get_roles())
