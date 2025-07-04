from tkinter import *

# from manage import database_manage
from view.ressource_view import RessourceView
from model.ressource_model import RessourceModel
from view.ressource_view import RessourceView
from tkinter.messagebox import askyesno

# import pdb; pdb.set_trace()
import sys

sys.path.append("..")


class RessourceComponent:
    """
    Component that manage a Ressource based on a RessourceModel

    root(Widget): The widget where this component is attach
    ressource(RessourceModel) : The ressource model that manage the ressource
    """

    # Initialisation de My Frame
    def __init__(self, root, ressource: RessourceModel):
        self.root = root
        self.myframe = Frame(self.root)
        self.ressource = ressource

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

    # Change the value when enter key is pressed and clear the input field
    def _command_ok(self, event):
        self._ok()

    def _button_reset(self):  # commande du bouton reset
        # We reinit the actual value
        self.ressource.vact = self.ressource.vdefault

        # We update the texte with the new value
        self.text.set(str(self.ressource.vact))

        # Update the database with the new value
        self.ressource.update()
        self.entri.delete(0, END)
        # import pdb; pdb.set_trace()

    def _button_modifie(self):  # commande du bouton modifie
        # self.listevar=[self.name,self.vmin,self.vmax,self.vdefaut,self.vact]

        self._modifie()

    def _button_delete(self):  # commande du delete
        self._delete()

    def _delete(self):
        if askyesno("Delete", "Do you want to delete ?"):
            is_deleted = self.ressource.delete()
            if is_deleted:
                self.myframe.destroy()
            else:
                showerror(
                    "Error message",
                    "Une erreur s'est produite lors de la suppression",
                )

    def _test_encadrement(self, vact, vmin, vmax):
        if vact < vmin:
            vact = vmin
        elif vact > vmax:
            vact = vmax
        return vact

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
        vact = self.ressource.vact
        # Check if the value is an Integer
        if self._test_int(get_valeur):
            vact += get_valeur
            self.ressource.vact = self._test_encadrement(
                vact, self.ressource.vmin, self.ressource.vmax
            )
            self.ressource.vact = vact
            self.ressource.update()

            self.text.set(str(self.ressource.vact))
        self.entri.delete(0, END)

    def _modifie(self):
        # self.fen = DefVal()
        # self.fen.modifie = True
        ressource_form = RessourceView(
            root=self.root, modifie=True, ressource=self.ressource
        )
        ressource_form.creation_fenetre()
        vact = self.ressource.vact
        self.ressource.vact = self._test_encadrement(
            vact, self.ressource.vmin, self.ressource.vmax
        )
        self.text.set(str(self.ressource.vact))
