from flask import Blueprint

stu = Blueprint('stu', __name__)

from apps.stu import views
