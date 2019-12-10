from flask import render_template, url_for, redirect, request, Blueprint, session
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message

from flask_app import db, bcrypt, mail
from flask_app.models import User, Post
from flask_app.users.forms import RegistrationForm, LoginForm, UpdateForm
import pyotp

users = Blueprint("users", __name__)


@users.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        otp_secret = pyotp.random_base32()
        hashed = bcrypt.generate_password_hash(opt_secret + form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed, opt_secret=opt_secret, is_confirmed=False)
        msg = Message("Please Confirm Your Account", sender="jjohnsonjjohnson123123@gmail.com", recipients=[form.email.data])
        msg.body="Please confirm your account at 127.0.0.1:5000/confirm_account/" + form.username.data
        mail.send(msg)
        db.session.add(user)
        db.session.commit()
        session['username'] = form.username.data
        return redirect(url_for('users.mfa_setup'))
    return render_template('register.html', title='Register', form=form)

@users.route("/mfa_setup", methods=["GET", "POST"])
def mfa_setup():
    if 'username' not in session:
        return redirect(url_for('users.register'))
    user = User.query.filter_by(username=session['username']).first()
    if 'username' is None:
        return redirect(url_for('users.register'))
    return render_template('mfa_setup.html', url=user.get_totop_uri()), 200, {
        'Cache-Control': 'no-cache, no-store, must-revalidate',
        'Pragma': 'no-cache',
        'Expires': '0'}

@users.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if not user.is_confirmed:
            return redirect(url_for('users.not_confirmed'))
        if user is not None and bcrypt.check_password_hash(user.opt_secret + user.password, user.opt_secret + form.password.data) and user.verify_totop(form.token.data):
            login_user(user)
            return redirect(url_for('users.account'))
    return render_template('login.html', form=form)

@users.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@users.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.password = bcrypt.generate_password_hash(current_user.opt_secret + form.password.data).decode('utf-8')
        db.session.commit()
        return redirect(url_for('users.account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.password.data = current_user.password

    return render_template('account.html', title='Account', form=form, current_user=current_user)

@users.route("/not_confirmed", methods=["GET"])
def not_confirmed():
    return render_template('not_confirmed.html', title='Not confirmed')

@users.route("/confirm_account/<user_name>", methods=["GET"])
def confirm_account(user_name):
    user = User.query.filter_by(username=user_name).first()
    if not user:
        return redirect(url_for('users.register'))
    user.is_confirmed = True
    db.session.commit()
    return redirect(url_for('users.account'))
