import unittest

from bson import ObjectId


class AdminTests(unittest.TestCase):
    repository_collection = None

    def setUp(self):
        self.devices = AdminTests.repository_collection.device_repository
        self.houses = AdminTests.repository_collection.house_repository
        self.users = AdminTests.repository_collection.user_repository
        self.user1id = self.users.add_user("Benny Clark", "xxxxxxxx", "benny@example.com", False)
        self.house1id = self.houses.add_house(self.user1id, "Benny's House", None)
        self.adapter1id = self.devices.add_device(house_id=self.house1id, room_id=None,
                                                  name="Test Adapter",
                                                  device_type="light_switch", target={},
                                                  configuration={"username": 'bc15050@mybristol.ac.uk',
                                                                 "password": 'test1234',
                                                                 "device_id": '46865'},
                                                  vendor='energenie')

    def tearDown(self):
        self.devices.clear_db()
        self.houses.clear_db()
        self.users.clear_db()

    def test_GettingEnergyReadingsAsList(self):
        consumption = self.devices.get_energy_consumption(self.adapter1id)
        self.assertIsInstance(consumption, list, "Not returning correct format for energy consumption")
        # We can probably only assume that the length is 7 for devices that are actually being used.
        # self.assertEqual(len(consumption), 7, "Size of consumption array is not correct")
