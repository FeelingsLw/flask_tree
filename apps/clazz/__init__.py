from flask import Blueprint

clazz = Blueprint('clazz',__name__,url_prefix='/clazz')

from . import view