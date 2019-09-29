from flask import Flask
from apps import config

app = Flask(__name__)
app.config.from_object(config)




from apps.stu import stu

app.register_blueprint(stu)
