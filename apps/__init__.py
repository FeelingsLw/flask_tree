from flask import Flask
from apps import config

from flask_wtf import CSRFProtect

app = Flask(__name__)
app.config.from_object(config)

CSRFProtect(app)

from apps.user import user

app.register_blueprint(user)

from apps.qd import qd

app.register_blueprint(qd)
