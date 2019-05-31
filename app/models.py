#coding: utf8
from app import db, lm
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(120), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    comments = db.relationship('Comment', backref='author', lazy='dynamic')
    strategies = db.relationship('Strategy', backref='author', lazy='dynamic')

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % (self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    body = db.Column(db.String(10000))
    timestamp = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    comments = db.relationship('Comment', backref='originpost', lazy='dynamic')
    def __repr__(self):
        return '<Post %r>' % (self.body)

class Comment(db.Model):
    __tablename__ = 'comment'
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(1000))
    timestamp = db.Column(db.String(100))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'))

    def __repr__(self):
        return '<Comment %r>' % (self.body)

class News(db.Model):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key = True)
    timestamp = db.Column(db.String(100))
    title = db.Column(db.String(100))
    body = db.Column(db.String(10000))
    author = db.Column(db.String(100))

    def __repr__(self):
        return '<News %r>' % (self.body)

class Strategy(db.Model):
    __tablename__ = 'strategy'
    id = db.Column(db.Integer, primary_key = True)
    strname = db.Column(db.String(1000))
    filename = db.Column(db.String(1000))
    time = db.Column(db.String(1000))
    result = db.Column(db.String(1000))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self):
        return '<Strategy %r>' % (self.body)

