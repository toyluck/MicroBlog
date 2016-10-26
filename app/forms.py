# 导入 From
from flask_wtf import Form
# 导入String 和 Boolean 两种Field ，用来记录用户的行为
from wtforms import StringField, BooleanField
# 确定是否数据的有效,对表单进行数据过滤
from wtforms.validators import DataRequired


class LoginForm(Form):
    openid = StringField("openid", validators=[DataRequired()])
    remember_me = BooleanField('remember_me', default=False)

