from app import create_app, db
from app.models import User

# Create app context so database operations work
app = create_app()

def remove_user(username):
    with app.app_context():
        user = User.query.filter_by(username=username).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f"User '{username}' has been removed.")
        else:
            print(f"User '{username}' not found.")

if __name__ == "__main__":
    username = input("Enter the username to remove: ")
    remove_user(username)
