from wtforms import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
class LoginForm(Form):
    username = StringField('', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('', validators=[DataRequired(message='请输入密码')])
