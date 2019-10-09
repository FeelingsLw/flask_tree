import functools

from apps.user import user
from flask import render_template, request, redirect, url_for, session
from apps.model import User, db, Clazz
from flask.views import MethodView
from apps.decorators import login_required


@user.route('/index/')
@login_required
def index():
    return render_template('home.html')


@user.route('/login/', methods=['GET', 'POST'])
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
                session['nick'] = user.nick_name
                session['sex'] = user.sex
                return redirect(url_for('user.index'))
            else:
                return render_template('login.html', msg='密码错误')
        else:
            return render_template('login.html', msg='用户名不存在')


@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


class RegisterView(MethodView):
    decorators = [login_required, ]

    def get(self):
        clazz = Clazz.query.all()
        return render_template('register.html', clazz=clazz)

    def post(self):
        uname = request.form['uname']
        passwd = request.form['passwd']
        real_passwd = request.form['real_passwd']
        nick_name = request.form['nick_name']
        sex = request.form['sex']
        phone = request.form['phone']
        cid = request.form['cid']
        user = User.query.filter_by(uname=uname).first()
        if user:
            return render_template('register.html', msg='用户名已存在')
        else:
            user = User(uname, passwd, nick_name, sex, phone, cid)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('user.login'))


class PersonalView(MethodView):
    decorators = [login_required]
    def get(self):
        clazz = Clazz.query.all()
        user = User.query.filter_by(id=session['uid']).first()
        return render_template('user/personal.html', user=user, clazz=clazz)

    def post(self):
        uname = request.form['uname']
        nick_name = request.form['nick_name']
        sex = request.form['sex']
        phone = request.form['phone']
        cid = request.form['cid']
        user = User.query.filter_by(id=session['uid']).first()
        if user:
            user.uname = uname
            user.nick_name = nick_name
            user.sex = sex
            user.phone = phone
            user.cid = cid
            db.session.commit()
        return redirect(url_for('user.personal'))


# 通过add_url_rule添加类视图和url的映射，并且在as_view方法中指定该url的名称，方便url_for函数调用
user.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
user.add_url_rule('/personal/', view_func=PersonalView.as_view('personal'))
