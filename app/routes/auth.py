from flask import Blueprint, render_template, flash, redirect, url_for, session
from app.forms import LoginForm
from app.models import User

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            session['username'] = user.username
            flash("Login successful!")
            return redirect(url_for("main.index"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html", title="Sign In", form=form)


@auth.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for("main.index"))