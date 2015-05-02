from flask import Flask, json, render_template, request
from flask.ext.pymongo import PyMongo
import pymongo

app = Flask(__name__)
mongo = PyMongo(app)
client = pymongo.MongoClient('localhost', 27017)
db = client['test']
id_key = 'id'
name_key = 'name'
address_key = 'address'


@app.route('/')
def hello_world():
    return render_template('layout.html', message='some shitty messsage')


@app.route('/users')
def all_users():
    return render_template('users.html')


@app.route('/user/<int:id>')
def edit_user(id):
    return render_template('edit.html', id=id)


@app.route('/api/users')
def all_users_json():
    t = db.users.find()
    res = [{id_key: item[id_key], name_key:item[name_key], address_key: item[address_key]} for item in t]
    print(res)
    json_str = json.dumps(res)
    return json_str


@app.route('/api/add', methods=['POST'])
def add():
    db.users.insert_one({
        id_key: db.users.count() + 1,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    })


@app.route('/api/remove/<int:id>', methods=['POST'])
def remove(id):
    # db.users.delete_one({id_key: request.form[id_key]})
    db.users.remove({id_key: id})



@app.route('/api/edit/<int:id>', methods=['GET'])
def get_detail_info(id):
    t = db.users.find_one({id_key: id})
    res = {}
    for i in [id_key, name_key, address_key]:
        res[i] = t[i]
    json_str = json.dumps(res)
    return json_str


@app.route('/api/edit/<int:id>', methods=['POST'])
def edit(id):
    new_user = {
        id_key: id,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    }
    db.users.find_one_and_update({id_key: id}, new_user)
    return json.dumps(new_user)


if __name__ == '__main__':
    app.run()
