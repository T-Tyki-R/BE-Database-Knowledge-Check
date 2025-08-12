# Imports
from application import create_app
from application.models import db, Consumer
from application.Utils.util import encode_token
import unittest


class TestConsumer(unittest.TestCase):
    def setUp(self):
        self.app = create_app("TestingConfig")
        self.consumer = Consumer(name="test_user", email="test@email.com",
                                  phone= "1231231234", password="test1")
        with self.app.app_context():
            db.drop_all()
            db.create_all()
            db.session.add(self.consumer)
            db.session.commit()
        self.token = encode_token(1)
        self.client = self.app.test_client()
    
    # Successful Creation Test
    def test_create_consumer(self):
        consumer_payload = {
            "name": "Naruto Uzumaki",
            "email" : "ichirakuramen1@email.com",
            "phone" : "0009990000",
            "password" : "fishCakeSpiral1"
        }

        response = self.client.post('/consumers/create', json= consumer_payload)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json['name'], "Naruto Uzumaki")

    # Failed Creation Test
    def test_create_consumer_fail(self):
        consumer_payload = {
            "name": "Naruto Uzumaki",
            "email" : "ichirakuramen1@email.com",
            "phone" : "0009990000"
            # password is missing for testing purposes
        }

        response = self.client.post('/consumers/create', json= consumer_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn(response.json['password'], "Missing field: Password")

    # Successful Login Test
    def test_login_consumer(self):
        credentials = {
            "email" : "test@email.com",
            "password" : "test1"
        }

        response = self.client.post('/consumers/login', json= credentials)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['status'], "success")
        return response.json['token']
    
    # Failed Login Test
    def test_login_consumer_fail(self):
        credentials = {
            "email" : "failure1@gmail.com",
            "password" : "test212"
        }

        response = self.client.post('/consumers/login', json= credentials)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "Invalid email or password")

    
    # Successful Update Test
    def test_update_consumer(self):
        update_payload = {
            "name": "Levi Ackerman",
            "email" : "test@email.com",
            "phone" : "",
            "password" : ""
        }

        headers = {'Authorization': "Bearer " + self.test_login_consumer()}

        response = self.client.put('/consumers/update', json=update_payload, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['name'], 'Levi Ackerman') 
        self.assertEqual(response.json['email'], 'test@email.com')    

    # Failed Update Test
    def test_update_consumer_fail(self):
        update_payload = {
            "name": "Levi Ackerman",
            "email" : "test@email.com",
            "phone" : "",
            "password" : ""
        }


        response = self.client.put('/consumers/update', json=update_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "You must be logged in to access")

    #Successful Delete Test
    def test_delete_consumer(self):
        delete_payload = {
            "name": "",
            "email" : "",
            "phone" : "",
            "password" : ""
        }

        headers = {'Authorization': "Bearer " + self.test_login_consumer()}

        response = self.client.delete('/consumers/delete', json=delete_payload, headers=headers)
        self.assertEqual(response.status_code, 200)

    # Failed Delete Test
    def test_delete_consumer_fail(self):
        delete_payload = {
            "name": "",
            "email" : "",
            "phone" : "",
            "password" : ""
        }

        response = self.client.delete('/consumers/delete', json=delete_payload)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json['message'], "You must be logged in to access") 
    

    # Successful Get/Display Test
    def test_display_consumer_paginated(self):
    
        response = self.client.get("/consumers/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json[0]["name"], "test_user")

