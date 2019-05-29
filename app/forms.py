#coding: utf8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User

class LoginForm(FlaskForm):
    username = StringField('', validators=[DataRequired(message='请输入用户名')])
    password = PasswordField('', validators=[DataRequired(message='请输入密码')])

class SignupForm(FlaskForm):
    class Meta:
        locales = ['zh']
    username = StringField('', validators=[DataRequired()])
    email = StringField('', validators=[DataRequired(), Email()])
    password = PasswordField('', validators=[DataRequired()])
    password2 = PasswordField('', validators=[DataRequired(), EqualTo('password')])
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('这个用户名已经被注册过啦!')
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('这个邮箱已经被注册过啦!')
