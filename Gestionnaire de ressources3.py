#!/usr/bin/env python3  
# -*- coding: utf8 -*-
# Python 3
from tkinter import *
from tkinter.ttk import *
from tkinter.messagebox import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
# import pdb; pdb.set_trace()
import pickle
from collections import OrderedDict
import os
from manage import manage_json_file as mjf
import json

class DataManage:
    """docstring for Save"""
    def __init__(self):
        self._data=OrderedDict()
        


    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, key, value, v):
        self._data =  v

    def _json_to_list(self, json_file):
        liste=[]
        
        for key,values in json_file.items():
            liste.append([key,values["vmin"],values["vmax"],values["vdefaut"],values["vact"]])
        return liste

    def _list_to_json(self, liste_de_liste):
        
        json_file={}
        for element in liste_de_liste:
            json_file[element[0]]={"vmin":element[1], "vmax": element[2], "vdefaut":element[3], "vact":element[4]}
        return json_file

    def load_data(self,filename):
        self._data=OrderedDict(mjf.load(filename))

    def save_data(self,filename):
        mjf.save(filename , self.data)

    def add_data(self, key, liste):
        liste_nom=["vmin","vmax","vdefaut","vact"]
        dictionnary={}
        for index in range(len(liste_nom)):
            dictionnary[liste_nom[index]] = liste[index]
        self._data[key]=dictionnary

    # def update_data(self,key,dictionnary):
    #     liste_keys=list(self.data[key].keys())
    #     if key in self.data:
    #         for index in range(len(values)):
    #             self.data[key][liste_keys[index]] = values[index]
    #     else:
    #          self.add_data(liste)

    def update_data(self, mainkey, secondkey, value):
        self._data[mainkey][secondkey] = value


    def del_data(self, key):
        del self.data[key]

class Root:
    """docstring for Root"""

    root = Tk()
    root.geometry("+350+200")
    save = DataManage()

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
        self.mb.menu.add_command(label="Save game", command=self._command_save)
        self.mb.menu.add_command(label="Save game as", command=self._command_save_as)
        self.mb.menu.add_command(label="Exit", command=self._confirmerquitter)
        # self.menubar.add_cascade(label="Files", menu=self.filemenu)

        # self.root.config(menu=self.menubar)

    # Fonctions lié au menu
    def _command_new(self):  # Fonction lié au bouton new
root=Tk()
filepath=askopenfilename(title="Ouvrir une image", filetypes=[("png files",".png"), ("jpeg files",".jpg"),("allfiles",".*")] ,initialdir=(os.path.expanduser('~/Desktop')))

# image=Image.open("C:/Users/Sweety/Pictures/frond'écran/dinosaure/553025.jpg")
image=Image.open(filepath)
photo=ImageTk.PhotoImage(image ,size=(500,500))
photo.place(x=0,y=0)
canvas=Canvas(root,width=700, height=700,bg="yellow")
item=canvas.create_image(300,300, image=photo)
canvas.place(x=0,y=0)
root.mainloop()
        self._new()

    
    def _command_open(
        self
    ):  # Fonction ouvrant le fichier choisis et l'assigne à save
        self._open()
        

    def _command_save(self):  # Fonction sauvegardant toutes les valeurs de save
        self._save()
        

    def _command_save_as(self):  # fonction lié au bouton save as
        self._save_as()

    def _command_add(self):
       self._add()

    def _new(self):
        self.filename = ""
        self.save.data.__init__()
        self.frame_ressource.destroy()
        self.frame_ressource = Frame(self.root, width=200, relief="groove")
        self.frame_ressource.grid(column=1, row=1)

    def _save(self):
        if self.filename == "":
            self._save_as()
        else:

            # for element in self.listeframe:
            #     self.save.append(element.liste_val)
            self.save.save_data(self.filename)
            showinfo("File saved", "Your file is saved")

    def _save_as(self):
        filename = asksaveasfilename()
        if filename == "":
            pass
        else:
            self.filename = filename
            self._save()

    def _add(self):
        liste = DefVal()
        liste.creation_fenetre()

        if liste.valeurs[0] == "":
            pass
        else:
            self.save.add_data(liste.valeurs[0],liste.valeurs[1:])
            frame = MyFrame(self.frame_ressource, liste.valeurs[0])

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
                self.save.load_data(self.filename)             
                for element in self.save.data:
                    self.frame = MyFrame(self.frame_ressource, element)
                    self.frame.creation_my_frame()
        except TypeError:
            pass
# Cration de l'objet frame dans lequel se trouve un label avec une valeur, une zone d'entrée et un bouton


class MyFrame:
    def __init__(self, root, key):  # Initialisation de My Frame
        self.root = root
        self.name = key
        self.vmin = Root.save.data[key].get("vmin")
        self.vmax = Root.save.data[key].get("vmax")
        self.vdefaut = Root.save.data[key].get("vdefaut")
        self.vact = Root.save.data[key].get("vact")
        self.myframe = Frame(self.root)
        # import pdb; pdb.set_trace()
    def creation_my_frame(self):  # Creation de la fenêtre

        self._creation_lbl_entry()
        self._creation_button()
        self.myframe.pack(pady=5)

    def _creation_lbl_entry(
        self,
    ):  # Creation du label du name est du label de la valeur affiché
        self.text = StringVar()
        self.text.set(str(self.vact))
        lbl1 = Label(self.myframe, text=self.name+":",justify="left")
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
        self.vact = self.vdefaut
        # self.lbl2["text"] = (self.vact, "/", self.vmax)
        self.text.set(str(self.vact))
        Root.save.update_data(self.name,"vact",self.vact)
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
       

    def _test_encadrement(self,vact,vmin,vmax):
        
        if vact < vmin:
            vact = vmin
        elif vact> vmax:
            vact = vmax
        return vact
    

    def _update(self,index,data):
        self.text.set(str(data))            
        Root.save.data[self.i][index] = data
        

    def _test_int(self,vtest):
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
        get_valeur= int(self.entri.get())
        vact=self.vact 
        if self._test_int(get_valeur):
            vact += get_valeur
            self.vact = self._test_encadrement(vact,self.vmin,self.vmax)
            self.text.set(str(self.vact))
            Root.save.update_data(self.name,"vact",self.vact)
        self.entri.delete(0,END)

    def _modifie(self):
        self.fen = DefVal()
        self.fen.modifie = True
        vact=self.vact
        self.fen.valeurs = [self.name]+list(Root.save.data[self.name].values())
        liste_nom = [
            "vmin",
            "vmax",
            "vdefaut",
        ]
        self.fen.creation_fenetre()

        for j in range(1, 4):
            Root.save.update_data(self.name,liste_nom[j-1], self.fen.valeurs[j])
            
       
        self.vmin = Root.save.data[self.name]["vmin"]
        self.vmax = Root.save.data[self.name]["vmax"]
        self.vdefaut = Root.save.data[self.name]["vdefaut"]
        self.vact=self._test_encadrement(vact,self.vmin,self.vmax)
        self.text.set(str(self.vact))
            

class DefVal(Root):
    """docstring for DefVal"""

    def __init__(self):
        self._valeurs = ["", 0, 0, 0, 0]
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

        
    


class RessourceModel(object):
    """docstring for Data_Frame"""

    def __init__(self, ressource_name):
        self._name = ressource_name
        self._vmin = 0
        self._vmax = 0
        self._vdefault = 0
        self._vact = 0

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
