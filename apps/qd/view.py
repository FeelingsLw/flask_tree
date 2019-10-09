from . import qd
from flask.views import MethodView
from flask import render_template, redirect, url_for, session
from apps.model import Qd, User
import datetime
from .forms import QdForm
from apps.model import db
from sqlalchemy import desc
from apps.decorators import login_required

class QdView(MethodView):
    decorators=[login_required]
    def get(self):
        # form = QdForm()
        today = datetime.date.today()
        qds =Qd.query.filter_by(uid=session['uid']).order_by(desc('create_time'))
        t_qd = None
        if qds.first():
            if qds[0].create_time == str(today):
                t_qd = qds[0]
        user = User.query.filter_by(id=session['uid']).first()
        return render_template('qd/index.html', qds=qds, user=user, t_qd=t_qd, today=today)

    def post(self):
        form = QdForm()

        if form.validate_on_submit():
            qd = Qd(uid=session['uid'], stage=form.stage.data, progress=form.stage.data, code_num=form.code_num.data,
                    bug_num=form.bug_num.data, create_time=form.create_time.data, remarks=form.remarks.data)
            db.session.add(qd)
            db.session.commit()
        return redirect(url_for('qd.qd'))


qd.add_url_rule('/qd/', view_func=QdView.as_view('qd'))
