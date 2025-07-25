from flask import Blueprint, request, jsonify, render_template
from app.models import User

bp = Blueprint('routes', __name__)

@bp.route('/')
def index():
    return render_template('index.html')   # serves the login page

@bp.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
    else:
        username = request.args.get('username')
        password = request.args.get('password')

    user = User.query.filter_by(username=username, password=password).first()

    if user:
        return jsonify({"status": "success", "message": "Login successful"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials"}), 401
