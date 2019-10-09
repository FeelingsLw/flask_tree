DEBUG = True
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = '123'
HOST = 'localhost'
PORT = 3306
DATABASE = 'flask_tree'

SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}?charset=utf8mb4".format(DIALECT, DRIVER, USERNAME, PASSWORD, HOST,
                                                                          PORT,
                                                                          DATABASE)
SQLALCHEMY_TRACK_MODIFICATIONS = False

import os

SECRET_KEY = os.urandom(16)
WTF_CSRF_SECRET_KEY = os.urandom(16)
