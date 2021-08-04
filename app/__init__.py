from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route("/flixlist")
def flixlist():
    rows = 10
    return render_template("flixlist.html", title="FlixList", rows=rows)
