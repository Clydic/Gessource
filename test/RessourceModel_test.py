from model.ressource_model import RessourceModel
import sys
import unittest
sys.path.append('..')


class TestRessourceModel(unittest.TestCase):
    def setUp(self):
        self.pv = RessourceModel('PV')

    def test_set_values_AttributeError(self):
        liste = ['2', 3, 4]
        self.assertRaises(TypeError, self.pv.set_values, liste)

    def test_set_values_True(self):
        dictionnary = {"vmin": -10, "vmax": 150, "vdefault": 150, "vact": 100}
        msg = "The result should be True"
        self.assertTrue(self.pv.set_values(dictionnary), msg)

    def test_set_values_False(self):
        dictionnary = {"vmin": -10, "vmax": 150,
                       "vdefault": 150, "vact": 100, "test": "foo"}
        msg = "The result should False"
        self.assertFalse(self.pv.set_values(dictionnary), msg)

    def test_get_values(self):
        dictionnary = {"vmin": -10, "vmax": 150, "vdefault": 150, "vact": 100}
        pv = self.pv
        pv.set_values(dictionnary)
        self.assertEqual(pv.get_values(), dictionnary)
