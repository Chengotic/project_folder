from flask import Blueprint, request, jsonify, render_template
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)

# -----------------
# LOGIN PAGE
# -----------------
@bp.route('/')
def index():
    return render_template('index.html')   # serves login page

# -----------------
# LOGIN API
# -----------------
@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json(silent=True) or {}
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.args.get('username')
        password = request.args.get('password')

    if not username or not password:
        return jsonify({"status": "fail", "message": "Missing username or password"}), 400

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

# -----------------
# REGISTRATION PAGE
# -----------------
@bp.route('/register_page')
def register_page():
    return render_template('register.html')  # create this template

# -----------------
# REGISTRATION API
# -----------------
@bp.route('/register', methods=['POST'])
def register():
    data = request.get_json(silent=True) or {}
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "fail", "message": "Missing username or password"}), 400

    # Check if username already exists
    if User.query.filter_by(username=username).first():
        return jsonify({"status": "fail", "message": "User already exists"}), 409

    # Create hashed password
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully"})
