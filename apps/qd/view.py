from . import qd
from flask.views import MethodView
from flask import render_template, redirect, url_for, session
from apps.model import Qd, User
import datetime


class QdView(MethodView):
    def get(self):
        today = datetime.date.today()
        qds = Qd.query.filter_by(uid=session['uid'])
        t_qd = None
        if qds.first():
            if qds[0].create_time == today:
                t_qd = qds[0]
        user = User.query.filter_by(id=session['uid']).first()
        return render_template('qd/index.html', qds=qds, user=user, t_qd=t_qd,today=today)

    def post(self):
        pass


qd.add_url_rule('/qd/', view_func=QdView.as_view('qd'))
