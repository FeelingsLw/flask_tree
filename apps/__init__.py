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


from logging.config import dictConfig

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

from apps import filter
from flask_restful import Api

api = Api(app)
from apps.clazz import clazz
app.register_blueprint(clazz)




