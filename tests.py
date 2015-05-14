from flask import json
from CALab3 import app, remove, default_db
import unittest


class Lab3Test(unittest.TestCase):
    def test_adding(self):
        prev_count = default_db.users.count()
        response = app.test_client().post('/api/add', data={'name': 'testAdd', 'address': 'NewStreet'})

        self.assertEqual(prev_count + 1, default_db.users.count())
        default_db.users.remove({'id': user_id_from_response(response)})

    def test_deleting(self):
        prev_count = default_db.users.count()
        response = app.test_client().post('/api/add', data={'name': 'testDelete', 'address': 'NewStreet'})

        remove(user_id_from_response(response))
        self.assertEqual(prev_count, default_db.users.count())

    def test_updating(self):
        add_response = app.test_client().post('/api/add', data={'name': 'testUpdateOld', 'address': 'NewStreet'})
        edit_data = {
            'name': 'testUpdateNew',
            'address': 'newAddress'
        }
        edit_post_response = app.test_client().post('api/edit/' + str(user_id_from_response(add_response)),
                                                    data=edit_data)
        edit_data['id'] = user_id_from_response(add_response)
        self.assertEqual(edit_post_response.data.decode(), json.dumps(edit_data))
        default_db.users.remove({'id': user_id_from_response(add_response)})

    def test_get_one_user(self):
        add_response = app.test_client().post('/api/add', data={'name': 'testGet', 'address': 'NewStreet'})
        get_response = app.test_client().get('/api/edit/' + str(user_id_from_response(add_response)))

        self.assertEqual(get_response.data.decode(), json.dumps({'id': user_id_from_response(add_response),
                                                                 'name': 'testGet', 'address': 'NewStreet'}))

        default_db.users.remove({'id': user_id_from_response(add_response)})


def user_id_from_response(response):
    import json

    response_dict = json.loads(response.data.decode())
    return response_dict['id']