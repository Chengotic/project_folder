from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    # Ensure instance folder exists
    os.makedirs(app.instance_path, exist_ok=True)

    # Configure database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(app.instance_path, "data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Secret key for sessions
    app.secret_key = os.environ.get("SECRET_KEY", "change_this_secret")  # Use env var in production

    # Initialize database
    db.init_app(app)

    # Register routes blueprint
    from app.routes import bp as routes_bp
    app.register_blueprint(routes_bp)

    return app
