import psycopg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

try:
    from src.settings import settings
    from src.models import models
except ModuleNotFoundError:
    from settings import settings
    from models import models


class DatabaseInitializerController:
    """
    Description: Le nécessaire pour initialiser la connexion à la base de données.
    Noter que dans cet environnement de développement on supprime la bdd existante et on en recrée une toute fraiche.
    """

    def return_engine_and_session(self):
        """
        Description: connexion à la base de données et renvoie le moteur dédié à initialiser les tables.
        Renvoie aussi de la session qui sera utilisée par la vue AppViews.
        """
        try:
            admin_log = settings.ADMIN_LOGIN
            admin_pwd = settings.ADMIN_PASSWORD
            db_name = settings.DATABASE_NAME
            engine = create_engine(
                f"postgresql+psycopg://{admin_log}:{admin_pwd}@localhost/{db_name}"
            )
        except psycopg.OperationalError as error:
            print(f"[bold red][START CONTROL][/bold red] {error}")

        session_maker = sessionmaker(engine)
        session = session_maker()
        return (engine, session)

    def init_db(self, engine):
        """
        Description: Dédié à aider au développement. On détruit et recrée les tables de la base de données.
        """
        base = models.get_base()
        base.metadata.drop_all(engine)
        base.metadata.create_all(engine)
