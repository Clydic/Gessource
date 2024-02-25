from collections import OrderedDict
from manage import manage_json_file as mjf
import sys
sys.path.append('..')
from model.ressource_model import RessourceModel


class DataManage:
    """docstring for Save"""

    def __init__(self):
        self._data = OrderedDict()

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, key, value, v):
        self._data = v

    def _json_to_list(self, json_file):
        liste = []

        for key, values in json_file.items():
            liste.append([key, values["vmin"], values["vmax"],
                         values["vdefaut"], values["vact"]])
        return liste

    def _list_to_json(self, liste_de_liste):

        json_file = {}
        for element in liste_de_liste:
            json_file[element[0]] = {
                "vmin": element[1], "vmax": element[2], "vdefaut": element[3], "vact": element[4]}
        return json_file

    def load_data(self, filename):
        self._data = OrderedDict(mjf.load(filename))

    def save_data(self, filename):
        mjf.save(filename, self.data)

    def add_data(self, ressource : RessourceModel):
        ressource_name = ressource.name
        ressource_values = ressource.get_values()
        if ressource_name not in self._data:
            self._data[ressource_name] = ressource_values
        raise Exception ("The ressource exists already")

    # def update_data(self,key,dictionnary):
    #     liste_keys=list(self.data[key].keys())
    #     if key in self.data:
    #         for index in range(len(values)):
    #             self.data[key][liste_keys[index]] = values[index]
    #     else:
    #          self.add_data(liste)

    def update_data(self, ressource_name, ressource_old_value, new_value):
        self._data[ressource_name][ressource_old_value] = new_value

    def del_data(self, key):
        del self.data[key]
