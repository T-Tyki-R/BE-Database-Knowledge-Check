# # Imports
# from application import create_app
# from application.models import db, Inventory
# import unittest
# import pytest


# class TestInventory(unittest.TestCase):
#     def setUp(self):
#         self.app = create_app("TestingConfig")
#         self.inventory = Inventory(name="Gas Pedal", price= 150.00)
#         with self.app.app_context():
#             db.drop_all()
#             db.create_all()
#             db.session.add(self.inventory)
#             db.session.commit()
#         self.client = self.app.test_client()
    
#     # Successful Creation Test
#     def test_create_inventory(self):
#         inventory_payload = {
#             "name": "Brake Pedal",
#             "price": 150.00
#         }

#         response = self.client.post('/inventory/create', json= inventory_payload)
#         self.assertEqual(response.status_code, 201)
#         self.assertEqual(response.json['name'], "Brake Pedal")

#     # # Failed Creation Test
#     def test_create_inventory_fail(self):
#         inventory_payload = {
#             "name": "Gas Pedal"
#             # Price field is missing for testing purposes

#         }

#         response = self.client.post('/inventory/create', json= inventory_payload)
#         self.assertEqual(response.status_code, 400)
#         self.assertIn(response.json['price'], "Missing field: Price")
    
#     # # Successful Update Test
#     def test_update_inventory(self):
#         update_payload = {
#             "name": "Brake Pedal",
#             "price" : 150.00
#         }

#         headers = {"Inventory_ID": str(self.inventory.inventory_id)}

#         # Fix: Use self.inventory.inventory_id in URL instead of hardcoded '1'
#         response = self.client.put(f'/inventory/update/{self.inventory.inventory_id}', json=update_payload, headers=headers)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json['name'], 'Brake Pedal')
#         self.assertEqual(response.json['price'], 150.00) 


    # # Failed Update Test
    # def test_update_inventory_fail(self):
    #     update_payload = {
    #         "name": "Brake Pedal",
    #         "email" : "test@email.com",
    #         "phone" : "",
    #         "salary" : 0,
    #         "password" : ""
    #     }

    #     headers = {'Authorization': "Bearer " + self.test_login_inventory()}

    #     response = self.client.put('/inventorys/update', json=update_payload, headers=headers)
    #     self.assertEqual(response.status_code, 404)
    #     self.assertEqual(response.json['message'], 'inventory not found')


