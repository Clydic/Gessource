import sys
import unittest
sys.path.append('..')
from model.ressource_model import RessourceModel

class TestRessourceModel(unittest.TestCase):
    def setUp(self):
        self.pv = RessourceModel('PV')

    def test_set_values_AttributeError(self):
        liste = ['2',3 , 4 ]
        self.assertRaises(AttributeError, self.pv.set_values, liste)

    def test_set_values(self):
        dictionnary = {"vmin":-10, "vmax":150, "vdefault": 150, "vact": 100}
        self.pv.set_values(dictionnary)
        self.assertEqual(self.pv.get_values(), dictionnary)


