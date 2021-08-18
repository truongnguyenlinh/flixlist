from flask_login import UserMixin
from werkzeug.security import check_password_hash
from . import db

class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(60), index=True, unique=True)
    username = db.Column(db.String(60), index=True, unique=True)
    first_name = db.Column(db.String(60), index=True)
    last_name = db.Column(db.String(60), index=True)
    password = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError("password is not a readable attribute.")

    @password.setter
    def password(self, password):
        self.password = password

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return "<User: {}>".format(self.username)
