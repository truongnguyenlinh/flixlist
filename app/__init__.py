from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route("/flixlist")
def flixlist():
    rows = 10
    return render_template("flixlist.html", title="FlixList", rows=rows)

@app.route("/friendflix")
def friendflix():
    rows = 3
    return render_template("friendflix.html", title="FriendFlix", rows=rows)

@app.route("/recsflix")
def recsflix():
    rows = 3
    return render_template("recsflix.html", title="RecsFlix", rows=rows)
