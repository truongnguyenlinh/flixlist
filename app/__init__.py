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
        raise AttributeError('password is not a readable attribute.')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

#    def __init__(self, username, password):
#        self.username = username
#        self.password = password

    def __repr__(self):
        return '<User: {}>'.format(self.username)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route("/")
def home():
    return jsonify(hello="world")

@app.route("/flixlist/<menu_item>")
def flixlist(menu_item):
    rows = 10
    return render_template("flixlist.html", title="FlixList", menu_item=menu_item, rows=rows)

@app.route("/friendlist")
def friendlist():
    rows = 3
    return render_template("friendlist.html", title="Friend List", rows=rows, url=os.getenv("URL"))

@app.route("/recommendations")
def recommendations():
    rows = 3
    return render_template("recommendations.html", title="Recommendations", rows=rows, url=os.getenv("URL"))

@app.route("/health")
def health():
    return ""

@app.route("/register", methods=("GET", "POST"))
# /register
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        error = None

        if not username:
            error = "Please enter a valid username."
        elif not password:
            error = "Please enter a valid password."
        elif User.query.filter_by(username=username).first() is not None:
            error = f"User {username} is taken!"

        if error is None:
            new_user = User(username, generate_password_hash(password)) # password
            db.session.add(new_user)
            db.session.commit()
            return f"User {username} created."
        else:
            return error, 418

    return render_template("register.html", url=os.getenv("URL"))
    # register.html

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get("password")
        error = None
        user = User.query.filter_by(username=username).first()

        if user is None:
            error = "Incorrect username."
        elif not check_password_hash(user["password"], password): # verify_password
            error = "Incorrect password. Please try again."

        if error is None:
            return "Login Successful", 200
        else:
            return error, 418

    return render_template("login.html", url=os.getenv("URL"))

if __name__ == "__main__":
    app.run()
    # add to wsgi.py