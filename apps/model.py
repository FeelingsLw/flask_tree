from flask_sqlalchemy import SQLAlchemy
from apps import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)
user_clazz = db.Table(
    't_user_class',
    db.Model.metadata,
    db.Column('id', db.INTEGER, primary_key=True, autoincrement=True),
    db.Column('uid', db.INTEGER, db.ForeignKey('t_user.id')),
    db.Column('cid', db.INTEGER, db.ForeignKey('t_class.id'))
)


class User(db.Model):
    __tablename__ = 't_user'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uname = db.Column(db.String(32))
    nick_name = db.Column(db.String(32))
    _passwd = db.Column(db.String(100))
    sex = db.Column(db.String(1))
    phone = db.Column(db.String(15))
    rid = db.Column(db.Integer)
    clazzs = db.relationship('Clazz', backref='users', secondary=user_clazz)

    def __init__(self, name, password, nick_name, sex=None, phone=None, cid=None):
        self.uname = name
        self.passwd = password
        self.sex = sex
        self.phone = phone
        self.nick_name = nick_name
        self.cid = cid

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


class Clazz(db.Model):
    __tablename__ = 't_class'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    name = db.Column(db.String(32))
    count = db.Column(db.INTEGER)


class Qd(db.Model):
    __tablename__ = 't_qd'
    id = db.Column(db.INTEGER, primary_key=True, autoincrement=True)
    uid = db.Column(db.INTEGER, db.ForeignKey('t_user.id'))
    cid = db.Column(db.INTEGER,db.ForeignKey('t_class.id'))
    user = db.relationship('User')
    clazz = db.relationship('Clazz')
    stage = db.Column(db.String(32))  # 阶段
    progress = db.Column(db.String(32))  # 进度
    code_num = db.Column(db.INTEGER)  # 代码数
    bug_num = db.Column(db.INTEGER)  # bug数
    create_time = db.Column(db.String(32))
    remarks = db.Column(db.String(300))

    def __str__(self):
        return "id:{} uid:{} stage:{} progress:{} bug_num:{} create_time:{} remarks:{}".format(self.id, self.uid,
                                                                                               self.stage,
                                                                                               self.progress,
                                                                                               self.bug_num,
                                                                                               self.create_time,
                                                                                               self.remarks)
