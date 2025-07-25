from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from app.models import User
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

bp = Blueprint('routes', __name__)

# -----------------
# HOMEPAGE
# -----------------
@bp.route('/')
def home():
    username = session.get('username')  # Retrieve username from session if logged in
    return render_template('home.html', username=username)

# -----------------
# LOGIN PAGE
# -----------------
@bp.route('/login_page')
def login_page():
    # If already logged in, redirect to home
    if 'username' in session:
        return redirect(url_for('routes.home'))
    return render_template('login.html')

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
        # Save username in session
        session['username'] = user.username
        return jsonify({"status": "success", "message": "Login successful", "redirect": url_for('routes.home')})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401

# -----------------
# LOGOUT
# -----------------
@bp.route('/logout')
def logout():
    session.pop('username', None)  # Remove username from session
    return redirect(url_for('routes.home'))

# -----------------
# REGISTRATION PAGE
# -----------------
@bp.route('/register_page')
def register_page():
    if 'username' in session:
        return redirect(url_for('routes.home'))
    return render_template('register.html')

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

    # Hash password and store new user
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"status": "success", "message": "User registered successfully", "redirect": url_for('routes.login_page')})
