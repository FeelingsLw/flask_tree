from flask_sqlalchemy import SQLAlchemy
from apps import app

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(32))
    passwd = db.Column(db.String(32))
    sex = db.Column(db.String(1))
