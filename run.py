from app import create_app, db
from app.models import User  # Must import models before create_all

app = create_app()

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Creates the User table in data.db
    app.run(host="0.0.0.0", port=5000, debug=True)