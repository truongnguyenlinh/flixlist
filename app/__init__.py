from flask import Flask, escape, request, render_template

app = Flask(__name__)


@app.route("/flixlist/<menu_item>")
def flixlist(menu_item):
    rows = 10
    return render_template("flixlist.html", title="FlixList", menu_item=menu_item, rows=rows)
