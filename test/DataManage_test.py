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

    def test_add_data_True(self):
        data_manage = DataManage()
        self.assertTrue(
            data_manage.add_data(self.ressource), "The result should True"
        )

    def test_add_data_False(self):
        data_manage = DataManage()
        data_manage.add_data(self.ressource)
        self.assertFalse(
            data_manage.add_data(self.ressource), "The result should False"
        )
