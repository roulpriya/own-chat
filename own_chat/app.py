from flask import Flask

from own_chat import config
from own_chat.chats.routes import blueprint as chat_blueprint
from own_chat.db import db
from own_chat.login_manager import login_manager
from own_chat.user.routes import blueprint as user_blueprint

app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)
login_manager.init_app(app)

app.register_blueprint(chat_blueprint, url_prefix="/api/chats")
app.register_blueprint(user_blueprint, url_prefix="/api/login")
