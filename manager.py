from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
from apps import app
from apps.model import db

manager = Manager(app)
migrate = Migrate(app, db)

manager.add_command('db', MigrateCommand)

'''
此文件用来管理数据库的表结构的创建与更新使用

# 初始化 数据库 版本文件 (执行命令后，会在项目跟目录生成migrations文件夹)
python manager.py db init

# 生成 数据库 表结构 文件
python manager.py db migrate

# 映射 表结构 到 数据库中
python manager.py db upgrade
'''

if __name__ == '__main__':
    manager.run()