from flask import Flask, escape, request, render_template,

app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        "index.html", title="Home"
    )

@app.route('/flixlist')
def flixlist():
    return render_template(
        "flixlist.html", title="FlixList"
    )