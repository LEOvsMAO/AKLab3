from flask import Flask, json, render_template, request, g
from db_utils import *
import pymongo

app = Flask(__name__)


def connect_to_db():
    client = pymongo.MongoClient('localhost', 27017)
    return client['test']


@app.before_request
def before_request():
    g.default_db = connect_to_db()


id_key = r'id'
name_key = r'name'
address_key = r'address'


@app.route('/')
def hello_world():
    return render_template('layout.html')


@app.route('/users')
def all_users():
    return render_template('users.html')


@app.route('/user/<int:id>')
def edit_user(id):
    return render_template('edit.html', id=id)


@app.route('/add')
def add_user():
    return render_template('add.html')


@app.route('/api/users')
def all_users_json():
    t = get_all_users()
    res = [{id_key: item[id_key], name_key: item[name_key], address_key: item[address_key]} for item in t]
    json_str = json.dumps(res)
    print("all users requested: ", json_str)
    return json_str


@app.route('/api/add', methods=['POST'])
def add():
    users = get_all_users(pymongo.DESCENDING)
    user = users[0]

    new_user = {
        id_key: user[id_key] + 1,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    }
    json_str = json.dumps(new_user)
    add_user(new_user)
    print("adding: ", new_user)
    return json_str


@app.route('/api/remove/<int:id>', methods=['POST'])
def remove(id):
    # db.users.delete_one({id_key: request.form[id_key]})
    print("removing: ", id)
    remove_user(id)
    return '', 204


@app.route('/api/edit/<int:id>', methods=['GET'])
def get_detail_info(id):
    t = get_one_user(id)
    res = {}
    for i in [id_key, name_key, address_key]:
        res[i] = t[i]
    json_str = json.dumps(res)
    print("get edit:", json_str)
    return json_str


@app.route('/api/edit/<int:id>', methods=['POST'])
def edit(id):
    new_user = {
        id_key: id,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    }
    json_str = json.dumps(new_user)

    print("post edit: ", new_user)
    return json_str


if __name__ == '__main__':
    app.run(debug=True)
