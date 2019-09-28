from apps.stu import stu
from flask import render_template, request, redirect, url_for
from apps.model import  User

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

        user = User.query.filter_by(uname=uname,passwd=passwd).first()
        if user:

            return redirect(url_for('stu.index'))
        else:
            return redirect(url_for('login'))