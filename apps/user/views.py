import functools

from apps.user import user
from flask import render_template, request, redirect, url_for, session,flash,jsonify,current_app
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
        current_app.logger.info('{}：在尝试登录'.format(uname))
        user = User.query.filter_by(uname=uname).first()
        if user:
            if user.check_password(passwd):
                current_app.logger.info('{}：登录成功了'.format(uname))
                session['uid'] = user.id
                session['uname'] = user.uname
                session['nick'] = user.nick_name
                session['sex'] = user.sex
                return redirect(url_for('user.index'))
            else:
                flash('密码错误')
                return render_template('login.html', msg='密码错误')
        else:
            flash('用户名不存在！')
            return render_template('login.html', msg='用户名不存在')


@user.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('user.login'))


class RegisterView(MethodView):

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
            clazz = Clazz.query.filter_by(id=cid).first()
            user.clazzs.append(clazz)
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


@user.route('/get_user/')
@user.route('/get_user/<int:page>')
def get_user(page=1):
    pager = User.query.paginate(page,2)
    clazzs = Clazz.query.all()
    return render_template('user/manager.html', pager=pager, clazzs=clazzs)

@user.route('/reset_pwd/<int:uid>/')
def reset_pwd(uid=None):
    if uid:
        user =User.query.filter_by(id=uid).first()
        if user:
            user.passwd='123'
            db.session.commit()
    return redirect(url_for('user.get_user'))

@user.route('/change_user/',methods=['GET','POST'])
def change_user():
    data = request.form
    user = User.query.filter_by(id = data.get('uid')).first()
    user.rid = data.get('rid')
    user.nick_name = data.get('nick_name')
    user.sex = data.get('sex')
    user.clazzs = Clazz.query.filter_by(id = data.get('cid')).all()
 
    db.session.commit()
    return jsonify({'status':'1','msg':'更新成功！'})
    

# 通过add_url_rule添加类视图和url的映射，并且在as_view方法中指定该url的名称，方便url_for函数调用
user.add_url_rule('/register/', view_func=RegisterView.as_view('register'))
user.add_url_rule('/personal/', view_func=PersonalView.as_view('personal'))
