from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired
class LoginForm(Form):
    username = StringField('username',validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('password', validators=[DataRequired(message='请输入密码')])
    remember_me = BooleanField('rem_me')
    submit = SubmitField('login')