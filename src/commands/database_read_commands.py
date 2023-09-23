"""
Description:
Toutes les commandes de lecture seule.
"""
import click
from rich import print

try:
    from src.exceptions import exceptions
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.read_console import ConsoleClientForRead
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from exceptions import exceptions
    from printers import printer
    from languages import language_bridge
    from clients.read_console import ConsoleClientForRead
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


class ApplicationHelpFormatter(click.HelpFormatter):
    def __init__(self, **kwargs):
        super().__init__(self, **kwargs)
        self.indent_increment = 4
        self.max_width = None

    def write_heading(self, heading):
        print(f"{heading.strip()}")

    def write_text(self, text):
        print(f"{text.strip()}")

    def write(self, text):
        print(f"{text}")


click.Context.formatter_class = ApplicationHelpFormatter


@click.command
@click.option("--client_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_clients(client_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les clients de l'entreprise.
    En l'absence d'arguments, l'ensemble des clients est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]last_update_date[/bright_white]: on filtre par date de mise à jour.
    [bright_white]client_id[/bright_white]: on filtre par id du client.
    [bright_white]civility[/bright_white]: on filtre par civilité.
    [bright_white]first_name[/bright_white]: on filtre par prénom.
    [bright_white]last_name[/bright_white]: on filtre par nom de famille.
    [bright_white]email[/bright_white]: on filtre par email.
    [bright_white]telephone[/bright_white]: on filtre par telephone.
    [bright_white]company_id[/bright_white]: on filtre par entreprise.
    [bright_white]employee_role[/bright_white]: on filtre par emploi du client.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_clients "creation_date>=19-02-2020"
    oc12_clients "last_update_date<01-01-2021"
    oc12_clients client_id=FJONIC35
    oc12_clients "civility=monsieur"
    oc12_clients first_name=Fred
    oc12_clients last_name=Jones
    oc12_clients email=sammy.rodgers@tmmachine.xe
    oc12_clients telephone=0699248635
    oc12_clients company_id=SCOU3541
    oc12_clients commercial_contact=aa123456789
    oc12_clients "employee_role='Ingénieur cloud computing'"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_clients(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except exceptions.QueryStructureException:
        message = APP_DICT.get_appli_dictionnary()["QUERY_STRUCTURE_FAILURE"]
        printer.print_message("info", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.info(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--collaborator_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_collaborators(collaborator_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les utilisateurs /collaborateurs de l'entreprise.
    En l'absence d'arguments, l'ensemble des collaborateurs est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]registration_number[/bright_white]: on filtre par matricule.
    [bright_white]role_id[/bright_white]: on filtre par rôle du collaborateur.
    [bright_white]department_id[/bright_white]: on filtre par service du collaborateur.
    [bright_white]username[/bright_white]: on filtre par username du collaborateur.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_collaborators "creation_date>=15-10-2022"
    oc12_collaborators registration_number=ac123456789
    oc12_collaborators role_id=emp
    oc12_collaborators department_id=ccial
    oc12_collaborators "username='daisy duck'"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_collaborators(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--company_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_companies(company_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les entreprises clientes.
    En l'absence d'arguments, l'ensemble des entreprises est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]activite_principale[/bright_white]: on filtre par activité principale.
    [bright_white]tranche_effectif_salarie[/bright_white]: on filtre par effectif.
    [bright_white]company_id[/bright_white]: on filtre par id entreprise.
    [bright_white]company_name[/bright_white]: on filtre par nom entreprise.
    [bright_white]company_registration_number[/bright_white]: on filtre par SIREN.
    [bright_white]company_registration_number[/bright_white]: on filtre par NIC.
    [bright_white]location_id[/bright_white]: on filtre par localité.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_companies "creation_date>=15-10-2022"
    oc12_companies "activite_principale=64.19Z"
    oc12_companies "tranche_effectif_salarie>50"
    oc12_companies "company_id=220315SASR"
    oc12_companies "company_name='CROIX ROUGE FRANCAISE'"
    oc12_companies "company_registration_number=662025196"
    oc12_companies "company_subregistration_number=60347"
    oc12_companies "location_id=FRIL75014CRF"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_companies(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--contract_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_contracts(contract_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les contrats de l'entreprise.
    En l'absence d'arguments, l'ensemble des contrats est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]contract_id[/bright_white]: on filtre par id du contrat.
    [bright_white]client_id[/bright_white]: on filtre par id du client.
    [bright_white]collaborator_id[/bright_white]: on filtre par id du collaborateur.
    [bright_white]status[/bright_white]: filtre pour statut. Valeurs possibles: signed, unsigned, canceled
    [bright_white]full_amount_to_pay[/bright_white]: on filtre par montant à payer.
    [bright_white]remain_amount_to_pay[/bright_white]: on filtre par montant restant à payer.
    [bright_white]creation_date[/bright_white]: on filtre par date de création.

    [bold cyan]Usage examples:[/bold cyan]
    [white]oc12_contracts contract_id=ff555[/white]
    [white]oc12_contracts status=signed[/white]
    [white]oc12_contracts collaborator_id=aa123456789[/white]
    [white]oc12_contracts "remain_amount_to_pay>=0"[/white]
    [white]oc12_contracts "status=signed et remain_amount_to_pay>0"[/white]
    [white]oc12_contracts "creation_date>=22-06-2020"[/white]
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_contracts(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--department_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_departments(department_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les départements /services de l'entreprise.
    En l'absence d'arguments, l'ensemble des départements est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]department_id[/bright_white]: on filtre par id department /service.
    [bright_white]department_id[/bright_white]: on filtre par nom department /service.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_departments "creation_date>=22-06-2021"
    oc12_departments "department_id=ccial"
    oc12_departments "name=oc12_support"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_departments(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--event_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_events(event_id, args):
    #     oc12_events "location_id=llb44430"
    # MANQUE 1 EVENT ??!!!
    #
    # oc12_events "client_id=mkc111"
    # renvoit 1 seul résultat
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les évènements organisés par l'entreprise.
    En l'absence d'arguments, l'ensemble des évènements est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]event_start_date[/bright_white]: on filtre par date de début.
    [bright_white]event_end_date[/bright_white]: on filtre par date de fin.
    [bright_white]event_id[/bright_white]: on filtre par evenementt id (le custom id).
    [bright_white]location_id[/bright_white]: on filtre par localité id (le custom id).
    [bright_white]attendees[/bright_white]: on filtre par nombre de personnes attendues.
    [bright_white]client_id[/bright_white]: on filtre par client id (le custom id).
    [bright_white]contract_id[/bright_white]: on filtre par contrat id (le custom id).
    [bright_white]collaborator_id[/bright_white]: on filtre par id pour recherche équipier Support.
    [bright_white]commercial_id[/bright_white]: on filtre par id pour recherche équipier Commercial.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_events "creation_date>15-07-2023"[/white]
    oc12_events "event_start_date>15-07-2023"
    oc12_events "event_end_date>15-07-2023"
    oc12_events "event_id=geg2021"
    oc12_events "location_id=llb44430"
    oc12_events "attendees>50"
    oc12_events "client_id=mkc111"
    oc12_events "collaborator_id=af123456789"
    oc12_events "commercial_id=aa123456789"
    oc12_events "contract_id=av123"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_events(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--location_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_locations(location_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les localités des évènements ou des entreprises.
    En l'absence d'arguments, l'ensemble des localités est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]location_id[/bright_white]: on filtre par id de localité.
    [bright_white]population[/bright_white]: on filtre par population de la localité.
    [bright_white]adresse[/bright_white]: on filtre par adresse de la localité.
    [bright_white]complement_adresse[/bright_white]: on filtre par complement_adresse de la localité.
    [bright_white]ville[/bright_white]: on filtre par ville.
    [bright_white]cedex[/bright_white]: on filtre par cedex de la localité.
    [bright_white]code_postal[/bright_white]: on filtre par code_postal de la localité.
    [bright_white]region[/bright_white]: on filtre par région.
    [bright_white]pays[/bright_white]: on filtre par code_postal de la localité.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_locations "creation_date<15-01-2022"
    oc12_locations "location_id=llb44430"
    oc12_locations "population>1500"
    oc12_locations "adresse='22 DE WAGRAM'"
    oc12_locations "complement_adresse='SITE CROIX ROUGE'"
    oc12_locations "ville='Le Loroux-Bottereau'"
    oc12_locations "cedex=92032"
    oc12_locations "code_postal=75009"
    oc12_locations "region='Centre-Val de Loire'"
    oc12_locations "pays=France"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_locations(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--role_id", prompt=False, help="")
@click.argument(
    "args",
    nargs=-1,
    type=str,
)
def get_roles(role_id, args):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à récupérer les roles des utilisateurs /collaborateurs de l'entreprise.
    En l'absence d'arguments, l'ensemble des roles est renvoyé.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]creation_date[/bright_white]: on filtre par date de création.
    [bright_white]role_id[/bright_white]: on filtre par id du rôle.
    [bright_white]name[/bright_white]: on filtre par nom du rôle.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_roles "creation_date>15-10-2022"
    oc12_roles "role_id=man"
    oc12_roles "name=MANAGER"
    """
    user_query_filters_args = args
    try:
        console_client = ConsoleClientForRead()
        console_client.get_roles(user_query_filters_args)
    except exceptions.QueryFailureException:
        pass
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
