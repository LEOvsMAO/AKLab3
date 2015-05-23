from CALab3 import app, id_key, name_key, address_key
import db_utils
from flask import json
from mock import patch, call
import unittest


class Lab3Test(unittest.TestCase):
    @patch("db_utils.add_user")
    @patch("db_utils.get_all_users")
    def test_adding(self, mock_get_all_users, mock_add):
        mock_get_all_users.return_value = [{id_key: 2, name_key: 'n1', address_key: 'a1'},
                                           {id_key: 1, name_key: 'n2', address_key: 'a2'}]
        response = app.test_client().post('/api/add', data={name_key: 'testAdd', address_key: 'NewStreet'})
        print("add.call_args:", mock_add.call_args)
        print("all_users.call_args:", mock_get_all_users.call_args)
        assert mock_add.call_args == call({id_key: 3, name_key: 'testAdd', address_key: 'NewStreet'})

    @patch("db_utils.remove_user")
    def test_deleting(self, mock_remove_user):
        response = app.test_client().post('/api/remove/1')
        print("remove.call_args:", mock_remove_user.call_args)
        assert mock_remove_user.call_args == call(1)

    @patch("db_utils.update_user")
    def test_updating(self, mock_update_users):

        edit_data = {
            'name': 'testUpdateNew',
            'address': 'newAddress'
        }
        edit_post_response = app.test_client().post('api/edit/1', data=edit_data)
        edit_data['id'] = 1
        print("update.call_args:", mock_update_users.call_args)
        assert mock_update_users.call_args == call(1, edit_data)

    @patch("db_utils.get_one_user")
    def test_get_one_user(self, get_one_user_mock):
        get_one_user_mock.return_value = {id_key: '1', address_key: 'a1', name_key: 'n1'}
        get_response = app.test_client().get('/api/edit/1')
        print("one.call_args:", get_one_user_mock.call_args)
        assert get_one_user_mock.call_args == call(1)

    @patch("db_utils.get_all_users")
    def test_get_all_users(self, mock_all_users):
        users = [{id_key: 1, name_key: 'n1', address_key: 'a1'},
                 {id_key: 2, name_key: 'n2', address_key: 'a2'}]

        mock_all_users.return_value = users
        get_response = app.test_client().get('/api/users')
        print("all_users:", json.loads(get_response.data.decode()))
        assert json.loads(get_response.data.decode()), users