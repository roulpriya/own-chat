from own_chat.app import app
from own_chat.user.models import db

if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
