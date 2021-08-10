import os
from flask_login import UserMixin
from flask import Flask, escape, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object("config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_view = "auth.login"


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return "<User: {}>".format(self.username)


@login_manager.user_loader
def load_user(user_id):
    return Employee.query.get(int(user_id))


@app.route("/")
def home():
    return jsonify(hello="world")


@app.route("/flixlist/<menu_item>")
def flixlist(menu_item):
    rows = 10
    return render_template(
        "flixlist.html", title="FlixList", menu_item=menu_item, rows=rows
    )

@app.route("/friendlist")
def friendflix():
    rows = 3
    return render_template("friendflix.html", title="Friend List", rows=rows)

@app.route("/recommendations")
def recsflix():
    rows = 3
    return render_template("recommendations.html", title="Recommendations", rows=rows)


@app.route("/shows/<show_id>")
def show_details(show_id):
    return render_template("show_details.html", title=show_id, show_id=show_id)


@app.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run()
