"""
Description:
De l'aide, de l'info pour les commandes. A compléter progressivement.
On insistera avant tout sur une application fonctionnelle et sécurisée, quitte à alimenter l'aide dans un 2ème temps.
"""
import click
from rich import print


@click.command
def help():
    """
    Description: bla bla bla
    """
    print("[bold green][HELP MENU][/bold green]", end="")

    basic_pos_commands = """
oc12_launch_application: [green]initialiser un POC[/green]
oc12_token: [green]obtenir un jeton d'accès[/green]
oc12_logout: [green]se déconnecter de l'application[/green]
oc12_clients: [green]obtenir les clients de l'entreprise[/green]
oc12_collaborators: [green]obtenir les employés /collaborateurs de l'entreprise[/green]
oc12_contracts: [green]obtenir les contrats de l'entreprise[/green]
oc12_events: [green]obtenir les évènements de l'entreprise[/green]
oc12_locations: [green]obtenir les localités des évènements de l'entreprise[/green]
oc12_departments: [green]obtenir les départements /services de l'entreprise[/green]
oc12_roles: [green]obtenir les rôles possibles des employés dans l'entreprise[/green]
oc12_help: [green]obtenir de l'aide (ce menu)[/green]
    """

    print(basic_pos_commands)
