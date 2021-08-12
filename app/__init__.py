import os
import requests
from flask_login import UserMixin
from flask import Flask, escape, request, render_template, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Constants for TMDB API
# =====================================================
API_KEY = "2cdd90f4142bcd5916204135c23506df"
BASE_URL = "https://api.themoviedb.org/3"


class MovieRequest:
    TOP_RATED = (
        BASE_URL + "/movie/top_rated?api_key=" + API_KEY + "&language=en-US&page=1"
    )
    TOP_RATED_TV = (
        BASE_URL + "/tv/top_rated?api_key=" + API_KEY + "&language=en-US&page=1"
    )

    def movie_details(movie_id):
        return BASE_URL + "/movie/" + movie_id + "?api_key=" + API_KEY

    def movie_providers(movie_id):
        return BASE_URL + "/movie/" + movie_id + "/watch/providers?api_key=" + API_KEY

    def tv_details(tv_id):
        return BASE_URL + "/tv/" + tv_id + "?api_key=" + API_KEY

    def tv_providers(tv_id):
        return BASE_URL + "/tv/" + tv_id + "/watch/providers?api_key=" + API_KEY

    def search_movie(query):
        return (
            BASE_URL
            + "/search/movie?api_key="
            + API_KEY
            + "&language=en-US&query="
            + query
            + "&page=1"
        )

    def search_tv(query):
        return (
            BASE_URL
            + "/search/tv?api_key="
            + API_KEY
            + "&language=en-US&query="
            + query
            + "&page=1"
        )


# =====================================================

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

    # Check search button
    query = request.args.get("search")
    if query == None:
        # Get Movies/TV Shows info
        if menu_item == "Movies":
            response = requests.get(MovieRequest.TOP_RATED)
            info_to_display = ["title", "release_date", "Movies"]
        elif menu_item == "TV Shows":
            response = requests.get(MovieRequest.TOP_RATED_TV)
            info_to_display = ["name", "first_air_date", "TV Shows"]
    else:
        # Search
        if menu_item == "Movies":
            response = requests.get(MovieRequest.search_movie(query))
            info_to_display = ["title", "release_date", "Movies"]
        elif menu_item == "TV Shows":
            response = requests.get(MovieRequest.search_tv(query))
            info_to_display = ["name", "first_air_date", "TV Shows"]

    movies_data = response.json()
    movies_data = movies_data["results"]

    return render_template(
        "flixlist.html",
        title="FlixList",
        menu_item=menu_item,
        movies_data=movies_data,
        info_to_display=info_to_display,
    )


@app.route("/friendlist")
def friendflix():
    rows = 3
    return render_template("friendlist.html", title="Friend List", rows=rows)


@app.route("/recommendations")
def recsflix():
    rows = 3
    return render_template("recommendations.html", title="Recommendations", rows=rows)


@app.route("/details/<type>/<id>")
def details(type, id):

    # Get movies details and streming providers
    if type == "Movies":
        response = requests.get(MovieRequest.movie_details(id))
        providers = requests.get(MovieRequest.movie_providers(id))
        info_to_display = ["title", "release_date", "Movies"]
    elif type == "TV Shows":
        response = requests.get(MovieRequest.tv_details(id))
        providers = requests.get(MovieRequest.tv_providers(id))
        info_to_display = ["name", "first_air_date", "TV Shows"]
    movie = response.json()
    try:
        providers = providers.json()["results"]["US"]["flatrate"]
    except:
        providers = [{"provider_name": "Not found"}]

    return render_template(
        "show_details.html",
        title=movie[info_to_display[0]],
        id=id,
        movie=movie,
        info_to_display=info_to_display,
        providers=providers,
    )


@app.route("/login", methods=("GET", "POST"))
def login():
    return render_template("login.html", title="Login")


if __name__ == "__main__":
    app.run()
