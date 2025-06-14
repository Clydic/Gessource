from manage.database_manage import DataManage


class RessourceModel:
    """
    Contain information for ressources
    constructor contain  argument string
    """

    def __init__(self, database: DataManage, ressource_name: str = None):
        self._name = ressource_name
        self._vmin = 0
        self._vmax = 0
        self._vdefault = 0
        self._vact = 0
        self.database = database

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        self._name = name

    @property
    def vmin(self):
        return self._vmin

    @vmin.setter
    def vmin(self, vmin):
        self._vmin = vmin

    @property
    def vmax(self):
        return self._vmax

    @vmax.setter
    def vmax(self, vmax):
        self._vmax = vmax

    @property
    def vdefault(self):
        return self._vdefault

    @vdefault.setter
    def vdefault(self, vdefault):
        self._vdefault = vdefault

    @property
    def vact(self):
        return self._vact

    @vact.setter
    def vact(self, vact):
        if vact < self._vmin:
            self._vact = self._vmin
        elif vact > self._vmax:
            self._vact = self._vmax
        else:
            self._vact = vact

    def get_values(self):
        return {
            "vmin": self._vmin,
            "vmax": self._vmax,
            "vact": self._vact,
            "vdefault": self._vdefault,
        }

    def set_values(self, dictionnary_of_values: dict):
        name_of_values = ["vmin", "vmax", "vact", "vdefault"]
        name_of_values.sort()

        if type(dictionnary_of_values) is not dict:
            raise TypeError("The paramater should be a dictionnary")
            return False

        keys_list = list(dictionnary_of_values)
        keys_list.sort()

        if name_of_values != keys_list:
            raise KeyError("Certaine clés ne sont pas présente")
            return False

        is_correct_order = self._test_encadrement(dictionnary_of_values)

        if is_correct_order:
            self._vact = int(dictionnary_of_values["vact"])
            self._vmin = int(dictionnary_of_values["vmin"])
            self._vmax = int(dictionnary_of_values["vmax"])
            self._vdefault = int(dictionnary_of_values["vdefault"])
            return True
        else:
            return False

    def add(self):
        self.database.add_data(
            ressource_name=self._name, ressource_values=self.get_values()
        )

    def update(self) -> bool:
        return self.database.update_ressource(
            ressource_name=self._name, ressource_values=self.get_values
        )

    def delete(self):
        return self.database.del_data(self.name)

    def _test_encadrement(self, dictionnary_of_values: dict) -> bool:
        vmin = dictionnary_of_values["vmin"]
        vact = dictionnary_of_values["vact"]
        vmax = dictionnary_of_values["vmax"]
        vdefault = dictionnary_of_values["vdefault"]
        return vmin <= vact <= vmax and vmin <= vdefault <= vmax
