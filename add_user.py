from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()

    username = input("Username: ")
    password = input("Password: ")

    if User.query.filter_by(username=username).first():
        print("User already exists!")
    else:
        db.session.add(User(username=username, password=password))
        db.session.commit()
        print("User added!")
