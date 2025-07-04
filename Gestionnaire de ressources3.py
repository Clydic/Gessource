#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Python 3
from tkinter import *

# from tkinter.ttk import *
from tkinter.messagebox import askyesno, showinfo, showerror
from tkinter.filedialog import askopenfilename, asksaveasfilename
from view import ressource_component
from model.ressource_model import RessourceModel
from manage.database_manage import DataManage
from view.ressource_view import RessourceView
from view.ressource_component import RessourceComponent


# import pdb; pdb.set_trace()
# import pickle
import os


class Root:
    """docstring for Root"""

    root = Tk()
    root.geometry("+350+200")
    ressources = DataManage()

    def __init__(self):
        self.listeframe = []

        self.root.protocol("WM_DELETE_WINDOW", self._confirmerquitter)
        self.root.bind("<Escape>", self._confirmerquitter)

    def _confirmerquitter(self):
        if askyesno("Quit", "Do you want to quit ?"):
            self.root.destroy()

    def _escape_command(self, event):
        self.ConfirmerQuitter()

    def creation_fenetre(self):
        self._creation_frame()
        self._barre_menu()
        self.root.mainloop()

    def _creation_frame(self):
        self.frame_ressource = Frame(self.root, width=200, relief="groove")
        self.frame_ressource.grid(column=1, row=1)

        self.frame_btt = Frame(self.root)
        self.frame_btt.grid(column=1, row=2)

        self.bttadd = Button(self.frame_btt, text="Add", command=self._command_add)
        self.bttadd.pack(side=LEFT)

    # On crée la barre de menu
    def _barre_menu(self):
        self.mb = Menubutton(self.root, text="Menu")
        self.mb.grid(column=0, row=0)

        self.mb.menu = Menu(self.mb, tearoff=0)
        self.mb["menu"] = self.mb.menu
        self.mb.menu.add_command(label="New game ", command=self._command_new)
        self.mb.menu.add_command(label="Load game", command=self._command_open)
        self.mb.menu.add_command(label="save", command=self._command_save)
        self.mb.menu.add_command(label="save game as", command=self._command_save_as)
        self.mb.menu.add_command(label="Exit", command=self._confirmerquitter)
        # self.menubar.add_cascade(label="Files", menu=self.filemenu)

        # self.root.config(menu=self.menubar)

    # Fonctions lié au menu
    def _command_new(self):  # Fonction lié au bouton new
        self._new()

    def _command_open(
        self,
    ):  # Fonction ouvrant le fichier choisis et l'assigne à ressources
        self._open()

    # Fonction sauvegardant toutes les valeurs de ressources
    def _command_save(self):
        self._save()

    def _command_save_as(self):  # fonction lié au bouton ressources as
        self._save_as()

    def _command_add(self):
        self._add()

    def _new(self):
        self.ressources.new()
        self.frame_ressource.destroy()
        self.frame_ressource = Frame(self.root, width=200, relief="groove")
        self.frame_ressource.grid(column=1, row=1)

    def _save(self):
        if self.ressources.filename == "":
            self._save_as()
        else:
            # for element in self.listeframe:
            #     self.save.append(element.liste_val)
            self.ressources.save_data()
            showinfo("File saved", "Your file is saved")

    def _save_as(self):
        filename = asksaveasfilename()
        if filename == "":
            pass
        else:
            self.ressources.filename = filename
            self.ressources.save_data()

    def _add(self):
        ressource_model = RessourceModel(database=self.ressources)
        ressource_view = RessourceView(root=self.root, ressource=ressource_model)

        ressource_view.creation_fenetre()

        ressource_component = RessourceComponent(
            root=self.frame_ressource,
            ressource=ressource_model,
        )
        ressource_component.creation_my_frame()

    def _open(self):
        self._new()
        filename = askopenfilename()
        try:
            if filename != "":
                self.ressources.filename = filename
                self.ressources.load_data()
                for ressource in self.ressources.data:
                    ressource_model = RessourceModel(
                        database=self.ressources, ressource_name=ressource
                    )
                    ressource_model.set_values(self.ressources.data[ressource])
                    frame = RessourceComponent(
                        root=self.frame_ressource, ressource=ressource_model
                    )
                    frame.creation_my_frame()
        except TypeError:
            pass


def main():
    gestionnaire_ressource = Root()
    gestionnaire_ressource.creation_fenetre()

    # test._json_to_list({'Pv': {'vmin': -10, 'vmax': 20, 'vdefaut': 20, 'vact': 0}, 'Mana': {'vmin': 0, 'vmax': 20, 'vdefaut': 20, 'vact': 0}})


def test_data():
    test = DataManage()
    (liste, liste1) = ([-10, 20, 20, 0], [0, 20, 20, 0])
    test.add_data("PV", liste)
    test.add_data("Mana", liste1)


def test_ordre(vmin, vmax, test_value):
    if vmin > vmax:
        print("info", "Le minimum doit être plus petit que le maximum")
        return False
    elif test_value < vmin or test_value > vmax:
        print(
            "Info",
            "La valeur par défaut doit être comprise entre le minium et le maximum",
        )
        return False
    else:
        print("Le test est bon")
        return True


def several_test_order():
    test_ordre(-10, 100, 60)
    test_ordre(-10, 100, 120)
    test_ordre(-10, 100, -60)
    test_ordre(-10, -100, 60)


if __name__ == "__main__":
    main()

    os.system("pause")
