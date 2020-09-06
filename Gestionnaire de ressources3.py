#!/usr/bin/env python3
# -*- coding: utf8 -*-
# Python 3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename

import pickle
from collections import OrderedDict
import os
from manage import manage_json_file as mjf
import json


class Root(object):
    """docstring for Root"""

    root = Tk()
    root.geometry("+150+0")
    save = []

    def __init__(self):
        self.filename = ""
        self.listeframe = []

        self.root.protocol("WM_DELETE_WINDOW", self._confirmerquitter)
        self.root.bind("<Escape>", self._confirmerquitter)

    def _confirmerquitter(self):
        if askyesno("Quitter", "Voulez-vous vraiment quitter ?"):
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
        self.mb.menu.add_command(label="New game", command=self._command_new)
        self.mb.menu.add_command(label="Load game", command=self._command_open)
        self.mb.menu.add_command(label="Save game", command=self._command_save)
        self.mb.menu.add_command(label="Save game as", command=self._command_save_as)
        self.mb.menu.add_command(label="Exit", command=self._confirmerquitter)
        # self.menubar.add_cascade(label="Files", menu=self.filemenu)

        # self.root.config(menu=self.menubar)

    # Fonctions lié au menu
    def _command_new(self):  # Fonction lié au bouton new
        self.filename = ""
        self.frame_ressource.destroy()
        self.frame_ressource = Frame(self.root)
        self.frame_ressource.grid(column=1, row=1)

    def _command_open(
        self
    ):  # Fonction ouvrant le fichier choisis et l'assigne à save

        filename = askopenfilename()
        try:
            if filename == "":
                pass
            else:
                self.filename = filename
                if Root.save != []:
                    self.frame_ressource.destroy()
                    self.frame_ressource = Frame(self.root, width=1)
                    self.frame_ressource.grid(column=1, row=1)
                # import pdb; pdb.set_trace()
                with open(self.filename, "rb") as file:
                    my_load = pickle.Unpickler(file)
                    Root.save = my_load.load()
                for element in Root.save:
                    self.frame = MyFrame(self.frame_ressource, element)
                    self.frame.creation_my_frame()
        except TypeError:
            pass

    def _command_save(self):  # Fonction sauvegardant toutes les valeurs de save
        
        if self.filename == "":
            pass
        else:

            # for element in self.listeframe:
            #     self.save.append(element.liste_val)
            

            with open(self.filename, "wb") as file:
                my_save = pickle.Pickler(file)
                my_save.dump(self.save)

            showinfo("File saved", "Your file is save")

    def _command_save_as(self):  # fonction lié au bouton save as
        filename = asksaveasfilename()
        if filename == "":
            pass
        else:
            self.filename = filename
            self.command_save()

    def _command_add(self):
        liste = DefVal()
        liste.creation_fenetre()

        if liste.valeurs[0] == "":
            pass
        else:
            Root.save.append(liste.valeurs)
            frame = MyFrame(self.frame_ressource, liste.valeurs)
            Root.save.append(frame)
            frame.creation_my_frame()


# Cration de l'objet frame dans lequel se trouve un label avec une valeur, une zone d'entrée et un bouton


class MyFrame:
    def __init__(self, root, liste):  # Initialisation de My Frame
        self.root = root
        # self.liste_val = liste_val
        self.i = Root.save.index(liste)
        self.text = StringVar()
        self.nom = liste[0]
        self.vmin = liste[1]
        self.vmax = liste[2]
        self.vdefaut = liste[3]
        self.vact = liste[4]
        self.myframe = Frame(self.root)

    def creation_my_frame(self):  # Creation de la fenêtre

        self._creation_lbl_entry()
        self._creation_button(),
        self.myframe.pack(pady=5)

    def _creation_lbl_entry(
        self,
    ):  # Creation du label du nom est du label de la valeur affiché

        self.text.set(str(self.vact))
        self.lbl1 = Label(self.myframe, text=(self.nom, ":"), width=6)
        self.lbl1.grid(row=0, column=1)

        self.lbl2 = Label(self.myframe, textvariable=self.text)
        self.lbl2.grid(row=0, column=2)

        self.entri = Entry(self.myframe, width=10)
        self.entri.bind("<Return>", self._valid_ok)
        self.entri.grid(row=0, column=3)

    def _creation_button(
        self,
    ):  # Creation des boutons de modification, de suppression et de reset
        self.photo_reset = PhotoImage(file="image/fleche_reset.gif")
        self.bps_reset = Button(
            self.myframe, image=self.photo_reset, command=self._button_reset
        )
        self.bps_reset.grid(row=0, column=4)

        self.photo_modifie = PhotoImage(file="image/mini_crayon.gif")
        self.bps_modifie = Button(
            self.myframe, image=self.photo_modifie, command=self._button_modifie
        )
        self.bps_modifie.grid(row=0, column=5)

        self.photo_delete = PhotoImage(file="image/mini_corbeille.gif")
        self.bps_delete = Button(
            self.myframe, image=self.photo_delete, command=self._button_delete
        )
        self.bps_delete.grid(row=0, column=6)

    # Fonction du bouton ok qui modifie les valeurs et nettoie l'Entry
    def _valid_ok(self, event):
        try:
            get_valeur = int(self.entri.get())
        except ValueError:
            showerror(
                "Error message",
                "Veuillez entrer un entier positif ou negatif ou nul",
            )
            get_valeur = 0
            self.entri.delete(0, END)
        else:
            self.vact += get_valeur

            if self.vact < self.vmin:
                self.vact = self.vmin
            elif self.vact > self.vmax:
                self.vact = self.vmax
            self.text.set(str(self.vact))
            Root.save[self.i][4] = self.vact
            self.entri.delete(0, END)

    def _button_reset(self):  # commande du bouton reset
        self.vact = self.vdefaut
        # self.lbl2["text"] = (self.vact, "/", self.vmax)
        self.text.set(str(self.vact))
        self.entri.delete(0, END)

    def _button_modifie(self):  # commande du bouton modifie
        # self.listevar=[self.nom,self.vmin,self.vmax,self.vdefaut,self.vact]
        self.fen = DefVal()
        self.fen.valeurs = self.liste_val
        self.fen.creation_fenetre()

        for j in range(0, 4):
            Root.save[self.i][j] = self.fen.valeurs[j]
            self.liste_val[j] = self.liste_val[j]
        self.nom = self.liste_val[0]
        self.vmin = self.liste_val[1]
        self.vmax = self.liste_val[2]
        self.vdefaut = self.liste_val[3]
        self.lbl1["text"] = self.nom
        # self.lbl2["text"] = (self.vact, "/", self.vmax)
        self.text.set(str(self.vact))

    def _button_delete(self):  # commande du delete

        self.myframe.destroy()
        Root.save.remove(self.liste_val)


