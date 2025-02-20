from flask_login import LoginManager

from own_chat.user.models import User

# login manager service for handling user authentication

login_manager = LoginManager()
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
