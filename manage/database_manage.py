from collections import OrderedDict
from manage import manage_json_file as mjf
import sys

sys.path.append("..")


class File:
    def __init__(self):
        self._name = ""

    def __get__(self, instance, owner):
        return self._name

    def __set__(self, instance, value):
        self._name = value


class DataManage:
    """
    Link the file where data are saved and the model
    """

    filename = File()

    def __init__(self):
        self._data = OrderedDict()

    @property
    def data(self):
        return self._data

    def _json_to_list(self, json_file):
        liste = []

        for key, values in json_file.items():
            liste.append(
                [key, values["vmin"], values["vmax"],
                    values["vdefaut"], values["vact"]]
            )
        return liste

    def _list_to_json(self, liste_de_liste):
        json_file = {}
        for element in liste_de_liste:
            json_file[element[0]] = {
                "vmin": element[1],
                "vmax": element[2],
                "vdefaut": element[3],
                "vact": element[4],
            }
        return json_file

    def load_data(self):
        self._data = OrderedDict(mjf.load(self.filename))

    def save_data(self):
        mjf.save(self.filename, self._data)

    def add_data(self, ressource_name: str, ressource_values: dict) -> bool:
        if ressource_name not in self._data:
            self._data[ressource_name] = ressource_values
            return True
        return False

    def update_data(self, ressource_name, value_name, new_value):
        self._data[ressource_name][value_name] = new_value

    def update_ressource(self, ressource_name, ressource_values: dict) -> bool:
        if type(ressource_values) == dict:
            self._data[ressource_name] = ressource_values
            return True
        else:
            return False

    def del_data(self, key):
        if key in self.data:
            del self.data[key]
            return True
        return False

    def new(self):
        self.filename = File()
        self._data = OrderedDict()
