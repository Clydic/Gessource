import sys
sys.path.append('..')
from model.ressource_model import RessourceModel
class RessourceView(Root):
    """docstring for DefVal"""

    def __init__(self):
        self._valeurs = ["", 0, 0, 0, 0]
        self.modifie = False
        self.liste_entry = []
        self.win = Toplevel(self.root)
        self.win.geometry("+320+0")
        self.controller = None

    @property
    def valeurs(self):
        return self._valeurs

    @valeurs.setter
    def valeurs(self, v):
        self._valeurs = v

def set_controller(self, controller):
    self.controller = controller

    def creation_fenetre(self):  # We create the window of DefVal

        self._creation_ligne()
        self._creation_button()
        self.win.mainloop()

    def _creation_ligne(self):  # We create lines of the window of Def data

        self.liste_nom = [
            "name:",
            "Valeur min:",
            "Valeur max:",
            "Valeur par defaut:",
        ]  # We make a list with name of label
        for i in range(4):
            self.frame = Frame(self.win, width=35)
            self.frame.pack()
            if self.modifie:
                if i == 0:
                    self._creation_label(self.frame,self.valeurs[i])
                   
                else:    
                    self._creation_label(self.frame,self.liste_nom[i])
                    self._creation_entry(self.frame,self._valeurs[i])
            else:
                self._creation_label(self.frame,self.liste_nom[i])
                self._creation_entry(self.frame,self._valeurs[i])
               
        
    def _creation_label(self,frame,name):
        self.lbl = Label(self.frame, text=name, width=18)
        self.lbl.pack(side=LEFT)



    def _creation_entry(self , frame, value):
        self.entry = Entry(frame, width=10)
        self.entry.insert(0, value)
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

        self._get_value()
        if self._test_int(self.valeurs[1:3]):
            if self._test_ordre(self.valeurs[1],self.valeurs[2],self.valeurs[3]):
                if not self.modifie:
                    self.valeurs[4] = self.valeurs[3]
            
                
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
        if vmin>vmax:
             showinfo("info", "Le minimum doit être plus petit que le maximum")
             return False
        elif test_value<vmin or test_value>vmax:
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
            self.valeurs[1] = int(self.liste_entry[0].get())  # min
            self.valeurs[2] = int(self.liste_entry[1].get())  # max
            self.valeurs[3] = int(self.liste_entry[2].get())  # valeur par def
        else:
            self.valeurs[0] = str(self.liste_entry[0].get())  # name
            self.valeurs[1] = int(self.liste_entry[1].get())  # min
            self.valeurs[2] = int(self.liste_entry[2].get())  # max
            self.valeurs[3] = int(self.liste_entry[3].get())  # valeur par defaut

    def _quit(self):
        self.win.quit()
        self.win.destroy()

