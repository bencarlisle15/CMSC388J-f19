from flask_app import db
from datetime import datetime
from flask_app.utils import datetime_to_str
from copy import deepcopy

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(256), nullable=False, unique=True)
    posts = db.relationship('Post', backref='user', lazy=True)
    def __repr__(self):
        return '<Name %r>' % self.name

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    author = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(2048), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='post', lazy=True)
    def __repr__(self):
        return '<Post %r>' % self.title

class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(256), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.String(2048), nullable=False)
    post_title = db.Column(db.String(256), db.ForeignKey('post.id'), nullable=False)
    def __repr__(self):
        return '<Comment %r>' % self.content

def init_db():
    # db.drop_all(bind=None)
    # db.session.commit()
    db.create_all()

def get_all_posts():
     posts = Post.query.all()
     temp_posts = deepcopy(posts)
     for post in temp_posts:
         post.date = datetime_to_str(post.date)
         if len(post.content) > 250:
             post.content = post.content[:250] + "..."
     return temp_posts

def create_post(author, title, content, user_id):
     post = Post(author=author, title=title, content=content, user_id=user_id)
     db.session.add(post)
     db.session.commit()

def create_user(name, email):
    users = User.query.filter(User.email == email).all()
    if len(users) == 0:
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
    elif users[0].name !=name:
        return -1
    return User.query.filter(User.email == email).all()[0].id

def create_comment(post_title, author, content):
    comment = Comment(post_title=post_title, author=author, content=content)
    db.session.add(comment)
    db.session.commit()

def get_post(post_title):
    post = Post.query.filter(Post.title == post_title).all()[0]
    temp_post = deepcopy(post)
    temp_post.date = datetime_to_str(temp_post.date)
    return temp_post

def get_comments(post_title):
    comments = Comment.query.filter(Comment.post_title == post_title).all()
    temp_comments = deepcopy(comments)
    for comment in temp_comments:
         comment.date = datetime_to_str(comment.date)
    return temp_comments

def get_user(user_id):
    return User.query.filter(User.id == user_id).all()[0]

def get_posts(user_id):
    posts = Post.query.filter(Post.user_id == user_id).all()
    temp_posts = deepcopy(posts)
    for post in temp_posts:
        post.date = datetime_to_str(post.date)
        if len(post.content) > 250:
            post.content = post.content[:250] + "..."
    return temp_posts
