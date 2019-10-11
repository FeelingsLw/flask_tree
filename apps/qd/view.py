from . import qd
from flask.views import MethodView
from flask import render_template, redirect, url_for, session, request, jsonify
from apps.model import Qd, User, Clazz
import datetime
from .forms import QdForm
from apps.model import db
from sqlalchemy import desc
from apps.decorators import login_required


class QdView(MethodView):
    decorators = [login_required]

    def get(self):
        u = User.query.filter_by(id=session['uid']).first()
        if u.rid == 1:
            today = datetime.date.today()
            qds = Qd.query.filter_by(uid=session['uid']).order_by(desc('create_time'))
            t_qd = None
            if qds.first():
                if qds[0].create_time == str(today):
                    t_qd = qds[0]
            return render_template('qd/index.html', qds=qds, user=u, t_qd=t_qd, today=today)
        else:
            qds = Qd.query.order_by(desc('create_time')).all()
            return render_template('qd/admin_index.html', qds=qds)

    def post(self):
        form = QdForm()

        if form.validate_on_submit():
            qd = Qd(uid=session['uid'], stage=form.stage.data, progress=form.stage.data, code_num=form.code_num.data,
                    bug_num=form.bug_num.data, create_time=form.create_time.data, remarks=form.remarks.data)
            db.session.add(qd)
            db.session.commit()
        return redirect(url_for('qd.qd'))


@qd.route('/search_qd/',methods=['POST'])
def search_qd():
    cname = request.form.get('cname')
    uname = request.form.get('uname')
    time = request.form.get('create_time')
    qds = Qd.query
    if time:
        qds= qds.filter_by(create_time=time)
    if uname:
        qds = qds.join(User).filter_by(nick_name=uname)
    if cname:
        qds = qds.join(Clazz).filter_by(name=cname)
    data = qds.order_by(desc('create_time')).all()
    datas = []
    for d in data:
        datas.append({
            'id': d.id,
            'uid': d.uid,
            'uname': d.user.nick_name,
            'cid': d.cid,
            'cname': d.clazz.name,
            'stage': d.stage,
            'progress': d.progress,
            'code_num':d.code_num,
            'bug_num': d.bug_num,
            'create_time': d.create_time,
            'remarks': d.remarks
        })
    return jsonify({'data': datas})


qd.add_url_rule('/qd/', view_func=QdView.as_view('qd'))
