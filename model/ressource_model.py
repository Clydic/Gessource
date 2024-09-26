class RessourceModel(object):
    """
    Contain information for ressources
    constructor contain  argument string
    """

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
        return self.vdefault

    @vdefault.setter
    def vdefault(self, vdefault):
        self.vdefault = vdefault

    def get_values(self):
        return {"vmin": self._vmin, "vmax": self._vmax, "vact": self._vact, "vdefault": self._vdefault}

    def set_values(self, dictionnary_of_values: dict):
        name_of_values = ["vmin", "vmax", "vact", "vdefault"]
        try:
            is_correct_order = self._test_encadrement(dictionnary_of_values)
            for key in dictionnary_of_values.keys():
                if key in name_of_values and is_correct_order:
                    self._vact = dictionnary_of_values['vact']
                    self._vmin = dictionnary_of_values['vmin']
                    self._vmax = dictionnary_of_values['vmax']
                    self._vdefault = dictionnary_of_values['vdefault']
                    return True
        except AttributeError:
            raise AttributeError("Le paramètre doit être un dictionnaire")
        else:
            return False

    def _test_encadrement(self , dictionnary_of_values:dict)->bool: 
        vmin = dictionnary_of_values['vmin']
        vact = dictionnary_of_values['vact']
        vmax = dictionnary_of_values['vmax']
        vdefault = dictionnary_of_values['vdefault']
        return vmin<=vact<=vmax and vmin<=vdefault<=vmax

