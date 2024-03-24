#!/usr/bin/env python3  
# -*- coding: utf8 -*-
# Python 3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
from model.ressource_model import RessourceModel
from manage.database_manage import DataManage
from view.ressource_view import RessourceView


# import pdb; pdb.set_trace()
import pickle
import os
from manage import manage_json_file as mjf

class Root:
    """docstring for Root"""

    root = Tk()
    root.geometry("+350+200")
    ressources = DataManage()

    def __init__(self):
        self.filename = ""
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
        self.mb.menu.add_command(label="New game test", command=self._command_new)
        self.mb.menu.add_command(label="Load game", command=self._command_open)
        self.mb.menu.add_command(label="ressources game", command=self._command_ressources)
        self.mb.menu.add_command(label="ressources game as", command=self._command_ressources_as)
        self.mb.menu.add_command(label="Exit", command=self._confirmerquitter)
        # self.menubar.add_cascade(label="Files", menu=self.filemenu)

        # self.root.config(menu=self.menubar)

    # Fonctions lié au menu
    def _command_new(self):  # Fonction lié au bouton new
        root=Tk()
        filepath=askopenfilename(title="Ouvrir une image", filetypes=[("png files",".png"), ("jpeg files",".jpg"),("allfiles",".*")] ,initialdir=(os.path.expanduser('~/Desktop')))

        # image=Image.open("C:/Users/Sweety/Pictures/frond'écran/dinosaure/553024.jpg")
        image=Image.open(filepath)
        photo=ImageTk.PhotoImage(image ,size=(500,500))
        photo.place(x=0,y=0)
        canvas=Canvas(root,width=700, height=700,bg="yellow")
        item=canvas.create_image(300,300, image=photo)
        canvas.place(x=0,y=0)
        root.mainloop()
        self._new()

    
    def _command_open( self):  # Fonction ouvrant le fichier choisis et l'assigne à ressources
        self._open()
        

    def _command_ressources(self):  # Fonction sauvegardant toutes les valeurs de ressources
        self._ressources()
        

    def _command_ressources_as(self):  # fonction lié au bouton ressources as
        self._ressources_as()

    def _command_add(self):
       self._add()

    def _new(self):
        self.filename = ""
        self.ressources.data.__init__()
        self.frame_ressource.destroy()
        self.frame_ressource = Frame(self.root, width=200, relief="groove")
        self.frame_ressource.grid(column=1, row=1)

    def _save(self):
        if self.filename == "":
            self._save_as()
        else:

            # for element in self.listeframe:
            #     self.save.append(element.liste_val)
            self.ressources.save_data(self.filename)
            showinfo("File saved", "Your file is saved")

    def _save_as(self):
        filename = asksaveasfilename()
        if filename == "":
            pass
        else:
            self.filename = filename
            self._ressources()

    def _add(self):
        liste = DefVal()
        liste.creation_fenetre()

        if liste.valeurs[0] == "":
            pass
        else:
            new_ressource = RessourceModel(liste.valeurs[0])
            liste.valeurs = liste.valeurs[1:]
            name_of_values = ["vmin", "vmax", "vact", "vdefault" ]
            values_for_ressource_model ={}
            for i in range(4):
                values_for_ressource_model[name_of_values[i]] = liste.valeurs
            RessourceModel.set_values({values_for_ressource_model})
            self.ressources.add_data(RessourceModel)
            frame = RessourceView(self.frame_ressource, liste.valeurs[0])

            frame.creation_my_frame()

    def _open(self):
        self._new()
        filename = askopenfilename()
        try:
            if filename == "":
                pass
            else:
                self.filename = filename
                # import pdb; pdb.set_trace()
                self.ressources.load_data(self.filename)             
                for ressource in self.ressources.data:
                    self.frame = RessourceView(self.frame_ressource, ressource)
                    self.frame.creation_my_frame()
        except TypeError:
            pass


class DefVal(Root):
    """docstring for DefVal"""

    def __init__(self, list_of_values: list):
        self._valeurs = list_of_values
        self.modifie = False
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
        if self._test_int(self.valeurs[1:3]) and self._test_ordre(
        self.valeurs[1],self.valeurs[2],self.valeurs[3]):
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


def main():
     gestionnaire_ressource = Root()
     gestionnaire_ressource.creation_fenetre()
    
    
    # test._json_to_list({'Pv': {'vmin': -10, 'vmax': 20, 'vdefaut': 20, 'vact': 0}, 'Mana': {'vmin': 0, 'vmax': 20, 'vdefaut': 20, 'vact': 0}})
   
    
def test_data():
    test=DataManage()
    (liste,liste1)=([-10, 20, 20, 0],[0, 20, 20, 0])
    
    test.add_data("PV",liste)
    
    test.add_data("Mana", liste1)

def test_ordre(vmin, vmax, test_value):
    if vmin>vmax:
         print("info", "Le minimum doit être plus petit que le maximum")
         return False
    elif test_value<vmin or test_value>vmax:
        print(
                "Info",
                "La valeur par défaut doit être comprise entre le minium et le maximum",
            )
        return False
    else:
     
        print("Le test est bon")
        return True
def several_test_order():
    test_ordre(-10, 100 , 60)
    test_ordre(-10, 100 , 120)
    test_ordre(-10, 100 , -60)
    test_ordre(-10, -100 , 60)
if __name__ == "__main__":
    main()

    os.system("pause")
