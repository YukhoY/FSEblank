#coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.fields import html5, simple
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('密码', validators=[DataRequired(message='请输入密码')])

class SignupForm(FlaskForm):
    class Meta:
        locales = ['zh']
    username = StringField('用户名', validators=[DataRequired()], render_kw={'class': 'logininput'})
    email = html5.EmailField('邮箱', validators=[DataRequired(), Email('输入了无效的邮箱')])
    password = PasswordField('密码', validators=[DataRequired(), Length(min=6, max=18, message='密码长度需在6-18位之间')])
    password2 = PasswordField('确认密码', validators=[DataRequired(),EqualTo('password', '两次输入的密码不同')])
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        print('正在校验用户名')
        if user is not None:
            print('用户名已存在')
            raise ValidationError('这个用户名已经被注册过啦!')
        print('用户名校验完成')
    def validate_email(self, email):
        print('正在校验邮箱')
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            print('邮箱已存在')
            raise ValidationError('这个邮箱已经被注册过啦!')
        print('邮箱校验完成')
