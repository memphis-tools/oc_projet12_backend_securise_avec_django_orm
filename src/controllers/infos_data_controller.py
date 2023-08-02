import csv
from tkinter import Tk, Text, INSERT, Button, S


def get_infos_data(file_basename):
    ml = []
    with open(f"src/validators/references/fr/{file_basename}.csv", "r") as file:
        csvreader = csv.reader(file)
        ml = list(csvreader)
        ml.pop(0)
    return ml


def display_info_data_one_column(element):
    items = get_infos_data(element)
    items.sort()
    popup = Tk()
    popup.geometry("550x500")
    popup.title("METIERS ATTENDUS POUR CLIENTS")
    text = Text(popup, background= "cyan", font=("consolas", 10))
    for item in items:
        text.insert(INSERT, f"{item[0]}\n")
        text.pack()
    Button(popup, text="fermer", command=popup.destroy).place(relx=0.5, rely=1.0, anchor=S)
    popup.mainloop()


def display_info_data_two_column(element):
    items = get_infos_data(element)
    items.sort()
    popup = Tk()
    popup.geometry("350x500")
    popup.title("TYPES VOIES ATTENDUS")
    text = Text(popup, background= "cyan", font=("consolas", 10))
    for item in items:
        text.insert(INSERT, f"{item[0]}:{item[1]}\n")
        text.pack()
    Button(popup, text="fermer", command=popup.destroy).place(relx=0.5, rely=1.0, anchor=S)
    popup.mainloop()