class DefVal(Root):
    """docstring for DefVal"""

    def __init__(self):
        self._valeurs = ["", 0, 0, 0, 0]
        self.liste_entry = []
        self.win = Toplevel(self.root)
        self.win.geometry("+320+0")

    @property
    def valeurs(self):
        return self._valeurs

    @valeurs.setter
    def valeurs(self, v):
        self._valeurs = v

    def creation_fenetre(self):  # We create the window of DefVal

        self._creation_ligne()
        self._creation_button()
        self.win.mainloop()

    def _creation_ligne(self):  # We create lines of the window of Def val

        self.liste_nom = [
            "Nom:",
            "Valeur min:",
            "Valeur max:",
            "Valeur par defaut:",
        ]  # We make a liste with name of label
        for i in range(4):
            self.frame = Frame(self.win, width=35)
            self.frame.pack()
            self.lbl = Label(self.frame, text=self.liste_nom[i], width=18)
            self.lbl.pack(side=LEFT)
            self.entry = Entry(self.frame, width=10)
            self.entry.insert(0, self._valeurs[i])
            self.entry.pack(side=RIGHT)
            self.liste_entry.append(self.entry)

    def _creation_button(self):
        self.frame_button = Frame(self.win, width=15)
        self.frame_button.pack(side=BOTTOM)
        self.button_ok = Button(
            self.frame_button, text="OK", command=self._commande_ok
        )
        self.button_ok.pack(side=LEFT)
        self.button_cancel = Button(
            self.frame_button, text="Cancel", command=self._command_cancel
        )
        self.button_cancel.pack(side=RIGHT, padx=5)

    def _commande_ok(self):
        test = None
        self.valeurs[0] = str(self.liste_entry[0].get())  # nom
        self.valeurs[1] = self.liste_entry[1].get()  # min
        self.valeurs[2] = self.liste_entry[2].get()  # max
        self.valeurs[3] = self.liste_entry[3].get()  # valeur par defaut
        self._test_encadrement(self.valeurs)

    def _command_cancel(self):

        self.win.quit()
        self.win.destroy()

    def _test_encadrement(self, liste):

        test = self._test_int(self.valeurs[1:4])

        if test:
            for index in range(len(self.valeurs)):
                if index != 0:
                    self.valeurs[index] = int(self.valeurs[index])
            if liste[0] == "":
                self.win.destroy()
                self.win.quit()
            if self.valeurs[1] > liste[2]:
                showinfo("info", "Le minimum doit être plus petit que le maximum")
            if liste[3] < liste[1] or liste[3] > liste[2]:
                showinfo(
                    "Info",
                    "La valeur par défaut doit être comprise entre le minium et le maximum",
                )
            else:
                self.valeurs[4] = self.valeurs[3]
                self.win.quit()
                self.win.destroy()
        else:
            pass

    def _test_int(self, liste):
        try:

            for element in liste:

                element = int(element)

            return True
        except ValueError:
            showerror("Message d'erreur", "Veuillez entrer un entier")
            return False


class Data(object):
    """docstring for Save"""
    def __init__(self):
        self._val=[]
        


    @property
    def val(self):
        return self._val

    @val.setter(self, v):
        self._val =  v

    def _json_to_list(self, json_file, liste):
        pass  

    def _list_to_json(self, liste, json_file):
        pass

    def load_data(self):
        pass

    def save_data(self):
        pass

    def add_data(self, liste):
        self._val.append(liste)

    def del_data(self):
        pass


class Data_Frame(object):
    """docstring for Data_Frame"""

    def __init__(self, liste):
        self._name=liste[0]
        self._vmin=liste[1]
        self._vmax=liste[2]
        self._vdefault=liste[3]
        self._vact=liste[4]

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self,name):
        self._name = name


    @property
    def vmin(self):
        return self._vmin


    @vmin.setter
    def vmin(self,vmin):
        self._vmin = vmin


    @property
    def vmax(self):
        return self._vmax


    @vmax.setter
    def vmax(self,vmax):
        self._vmax = vmax


    @property
    def vdefaut(self):
        return self.vdefaut


    @vdefaut.setter
    def vdefaut(self,vdefaut):
        self._name = vdefaut


          

def main():
    gestionnaire_ressource = Root()
    gestionnaire_ressource.creation_fenetre()


if __name__ == "__main__":
    main()

    # os.system("pause")
