from flask import Blueprint

user = Blueprint('user', __name__)

from apps.user import views
