from flask import Flask, json, render_template, request
import pymongo

app = Flask(__name__)
client = pymongo.MongoClient('localhost', 27017)
default_db = client['test']
id_key = 'id'
name_key = 'name'
address_key = 'address'


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
def all_users_json(db=default_db):
    t = db.users.find().sort(id_key)
    res = [{id_key: item[id_key], name_key:item[name_key], address_key: item[address_key]} for item in t]
    json_str = json.dumps(res)
    print("all users requested: ", json_str)
    return json_str


@app.route('/api/add', methods=['POST'])
def add(db=default_db):
    users = db.users.find().sort([(id_key, pymongo.DESCENDING)])
    user = users[0]
    print("adding: ", user)
    db.users.insert_one({
        id_key: user[id_key] + 1,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    })


@app.route('/api/remove/<int:id>', methods=['POST'])
def remove(id, db=default_db):
    # db.users.delete_one({id_key: request.form[id_key]})
    print("removing: ", id)
    db.users.remove({id_key: id})



@app.route('/api/edit/<int:id>', methods=['GET'])
def get_detail_info(id, db=default_db):
    t = db.users.find_one({id_key: id})
    res = {}
    for i in [id_key, name_key, address_key]:
        res[i] = t[i]
    json_str = json.dumps(res)
    print("get edit:", json_str)
    return json_str


@app.route('/api/edit/<int:id>', methods=['POST'])
def edit(id, db=default_db):
    new_user = {
        id_key: id,
        name_key: request.form[name_key],
        address_key: request.form[address_key]
    }

    db.users.update({id_key: id}, {'$set': new_user})
    print("post edit: ", new_user)
    return json.dumps(new_user)


if __name__ == '__main__':
    app.run(debug=True)
