from apps.stu import stu
from flask import render_template, request, redirect, url_for, session
from apps.model import User, db
from flask.views import MethodView


@stu.route('/index/')
def index():
    return render_template('index.html')


@stu.route('/login/', methods=['GET', 'POST'])
def login():
    if 'GET' == request.method:
        return render_template('login.html')
    else:
        uname = request.form['uname']
        passwd = request.form['passwd']

        user = User.query.filter_by(uname=uname).first()
        if user:
            if user.check_password(passwd):
                session['uid'] = user.id
                session['uname'] = user.uname
                return redirect(url_for('stu.index'))
            else:
                return render_template('login.html',msg='密码错误')
        else:
            return render_template('login.html', msg='用户名不存在')


class RegisterView(MethodView):
    def get(self):
        return render_template('register.html')

    def post(self):
        uname = request.form['uname']
        passwd = request.form['passwd']
        real_passwd = request.form['real_passwd']
        nick_name = request.form['nick_name']
        sex = request.form['sex']
        phone = request.form['phone']
        user = User.query.filter_by(uname=uname).first()
        if user:
            return render_template('register.html', msg='用户名已存在')
        else:
            user = User(uname, passwd, nick_name, sex, phone)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('stu.login'))


# 通过add_url_rule添加类视图和url的映射，并且在as_view方法中指定该url的名称，方便url_for函数调用
stu.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
