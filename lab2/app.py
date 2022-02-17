from flask import Flask, request, jsonify, json
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import (
    JWTManager,
    create_access_token,
    jwt_required,
    get_jwt_identity,
    create_refresh_token, get_jwt
)
from datetime import timedelta

DATABASE_URI =  'postgresql://postgres:colt1911@localhost:5432/flask'

app = Flask(__name__)

app.config['SECRET_KEY'] = "elsese1" 
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=2)
iwt = JWTManager(app)

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI


db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'User("{self.username}", "{self.email}")'


class Task(db.Model):
    __tablename__ = 'tasks'

    task_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String, unique=True, nullable=False)
    status = db.Column(db.String,  nullable=False)

    def __repr__(self):
        return f'Task("{self.title}")'



@app.route('/tasks', methods = ['GET','POST'])
@jwt_required()
def todolist():
    if request.method == 'GET':
        tasks = Task.query.all()
        result = []
        for task in tasks:
            dict={}
            dict['id'] = task.task_id
            dict['title'] = task.title
            dict['status'] = task.status
            result.append(dict)

        return jsonify({
            'tasks_list':result
        })


    if request.method == 'POST':
        id = request.json.get('id')
        title = request.json.get('title')
        status = request.json.get('status')

        task = Task(task_id=id, title=title, status=status)

        db.session.add(task)
        db.session.commit()

        return jsonify({
            "status":"success",
            "data" : f"{title} task added successfully"

        }), 201


@app.route('/tasks/<int:id>', methods=['PUT','GET','DELETE'])
@jwt_required()
def mod_task(id):
    task = Task.query.filter_by(task_id=id).first()

    if request.method == 'GET':
        dict = {}
        dict['id'] = task.task_id
        dict['title'] = task.title
        dict['status'] = task.status

        return jsonify({
            "tasks": dict
        })

    if request.method == 'PUT':
        # task.title = request.json.get('title')
        # task.status = request.json.get('status')

        data = json.loads(request.data)
        task.title = data['title']
        task.status = data['status']

        db.session.commit()

        return jsonify({
            "status": 'success',
            "data": 'task updated successfully'
        })

    if request.method == 'DELETE':
        db.session.delete(task)
        db.session.commit()

        return jsonify({
            "status": "success"
        })

@app.route('/user/<int:id>', methods=['PUT','GET','DELETE'])
@jwt_required()
def mod_user(id):
    user = User.query.filter_by(task_id=id).first()

    if request.method == 'GET':
        dict = {}
        dict['id'] = user.id
        dict['username'] = user.username
        dict['pass'] = user.password

        return jsonify({
            "user": dict
        })

    if request.method == 'PUT':
        # task.title = request.json.get('title')
        # task.status = request.json.get('status')

        data = json.loads(request.data)
        user.username = data['usernmae']
        user.password = data['pass']

        db.session.commit()

        return jsonify({
            "status": 'success',
            "data": 'user updated successfully'
        })

    if request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()

        return jsonify({
            "status": "success"
        })

@app.route('/users', methods = ['GET','POST'])
@jwt_required()
def adduser():
    if request.method == 'GET':
        users = User.query.all()
        result = []
        for user in users:
            dict={}
            dict['id'] = user.id
            dict['username'] = user.username
            dict['pass'] = user.password
            result.append(dict)

        return jsonify({
            'users':result
        })


    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('pass')

        user = User(username=username, password=password)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "status":"success",
            "data" : f"user {username} added successfully"

        }), 201


@app.route('/login', methods=['POST'])
def login():       
    username = request.json.get('username')
    password = request.json.get('password')
    user = User.query.filter_by(username=username , password=password).first()  
    
    if user:
        access_token = create_access_token(identity=username)
        
        return jsonify({
            'status': 'success',
            'data': {
                'access_token': access_token
            }
        })
    return jsonify({
        'status': 'Fail',
        'msg': 'username or password incorrect'
    })







db.create_all()

app.run(host='127.0.0.1', port=5000, debug=True)