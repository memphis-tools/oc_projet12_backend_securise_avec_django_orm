"""
Description:
Toutes les commandes qui permettent les suppressions
"""
import click

try:
    from src.printers import printer
    from src.languages import language_bridge
    from src.clients.delete_console import ConsoleClientForDelete
    from src.exceptions import exceptions
    from src.settings import settings, logtail_handler
except ModuleNotFoundError:
    from printers import printer
    from languages import language_bridge
    from clients.delete_console import ConsoleClientForDelete
    from exceptions import exceptions
    from settings import settings, logtail_handler


APP_DICT = language_bridge.LanguageBridge()
LOGGER = logtail_handler.logger


@click.command
@click.option("--client_id", prompt=True, help="")
def delete_client(client_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un client de l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]client_id[/bright_white]: id du client.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_client --client_id=mkc111
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_client(client_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()[
            "FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--collaborator_id", prompt=True, help="")
def delete_collaborator(collaborator_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un utilisateur /collaborateur de l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]collaborator_id[/bright_white]: id du collaborateur.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_collaborator --collaborator_id=aa123456789
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_collaborator(collaborator_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        pass
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--company_id", prompt=True, help="")
def delete_company(company_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer une entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]company_id[/bright_white]: id de l'entreprise.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_company --company_id=666217CHCGF
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_company(company_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()[
            "FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--contract_id", prompt=True, help="")
def delete_contract(contract_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un contrat de l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]contract_id[/bright_white]: id du contrat.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_contract --contract_id=xx55555
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_contract(contract_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        pass
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--department_id", prompt=True, help="")
def delete_department(department_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un département /service de l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]department_id[/bright_white]: id du département /service.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_department --department_id=dev
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_department(department_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()[
            "FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--event_id", prompt=True, help="")
def delete_event(event_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un évènement organisé par l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]event_id[/bright_white]: id de l'évènement.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_event --event_id=dkap520
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_event(event_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()[
            "FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--location_id", prompt=True, help="")
def delete_location(location_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer une localité.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]location_id[/bright_white]: id de la localité.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_location --location_id=FRIL94150L
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_location(location_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()["LOCATION_RATTACHED_TO_COMPANY"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)


@click.command
@click.option("--role_id", prompt=True, help="")
def delete_role(role_id):
    """
    [bold cyan]Description:[/bold cyan]

    Dédiée à supprimer un roles pour les utilisateurs /collaborateurs de l'entreprise.

    [bold cyan]Arguments:[/bold cyan]
    [bright_white]role_id[/bright_white]: id du role.

    [bold cyan]Usage examples:[/bold cyan]
    oc12_delete_role --role_id=man
    """
    console = ConsoleClientForDelete()
    try:
        console_client_return = console.delete_role(role_id)
        click.secho(console_client_return, bg="blue", fg="white")
    except exceptions.MissingUpdateParamException:
        message = APP_DICT.get_appli_dictionnary()["MISSING_PARAMETER"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.ForeignKeyDependyException:
        message = APP_DICT.get_appli_dictionnary()[
            "FOREIGNKEY_CONTRACT_CAN_NOT_BE_DROP"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.InsufficientPrivilegeException:
        message = APP_DICT.get_appli_dictionnary()["INSUFFICIENT_PRIVILEGES_EXCEPTION"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CommercialCollaboratorIsNotAssignedToContract:
        message = APP_DICT.get_appli_dictionnary()[
            "COMMERCIAL_COLLABORATOR_IS_NOT_ASSIGNED_TO_CONTRACT"
        ]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except exceptions.CustomIdMatchNothingException:
        message = APP_DICT.get_appli_dictionnary()["CUSTOM_ID_MATCHES_NOTHING"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
    except Exception:
        message = APP_DICT.get_appli_dictionnary()["MISSING_TOKEN_ERROR"]
        printer.print_message("error", message)
        if settings.INTERNET_CONNECTION and settings.LOG_COLLECT_ACTIVATED:
            LOGGER.error(message)
