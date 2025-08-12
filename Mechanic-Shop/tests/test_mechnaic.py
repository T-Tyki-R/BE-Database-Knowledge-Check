# Imports
from application import create_app
from application.models import db, Mechanic
from application.Utils.util import encode_token
import unittest


class TestmMechanic(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.mechanic = Mechanic(name="test_user", email="test1@email.com",
                                  phone= "1231231234", salary= 12000.00, password="test12")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.mechanic)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
    
    # Successful Creation Test
    def test_create_mechanic(self):
        mechanic_payload = {
            "name": "Naruto Uzumaki",
            "email" : "ichirakuramen1@email.com",
            "phone" : "0009990000",
            "salary" : 12000.00,
            "password" : "fishCakeSpiral1"
        }

        response = self.client.post('/mechanics/create', json= mechanic_payload)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], "Naruto Uzumaki")

     # Failed Creation Test
    def test_create_mechanic_fail(self):
        mechanic_payload = {
            "name": "Naruto Uzumaki",
            "email" : "ichirakuramen1@email.com",
            "phone" : "0009990000",
            "salary" : 50000.00
            # password is missing for testing purposes
        }

        response = self.client.post('/mechanics/create', json= mechanic_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['password'], "Missing field: Password")

    # Successful Login Test
    def test_login_mechanic(self):
        credentials = {
            "email" : "test1@email.com",
            "password" : "test12"
        }

        response = self.client.post('/mechanics/login', json= credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], "success")
        return response.json['token']
    
    # Failed Login Test
    def test_login_mechanic_fail(self):
        credentials = {
            "email" : "failure1@gmail.com",
            "password" : "test212"
        }

        response = self.client.post('/mechanics/login', json= credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Invalid email or password")

    
    #Successful Update Test
    def test_update_mechanic(self):
        update_payload = {
            "name": "Levi Ackerman",
            "email" : "test@email.com",
            "phone" : "",
            "salary": 20000.00,
            "password" : ""
        }

        headers = {'Authorization': "Bearer " + self.test_login_mechanic()}

        response = self.client.put('/mechanics/update', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Levi Ackerman') 
        self.assertEqual(response.json['email'], 'test@email.com')    
        self.assertEqual(response.json['salary'], 20000.00)

    # Failed Update Test
    def test_update_mechanic_fail(self):
        update_payload = {
            "name": "Levi Ackerman",
            "email" : "test@email.com",
            "phone" : "",
            "salary" : 0,
            "password" : ""
        }

        response = self.client.put('/mechanics/update', json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "You must be logged in to access") 

    #Successful Delete Test
    def test_delete_mechanic(self):
        delete_payload = {
            "name": "",
            "email" : "",
            "phone" : "",
            "salary": 0,
            "password" : ""
        }

        headers = {'Authorization': "Bearer " + self.test_login_mechanic()}

        response = self.client.delete('/mechanics/delete', json=delete_payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    # Failed Delete Test
    def test_delete_mechanic_fail(self):
        delete_payload = {
            "name": "",
            "email" : "",
            "phone" : "",
            "salary": 0,
            "password" : ""
        }

        response = self.client.delete('/mechanics/delete', json=delete_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "You must be logged in to access") 
    

    # Successful Get/Display Test
    def test_display_mechanic_paginated(self):
    
        response = self.client.get("/mechanics/?page=1&per_page=5")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "test_user")

    # Successful Get/Search Test
    def test_search_mechanic(self):
        
        response = self.client.get("/mechanics/?search=test")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "test_user")
    
    # Successful Get/Display (Popular) Test
    def test_display_popular_mechanics(self):
        
        response = self.client.get("/mechanics/popular")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "test_user")



