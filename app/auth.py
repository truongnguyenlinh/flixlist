from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db


auth = Blueprint("auth", __name__)


@auth.route("/login")
def login():
    return render_template("login.html", title="Login")


@auth.route('/login', methods=["POST"])
def login_post():
    username = request.form.get('username')
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    error = None

    if not user or not user.verify_password(password):
        flash("Please check your login details and try again.")
        return redirect(url_for('auth.login', _external=True))

    if error:
        return error, 418
    else:
        return redirect("/", url=os.getenv("URL"))


@auth.route("/register")
def register():
    return render_template("register.html")


@auth.route("/register", methods=["POST"])
def register_post():
    username = request.form.get("username")
    password = request.form.get("password")
    user = User.query.filter_by(username=username).first()
    error = None

    if user: 
        flash('Email address already exists')
        return redirect(url_for('auth.register', _external=True))
    elif not username:
        error = "Please enter a valid username."
    elif not password:
        error = "Please enter a valid password."

    if error:
        return error, 418
    else:
        new_user = User(
            email=email, 
            username=username, 
            password_hash=generate_password_hash(password))
            # TODO: add fields for first_name and user_name columns


        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for("auth.login", _external=True))


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index", _external=True))
