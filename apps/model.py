from flask_sqlalchemy import SQLAlchemy
from apps import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(32))
    nick_name = db.Column(db.String(32))
    _passwd = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    phone = db.Column(db.String(15))

    def __init__(self, name, password, nick_name, sex=None, phone=None):
        self.uname = name
        self.passwd = password
        self.sex = sex
        self.phone = phone
        self.nick_name = nick_name

    @property
    def passwd(self):
        return self._passwd

    # 定义一个赋值的方法
    @passwd.setter
    def passwd(self, rawpwd):
        self._passwd = generate_password_hash(rawpwd)

    # 定义一个验证密码的方法
    def check_password(self, rawpwd):
        return check_password_hash(self.passwd, rawpwd)
