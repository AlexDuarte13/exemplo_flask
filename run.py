from flask import Flask, render_template, url_for, request, session, redirect
from flask_pymongo import PyMongo
import bcrypt

#Install Flask
#pip install flask
#pip install flask_pymongo
#pip install bcrypt

#Tutorial Mongo
#use fotografia
#db.users.insert({"name":"alex", "password":"alex", "cep":"21741-200"})
#db.getCollection("users").find({})


app = Flask(__name__)

app.config['MONGO_DBNAME'] = 'fotografia'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/fotografia'

mongo = PyMongo(app)

@app.route('/')
def index():
    if 'username' in session:
        return 'You are logged in as ' + session['username']

    return render_template('index.html')

@app.route('/login', methods=['POST'])
def login():
    users = mongo.db.users
    login_user = users.find_one({'name' : request.form['username']})

    if login_user['name'] == 'alex':
            return "Usuario encontrado: " + login_user['name']

    return 'Invalid username/password combination'

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name' : request.form['username']})
        print(existing_user)

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name' : request.form['username'], 'password' : hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        
        return 'That username already exists!'

    return render_template('register.html')

if __name__ == '__main__':
    app.secret_key = 'mysecret'
    app.run(debug=True)