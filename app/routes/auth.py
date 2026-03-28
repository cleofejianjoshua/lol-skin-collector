from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from sqlalchemy.exc import IntegrityError


auth = Blueprint("auth", __name__, url_prefix="/auth")

#register api
@auth.route("/register", methods=["POST"])
def api_register():
    data = request.form

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

# login api
@auth.route("/login", methods=["POST"])
def api_login():
    data = request.form

    username = data.get("username")
    password = data.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.password == password:
        session["username"] = user.username
        return jsonify({"message": "Login successful"})

    return jsonify({"error": "Invalid username or password"}), 401

# logout api
@auth.route("/logout", methods=["POST"])
def api_logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out"})