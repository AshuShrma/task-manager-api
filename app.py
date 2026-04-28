from models import db, User, Task
from flask import Flask, request, jsonify
from models import db, User
from flask_bcrypt import Bcrypt

app = Flask(__name__)   # ✅ MUST be here FIRST

app.config['SECRET_KEY'] = 'secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db.init_app(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    return "Task Manager API Running"

# after app = Flask(__name__)

# 🔐 Register API
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    username = data['username']
    email = data['email']
    password = data['password']

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    new_user = User(username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"})

# 🔐 Login API
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()

    if user and bcrypt.check_password_hash(user.password, password):
        return jsonify({"message": "Login successful"})
    else:
        return jsonify({"message": "Invalid credentials"}), 401

@app.route('/add_task', methods=['POST'])
def add_task():
    data = request.get_json()

    title = data['title']
    user_id = data['user_id']

    new_task = Task(title=title, user_id=user_id)

    db.session.add(new_task)
    db.session.commit()

    return jsonify({"message": "Task added successfully"})
# 📋 Get Tasks API
@app.route('/tasks/<int:user_id>', methods=['GET'])
def get_tasks(user_id):
    tasks = Task.query.filter_by(user_id=user_id).all()

    result = []
    for task in tasks:
        result.append({ 
            "id": task.id,
            "title": task.title,
            "completed": task.completed
        })

    return jsonify(result)

@app.route('/delete_task/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if not task:
        return jsonify({"message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({"message": "Task deleted successfully"})
if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000)
