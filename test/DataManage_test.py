import sys
import unittest
sys.path.append('..')
from manage.database_manage import DataManage
from model.ressource_model import RessourceModel


class TestDataManage(unittest.TestCase):
    def setUp(self) -> None:
        self.ressource = RessourceModel("PV")
        self.ressource.set_values(
            {"vmin": -10, "vmax": 150, "vdefault": 150, "vact": 100})

    def test_add_data(self):
        data_manage = DataManage()
        data_manage.add_data(self.ressource)
        ressource_name = self.ressource.name
        ressource_values = self.ressource.get_values()
        self.assertEqual(data_manage.data, { 
            ressource_name : ressource_values })

    def test_add_data_error(self):
        data_manage = DataManage()
        data_manage.add_data(self.ressource)
        self.ressource = RessourceModel("Mana")
        self.ressource.set_values(
            {"vmin": -10, "vmax": 150, "vdefault": 150, "vact": 100})
        self.assertRaises(Exception, ('La donnée ne doit âs être ajouté'))
    
    

    
    
