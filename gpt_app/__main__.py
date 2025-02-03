from gpt_app.app import app
from gpt_app.models import db

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
