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
    Description:
    Le nécessaire pour initialiser la connexion à la base de données.
    On va se servir des identifiants de connexion du "role" auquel est rattaché l'utilisateur.
    Pour accéder à cette classe, il a été contrôlé la présence d'un JWT token valide (dans le PATH utilisateur).
    Toutes autres opérations que "lecture seule, GET, etc" imposeront à l'utilisateur de saisir son mot de passe.
    """

    def return_engine_and_session(self, user_login="", user_pwd="", decoded_token=""):
        """
        Description: connexion à la base de données et renvoie le moteur dédié à initialiser les tables.
        Renvoie aussi de la session qui sera utilisée par la vue AppViews.
        """

        try:
            if decoded_token == "":
                # l'utilisateur demande un token, c'est sa "connexion" initiale à l'application
                user_login = user_login
                user_pwd = user_pwd
            else:
                # l'utilisateur vient de demander un token, l'a obtenu et requete la bdd, on exploite le token décodé
                user_login = str(decoded_token["department"]).lower()
                dprt = str(decoded_token["department"]).upper()
                user_pwd = eval(f"settings.{dprt}_PWD")
            db_name = settings.DATABASE_NAME
            engine = create_engine(
                f"postgresql+psycopg://{user_login}:{user_pwd}@localhost/{db_name}"
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
