from flask import Blueprint, render_template, session, redirect, url_for

main = Blueprint("main", __name__)

@main.route("/index")
def index():
    if 'username' in session:
        user = {"username": session['username']}
    else:
        user = {"username": "Guest"}

    return render_template("index.html", title="Home", user=user)


@main.route("/")
def home():
    return redirect(url_for("main.index"))