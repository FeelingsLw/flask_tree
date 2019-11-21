from apps import api
from flask import request,render_template,jsonify
from flask_restful import reqparse,Resource
from apps.model import Clazz
from . import clazz
@clazz.route('/')
def index():
    return render_template('clazz/index.html')

pareser = reqparse.RequestParser()
class ClazzList(Resource):
    def get(self):
        def remove(v):
            v.pop('_sa_instance_state')
            return v
        clazzs = [remove(c.__dict__) for c in Clazz.query.all()]
        return jsonify(clazzs)
class ClazzView(Resource):
    def get(self):
        clazzs = Clazz.query.all()
        return '',404
    def post(self):
        args= reqparse.parse_args()

api.add_resource(ClazzView,'/clazzs/')
api.add_resource(ClazzList,'/clazz_list/')
