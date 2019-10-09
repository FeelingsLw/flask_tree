from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class QdForm(FlaskForm):
    stage = StringField('阶段',validators=[DataRequired()])  # 阶段
    progress = StringField('进度',validators=[DataRequired()])  # 进度
    code_num = IntegerField('代码数',validators=[DataRequired()])  # 代码数
    bug_num = IntegerField('bug数',validators=[DataRequired()])  # bug数
    create_time = StringField('日期',validators=[DataRequired()])
    remarks = StringField()
