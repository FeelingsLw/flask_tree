from apps.qd import qd
from flask.views import MethodView
from flask import render_template, redirect, url_for, session, request, jsonify
from apps.model import Qd, User, Clazz
import datetime
from apps.qd.forms import QdForm
from apps.model import db
from sqlalchemy import desc,text
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
class Charts(MethodView):
    def get(self):
        return render_template('data_analysis/index.html')
    def post(self):
        # 记录所有学生签到信息的集合
        all_code=[]
        # 获取所有学生
        users = User.query.filter_by(rid =1).all()
        #data =[]
        us =[]
        data = [d[0] for d in db.session.execute('select create_time FROM t_qd GROUP BY create_time ORDER BY create_time').cursor._rows]
        sql ='''
        SELECT 
            IFNULL(q2.code_num,0) as code_num
            FROM
                (SELECT create_time 
                FROM t_qd 
                GROUP BY create_time 
                ORDER BY create_time
                )q1
            
            left JOIN (select * from t_qd where uid ={} )  q2
            on q2.create_time = q1.create_time

        '''
    
        for u in users:
            us.append(u.nick_name)
            # 通过学生获取代码信息
            #qds = Qd.query.filter_by(uid=u.id)
            #all_code.append([qd.code_num for qd in qds])
            # data = [qd.create_time for qd in qds]
            
            code_nums =[c[0] if c[0] else 0 for c in db.session.execute(sql.format(u.id)).cursor._rows]
            all_code.append(code_nums)

        return jsonify({
            'user':us,
            'data':data,
            'code_num':all_code
        })




@qd.route('/search_qd/',methods=['POST'])
def search_qd():
    cname = request.form.get('cname')
    uname = request.form.get('uname')
    time = request.form.get('create_time')
    search = Qd.query.join(User).join(User.clazzs)

    User.query.from_statement(text('select * from t_user')).all()
    if time:
        search= search.filter(Qd.create_time==time)
    if uname:
        search = search.filter(User.nick_name==uname)
    if cname:
        search = search.filter(Clazz.name == cname)
    data = search.order_by(Qd.create_time.desc()).all()
    datas = []
    for d in data:
        cname = d.user.clazzs[0].name if len(d.user.clazzs)>0 else 'No Class'
        cid = d.user.clazzs[0].id if len(d.user.clazzs)>0 else 'No Class'
        uname = d.user.nick_name
        uid  = d.uid
        datas.append({
            'id': d.id,
            'uid': uid,
            'uname': uname,
            'cid': cid,
            'cname': cname,
            'stage': d.stage,
            'progress': d.progress,
            'code_num':d.code_num,
            'bug_num': d.bug_num,
            'create_time': d.create_time,
            'remarks': d.remarks
        })
    return jsonify({'data': datas})


qd.add_url_rule('/qd/', view_func=QdView.as_view('qd'))
qd.add_url_rule('/charts/', view_func=Charts.as_view('charts'))




