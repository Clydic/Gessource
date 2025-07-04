from tkinter import *
from model.ressource_model import RessourceModel
import sys

sys.path.append("..")


class RessourceView:
    """docstring for DefVal"""

    def __init__(self, root, ressource: RessourceModel, modifie: bool = False):
        self.win = Toplevel(root)
        self.ressource = ressource
        self.modifie = modifie
        self.liste_entry = []
        self.controller = None
        self._valeurs = ["", 0, 0, 0]

    # @property
    # def valeurs(self):
    #     return self._valeurs
    #
    # @valeurs.setter
    # def valeurs(self, v):
    #     self._valeurs = v

    def creation_fenetre(self):  # We create the window of DefVal
        self._forms_creation()
        self._creation_button()
        self.win.geometry("+320+0")
        self.win.mainloop()

    def _forms_creation(self):  # We create lines of the window of Def data
        # === Initialisation
        # We make a list with name of label
        labels = [
            "name:",
            "Valeur min:",
            "Valeur max:",
            "Valeur par defaut:",
        ]
        ressource_value = self.ressource.get_values().copy()
        del ressource_value["vact"]
        values_list = list(ressource_value.values())
        # === Treatment
        for i in range(4):
            # We're creating the frame where is the current line
            frame = Frame(self.win, width=35)
            frame.pack()

            # Are we into a modification case?
            # Yes
            if self.modifie:
                # If it's label name
                if i == 0:
                    # Creation of the Label based on the ressource name
                    self._creation_label(frame, self.ressource.name)

                # If other labels
                else:
                    # Cretation of label and entry fo aother values
                    self._creation_label(frame, labels[i])
                    self._creation_entry(frame, values_list[i - 1])
            # No
            else:
                # Creation of label and entry of forms
                self._creation_label(frame, labels[i])
                self._creation_entry(frame, self._valeurs[i])

    def _creation_label(self, frame, name):
        lbl = Label(frame, text=name, width=18)
        lbl.pack(side=LEFT)

    def _creation_entry(self, frame, value):
        entry = Entry(frame, width=10)
        entry.insert(0, value)
        entry.pack(side=RIGHT)
        self.liste_entry.append(entry)

    def _creation_button(self):
        frame_button = Frame(self.win, width=15)
        frame_button.pack(side=BOTTOM)
        button_ok = Button(frame_button, text="OK", command=self._commande_ok)
        button_ok.pack(side=LEFT)
        button_cancel = Button(
            frame_button, text="Cancel", command=self._command_cancel
        )
        button_cancel.pack(side=RIGHT, padx=5)

    def _commande_ok(self):
        self._get_value()
        if self._test_int(self._valeurs[1:3]):
            if self._test_ordre(self._valeurs[1], self._valeurs[2], self._valeurs[3]):
                self.ressource.vmin = self._valeurs[1]
                self.ressource.vmax = self._valeurs[2]
                self.ressource.vdefault = self._valeurs[3]
                if not self.modifie:
                    self.ressource.name = self._valeurs[0]
                    self.ressource.vact = self._valeurs[3]
                    self.ressource.add()
                else:
                    self.ressource.update()
                self._quit()

    def _command_cancel(self):
        self.win.destroy()

    def _test_encadrement(self, liste):
        test = self._test_int(self.valeurs[1:4])
        if test:
            for index in range(len(self.valeurs)):
                if index != 0:
                    self.valeurs[index] = int(self.valeurs[index])
            if liste[0] == "":
                return False
            if liste[1] > liste[2]:
                showinfo("info", "Le minimum doit être plus petit que le maximum")

            if liste[3] < liste[1] or liste[3] > liste[2]:
                showinfo(
                    "Info",
                    "La valeur par défaut doit être comprise entre le minium et le maximum",
                )

            else:
                return True
        else:
            return False

    def _test_ordre(self, vmin, vmax, test_value):
        if vmin > vmax:
            showinfo("info", "Le minimum doit être plus petit que le maximum")
            return False
        elif test_value < vmin or test_value > vmax:
            showinfo(
                "Info",
                "La valeur par défaut doit être comprise entre le minium et le maximum",
            )
            return False
        else:
            return True

    def _test_int(self, liste):
        try:
            for element in liste:
                element = int(element)

            return True
        except ValueError:
            showerror("Message d'erreur", "Veuillez entrer un entier")

    def _get_value(self):
        if self.modifie:
            self._valeurs[1] = int(self.liste_entry[0].get())  # min
            self._valeurs[2] = int(self.liste_entry[1].get())  # max
            self._valeurs[3] = int(self.liste_entry[2].get())  # valeur par def
        else:
            self._valeurs[0] = str(self.liste_entry[0].get())  # name
            self._valeurs[1] = int(self.liste_entry[1].get())  # min
            self._valeurs[2] = int(self.liste_entry[2].get())  # max
            # valeur par defaut
            self._valeurs[3] = int(self.liste_entry[3].get())

    def _quit(self):
        self.win.quit()
        self.win.destroy()
