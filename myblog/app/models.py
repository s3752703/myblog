from datetime import datetime
from enum import unique
from modulefinder import IMPORT_NAME
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import db,login
from hashlib import md5
from flask import Flask
from flask_robohash import Robohash

followers = db.Table('follwers', 
    db.Column('follower_id',db.Integer,db.ForeignKey('user.id')),
    db.Column('followed_id',db.Integer,db.ForeignKey('user.id'))
)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    username = db.Column(db.String(120), index=True, unique=True)
    aboutMe = db.Column(db.String(200))
    lastSeen = db.Column(db.DateTime,default = datetime.utcnow)
    password_hash = db.Column(db.String(128))
    email = db.Column(db.String(120), index=True, unique=True)
    followed = db.relationship('User',secondary = followers,
        primaryjoin = (followers.c.follower_id == id),
        secondaryjoin = (followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )
    images = db.relationship('Images',backref='author',lazy='dynamic')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    def set_p(self,password):
        self.password_hash = generate_password_hash(password)
    def check_p(self,password):
        return check_password_hash(self.password_hash,password)
    def get_user_post(self):
        return self.posts
    def profile_pic(self,size):
        awesome_app = Flask('awesome_app')
        robohash = Robohash()
        robohash.init_app(awesome_app)
        robohash = Robohash(app=awesome_app,x=size,y=size,hash_algorithm='md5')
        return robohash(self.username.lower())
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id == user.id).count() > 0
    
    def followed_posts(self):
        followed = Post.query.join(
            followers, (followers.c.followed_id == Post.user_id)).filter(
                followers.c.follower_id == self.id)
        own = Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Post {}>'.format(self.body)
class Images(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_uri = db.Column(db.String(400))
@login.user_loader
def load_u(id):
    return User.query.get(int(id))

