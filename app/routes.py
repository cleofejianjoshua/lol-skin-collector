from flask import render_template, flash, redirect, url_for, session, jsonify
from app import app, db
from app.forms import LoginForm, RegistrationForm
from app.models import User
from sqlalchemy.exc import IntegrityError


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()

        if user and user.password == form.password.data:
            session['username'] = user.username
            flash("Login successful!")
            return redirect(url_for("index"))
        else:
            flash("Invalid username or password.")

    return render_template("login.html", title="Sign In", form=form)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            password=form.password.data
        )

        try:
            db.session.add(user)
            db.session.commit()
            flash("Account created successfully!")
            return redirect(url_for("login"))
        except IntegrityError:
            db.session.rollback()
            flash("Username already exists. Please choose another.", "error")

    return render_template("register.html", title="Register", form=form)

@app.route("/logout")
def logout():
    session.pop('username', None)
    flash("You have been logged out.")
    return redirect(url_for("index"))

@app.route("/index")
def index():
    if 'username' in session:
        user = {"username": session['username']}
    else:
        user = {"username": "Guest"}

    return render_template("index.html", title="Home", user=user)

@app.route("/") 
def home():
    return redirect(url_for("index"))

@app.route("/api/user")
def user():
    if "username" in session:
        return jsonify({"username": session["username"]})
    return jsonify({"username": "Guest"})