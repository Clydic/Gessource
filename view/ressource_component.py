from tkinter import *

# from manage import database_manage
from model.ressource_model import RessourceModel
from manage.database_manage import DataManage

# import pdb; pdb.set_trace()
import sys

sys.path.append("..")


class RessourceComponent:
    # Initialisation de My Frame
    def __init__(self, root, ressource: RessourceModel, database: DataManage):
        self.root = root
        self.myframe = Frame(self.root)
        self.ressource = ressource
        self.database = database

    def creation_my_frame(self):  # Creation de la fenêtre
        self._creation_lbl_entry()
        self._creation_button()
        self.myframe.pack(pady=5)

    def _creation_lbl_entry(
        self,
    ):  # Creation du label du name est du label de la valeur affiché
        self.text = StringVar()
        self.text.set(str(self.ressource.vact))
        lbl1 = Label(self.myframe, text=self.ressource.name +
                     ":", justify="left")
        lbl1.grid(row=0, column=1)

        lbl2 = Label(self.myframe, textvariable=self.text, justify="right")
        lbl2.grid(row=0, column=2)

        self.entri = Entry(self.myframe, width=10)
        self.entri.bind("<Return>", self._command_ok)
        self.entri.grid(row=0, column=3)

    def _creation_button(
        self,
    ):  # Creation des boutons de modification, de suppression et de reset
        self.photo_reset = PhotoImage(file="image/fleche_reset.gif")
        bps_reset = Button(
            self.myframe, image=self.photo_reset, command=self._button_reset
        )
        bps_reset.grid(row=0, column=4)

        self.photo_modifie = PhotoImage(file="image/mini_crayon.gif")
        bps_modifie = Button(
            self.myframe, image=self.photo_modifie, command=self._button_modifie
        )
        bps_modifie.grid(row=0, column=5)

        self.photo_delete = PhotoImage(file="image/mini_corbeille.gif")
        bps_delete = Button(
            self.myframe, image=self.photo_delete, command=self._button_delete
        )
        bps_delete.grid(row=0, column=6)

    # Fonction du bouton ok qui modifie les valeurs et nettoie l'Entry
    def _command_ok(self, event):
        self._ok()

    def _button_reset(self):  # commande du bouton reset
        # We reinit the actual value
        self.ressource_model.vact = self.ressource_model.vdefaut

        # We update the texte with the new value
        self.text.set(str(self.ressource_model.vact))

        # Update the database with the new value
        database_manage.update_data(self.name, "vact", self.ressource.vact)
        self.entri.delete(0, END)
        # import pdb; pdb.set_trace()

    def _button_modifie(self):  # commande du bouton modifie
        # self.listevar=[self.name,self.vmin,self.vmax,self.vdefaut,self.vact]

        self._modifie()

    def _button_delete(self):  # commande du delete
        self._delete()

    def _delete(self):
        if askyesno("Delete", "Do you want to delete ?"):
            Root.save.del_data(self.name)
            self.myframe.destroy()

    def _test_encadrement(self, vact, vmin, vmax):
        if vact < vmin:
            vact = vmin
        elif vact > vmax:
            vact = vmax
        return vact

    def _update(self, index, data):
        self.text.set(str(data))
        Root.save.data[self.i][index] = data

    def _test_int(self, vtest):
        try:
            int(vtest)
            return True
        except ValueError:
            showerror(
                "Error message",
                "Veuillez entrer un entier positif ou negatif ou nul",
            )
            return False

    def _ok(self):
        get_valeur = int(self.entri.get())
        vact = self.vact
        if self._test_int(get_valeur):
            vact += get_valeur
            self.vact = self._test_encadrement(vact, self.vmin, self.vmax)
            self.text.set(str(self.vact))
            Root.save.update_data(self.name, "vact", self.vact)
        self.entri.delete(0, END)

    def _modifie(self):
        self.fen = DefVal()
        self.fen.modifie = True
        vact = self.vact
        self.fen.valeurs = [self.name] + \
            list(Root.save.data[self.name].values())
        liste_nom = [
            "vmin",
            "vmax",
            "vdefaut",
        ]
        self.fen.creation_fenetre()

        for j in range(1, 4):
            Root.save.update_data(
                self.name, liste_nom[j - 1], self.fen.valeurs[j])

        self.vmin = Root.save.data[self.name]["vmin"]
        self.vmax = Root.save.data[self.name]["vmax"]
        self.vdefaut = Root.save.data[self.name]["vdefaut"]
        self.vact = self._test_encadrement(vact, self.vmin, self.vmax)
        self.text.set(str(self.vact))
