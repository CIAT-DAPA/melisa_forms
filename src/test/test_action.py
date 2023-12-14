import unittest
from flask import Flask
from mongoengine import connect, disconnect
import os, sys
sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
# Import the Flask application from your app.py file
from app import app

class TestActionsBlueprint(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        disconnect(alias='default')
        
        self.db_name = 'testdb'
        connect(self.db_name, host='mongomock://localhost')

    def tearDown(self):
        disconnect(alias=self.db_name)

    def test_show_actions(self):
        response = self.client.get('/actions')
        self.assertEqual(response.status_code, 401)



if __name__ == '__main__':
    unittest.main()