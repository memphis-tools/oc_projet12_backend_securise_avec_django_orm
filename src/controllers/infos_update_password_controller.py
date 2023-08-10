import csv
from tkinter import Tk, Text, INSERT, Button, S

try:
    from src.settings import settings
except ModuleNotFoundError:
    from settings import settings


def display_info_password_policy():
    items = settings.NEW_PASSWORD_POLICY
    popup = Tk()
    popup.geometry("650x500")
    popup.title("POLITIQUE DES MOTS DE PASSE")
    text = Text(popup, background= "cyan", font=("consolas", 10))
    for item in items:
        text.insert(INSERT, f"{item}:")
        text.insert(INSERT, str(eval(f"settings.{item}")) + "\n")
        text.pack()
    Button(popup, text="fermer", command=popup.destroy).place(relx=0.5, rely=1.0, anchor=S)
    popup.mainloop()
