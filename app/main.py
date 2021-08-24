import os
import requests
from flask import Blueprint, render_template, request, url_for, redirect
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


@main.route("/")
def index():
    return redirect(url_for("auth.login", _external=True))


@main.route("/<menu_item>")
@login_required
def flixlist(menu_item):

    query = request.args.get("search")
    if query is None:
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
    rows = 3
    return render_template(
        "recommendations.html",
        title="Recommendations",
        rows=rows,
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
    except KeyError:
        providers = [{"provider_name": "Not found"}]

    return render_template(
        "show_details.html",
        title=movie[info_to_display[0]],
        id=id,
        movie=movie,
        info_to_display=info_to_display,
        providers=providers,
    )
