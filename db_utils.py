import pymongo
from flask import g
id_key = 'id'
name_key = 'name'
address_key = 'address'


def get_all_users(ascending=pymongo.ASCENDING):
    db = g.default_db
    if ascending != pymongo.ASCENDING:
        ascending = pymongo.DESCENDING
    return db.users.find().sort([(id_key, ascending)])


def get_one_user(user_id):
    db = g.default_db
    return db.users.find_one({id_key: user_id})


def update_user(user_id, new_user):
    db = g.default_db
    db.users.update({id_key: user_id}, {'$set': new_user})


def add_user(new_user):
    db = g.default_db
    db.users.insert_one(new_user)


def remove_user(user_id):
    db = g.default_db
    db.users.remove({id_key: user_id})