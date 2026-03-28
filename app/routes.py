"""
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


@app.route("/api/register", methods=["POST"])
def api_register():

    from flask import request

    data = request.form  # because you're using FormData

    username = data.get("username")
    password = data.get("password")
    password2 = data.get("password2")

    if not username or not password:
        return jsonify({"error": "Missing fields"}), 400

    if password != password2:
        return jsonify({"error": "Passwords do not match"}), 400

    user = User(username=username, password=password)

    try:
        db.session.add(user)
        db.session.commit()
        return jsonify({"message": "Account created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Username already exists"}), 400

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

"""