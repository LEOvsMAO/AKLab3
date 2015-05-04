from flask import json

__author__ = 'dasd'

from mock import Mock
from CALab3 import app, add, remove, edit, all_users_json, default_db
import unittest


class Lab3Test(unittest.TestCase):
    def test_adding(self):
        prev_count = default_db.users.count()
        response = app.test_client().post('/api/add', data={'name': 'John', 'address': 'NewStreet'})
        self.assertEqual(prev_count + 1, default_db.users.count())
        default_db.users.remove({'id': prev_count})

    def test_deleting(self):
        prev_count = default_db.users.count()
        response = app.test_client().post('/api/add', data={'name': 'John', 'address': 'NewStreet'})
        remove(prev_count + 1)
        self.assertEqual(prev_count, default_db.users.count())

    def test_updating(self):
        prev_count = default_db.users.count()
        add_response = app.test_client().post('/api/add', data={'name': 'John', 'address': 'NewStreet'})
        edit_data = {
            'name': 'newName',
            'address': 'newAddress'
        }
        edit_post_response = app.test_client().post('api/edit/' + str(prev_count + 1), data=edit_data)
        edit_data['id'] = prev_count + 1
        self.assertEqual(edit_post_response.data, json.dumps(edit_data))

    def test_get_all_users(self):
        pass

    def test_get_one_user(self):
        prev_count = default_db.users.count()
        add_response = app.test_client().post('/api/add', data={'name': 'John', 'address': 'NewStreet'})
        get_response = app.test_client().get('/api/edit/' + str(prev_count + 1))
        self.assertEqual(get_response.data, json.dumps({'id': prev_count + 1, 'name': 'John', 'address': 'NewStreet'}))