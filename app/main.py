import os
import requests
from flask import Blueprint, render_template, request
from flask_login import login_required, current_user


main = Blueprint("main", __name__)


# Constants for TMDB API
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

    def movie_recommendations(movie_id):
        return BASE_URL + "/movie/" + movie_id + "/recommendations?api_key=" + API_KEY

    def tv_details(tv_id):
        return BASE_URL + "/tv/" + tv_id + "?api_key=" + API_KEY

    def tv_providers(tv_id):
        return BASE_URL + "/tv/" + tv_id + "/watch/providers?api_key=" + API_KEY

    def tv_recommendations(tv_id):
        return BASE_URL + "/tv/" + tv_id + "/recommendations?api_key=" + API_KEY

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


@main.route("/")
def index():
    return render_template("index.html")


@main.route("/profile")
@login_required
def profile():
    return render_template("profile.html", name=current_user.name)


@main.route("/<menu_item>")
@login_required
def flixlist(menu_item):

    query = request.args.get("search")
    if query == None:
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


@main.route("/friendlist")
@login_required
def friendlist():
    rows = 3
    return render_template(
        "friendlist.html", title="Friend List", rows=rows, url=os.getenv("URL")
    )


@main.route("/recommendations")
@login_required
def recommendations():
    # TO DO - Asign user watched movies and TV shows from DB to respective varables this is a static example
    user_watched_movies = [45, 65, 12, 508943]
    user_watched_tv = [62, 82134]
    # =================================================================
    movies_data = []
    tv_data = []
    info_to_display = [
        "title",
        "release_date",
        "Movies",
        "name",
        "first_air_date",
        "TV Shows",
    ]

    # Get recommendations for each movie watched by the user
    for user_movie in user_watched_movies:
        response = requests.get(MovieRequest.movie_recommendations(str(user_movie)))
        try:
            movie_recommendations = response.json()["results"]
        except:
            movie_recommendations = []
        for recommendation in movie_recommendations:
            if int(recommendation["id"]) not in user_watched_movies:
                print(recommendation["id"])
                movies_data.append(recommendation)

    # Get recommendations for each tv show watched by the user
    for user_tv in user_watched_tv:
        response = requests.get(MovieRequest.tv_recommendations(str(user_tv)))
        try:
            tv_recommendations = response.json()["results"]
        except:
            tv_recommendations = []
        for recommendation in tv_recommendations:
            if int(recommendation["id"]) not in user_watched_tv:
                print(recommendation["id"])
                tv_data.append(recommendation)

    return render_template(
        "recommendations.html",
        title="Recommendations",
        movies_data=movies_data,
        tv_data=tv_data,
        url=os.getenv("URL"),
    )


@main.route("/details/<type>/<id>")
@login_required
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
