import click
from flask import Flask, request, jsonify, Blueprint
from flask_login import LoginManager, login_user
from werkzeug.security import check_password_hash

from .models import db, User
from .routes import api

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///gpt.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

db.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


app.register_blueprint(api, url_prefix='/api')

bp = Blueprint('user', __name__)


@bp.cli.command('create_user')
@click.argument('username')
@click.argument('password')
def create_user_command(username, password):
    create_user(username, password)
    click.echo("User created successfully!")


app.register_blueprint(bp)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.json.get('username')
        password = request.json.get('password')

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({'message': 'Login successful'})
        else:
            return jsonify({'message': 'Invalid credentials'}), 401

    return jsonify({'message': 'Login required'}), 401


def create_user(username, password):
    with app.app_context():
        # Input validation
        if not username or not password:
            raise ValueError("All fields are required")

        # Check for existing user
        if User.query.filter_by(username=username).first():
            raise ValueError("Username already exists")

        user = User()
        user.username = username
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return True, "User created successfully!"
