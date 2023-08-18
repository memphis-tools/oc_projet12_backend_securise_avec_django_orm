"""
Description:
On isole la fonctionnalité dédiée à afficher à l'utilisateur un message lors d'une exception.
Le printer est utilisée par les "consoles clients"
"""
from rich import print


def print_message(message_type, message_content):
    """
    Description:
    Fonction dédiée à afficher des messages en cas d'exception.
    Paramètres:
    - message_type: chaine de caractères, attendues: debug, error, info
    - message_content: chaine de caractères
    """
    message_colors_dict = {
        "debug": "yellow",
        "error": "red",
        "info": "cyan",
        "success": "green",
    }
    prelude = f"[bold {message_colors_dict[message_type]}]"
    title = message_type
    postlude = f"[/bold {message_colors_dict[message_type]}]"
    print(f"{prelude}{title}{postlude} {message_content}")
