import click
from flask import request, jsonify, Blueprint
from flask_login import login_user
from werkzeug.security import check_password_hash

from own_chat.db import db
from own_chat.user.models import User

blueprint = Blueprint("login", __name__)


@blueprint.cli.command("create_user")
@click.argument("username")
@click.argument("password")
def create_user_command(username, password):
    create_user(username, password)
    click.echo("User created successfully!")


@blueprint.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")

        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return jsonify({"message": "Login successful"})
        else:
            return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({"message": "Login required"}), 401


def create_user(username, password):
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
