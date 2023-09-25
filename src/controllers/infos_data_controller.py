"""
Description:
Fonctions dédiés aux menus d'aide pour saisie
"""
import csv
from tkinter import Tk, Text, INSERT, Button, S


def get_infos_data(file_basename):
    """
    Description:
    Sert à lire un fichier .csv avec plsueirs enregistrements mono-colonnes.
    Fichiers sont par défaut ceux en Français: src/validators/references/fr/*.csv
    Paramètres:
    - file_basename: le nom du fichier .csv à exploiter
    """
    ml = []
    with open(f"src/validators/references/fr/{file_basename}.csv", "r") as file:
        csvreader = csv.reader(file)
        csv_list = []
        for elem in csvreader:
            csv_list.append(elem[0])
        csv_list.pop(0)
    return csv_list


def display_info_data_medium_window(element):
    """
    Description:
    Usage depuis src/clients/info_console.py.
    Sert à présenter, sous forme de popup large, les saisies possibles à produire.
    """
    items = get_infos_data(element)
    items.sort()
    popup = Tk()
    popup.geometry("550x500")
    popup.title("METIERS ATTENDUS POUR CLIENTS")
    text = Text(popup, background="cyan", font=("consolas", 10))
    for item in items:
        text.insert(INSERT, f"{item}\n")
        text.pack()
    Button(popup, text="fermer", command=popup.destroy).place(
        relx=0.5, rely=1.0, anchor=S
    )
    popup.mainloop()


def display_info_data_thin_window(element):
    """
    Description:
    Usage depuis src/clients/info_console.py.
    Sert à présenter, sous forme de popup étroite, les saisies possibles à produire.
    """
    items = get_infos_data(element)
    items.sort()
    popup = Tk()
    popup.geometry("350x500")
    popup.title("TYPES VOIES ATTENDUS")
    text = Text(popup, background="cyan", font=("consolas", 10))
    for item in items:
        text.insert(INSERT, f"{item}\n")
        text.pack()
    Button(popup, text="fermer", command=popup.destroy).place(
        relx=0.5, rely=1.0, anchor=S
    )
    popup.mainloop()
