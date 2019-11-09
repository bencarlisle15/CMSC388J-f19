from flask_app import app, db
from flask import render_template, request, redirect, url_for
from flask_app.models import *
from flask_app.forms import *

@app.route('/')
def index():
    return render_template('index.html', posts=get_all_posts(), form=PostForm())

@app.route('/submit_post', methods=['POST'])
def submit_post():
    if  PostForm().validate_on_submit():
        id = create_user(request.form.get("name"), request.form.get("email"))
        if id >= 0:
            create_post(request.form.get("name"), request.form.get("title"), request.form.get("content"), id)
    return redirect("/")

@app.route('/submit_comment/<post_title>', methods=['POST'])
def submit_comment(post_title):
    if  CommentForm().validate_on_submit():
        create_comment(post_title, request.form.get("name"),  request.form.get("content"))
    return redirect("/posts/" + post_title)

@app.route("/posts/<post_title>")
def post(post_title):
    return render_template('post.html', post=get_post(post_title), comments=get_comments(post_title), form=CommentForm())

@app.route("/<name>_<int:user_id>")
def profile(name, user_id):
    posts = get_posts(user_id)
    return render_template('user.html', user=get_user(user_id), posts=posts, number_of_posts=len(posts))
