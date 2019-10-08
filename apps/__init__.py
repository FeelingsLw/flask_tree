from flask import Flask
from apps import config

app = Flask(__name__)
app.config.from_object(config)




from apps.user import user

app.register_blueprint(user)

from apps.qd import qd

app.register_blueprint(qd)