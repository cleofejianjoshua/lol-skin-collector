from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from sqlalchemy.exc import IntegrityError


api = Blueprint("api", __name__, url_prefix="/api")

@api.route("/register", methods=["POST"])
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


@api.route("/user")
def user():
    from flask import session

    if "username" in session:
        return jsonify({"username": session["username"]})
    return jsonify({"username": "Guest"})

# login api not yet modified
@api.route("/login", methods=["GET", "POST"])
def login():

    data = request.form

    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing Fields"}), 400
    
    user = User.query.filter_by(username=username).first()

    if user and user.passwor == password:
        session["username"] = user.username
        return jsonify({
            "message": "Login Successful",
            "username": user.username
        }), 200
    
    return jsonify ({"error": "Invalid username or password"}), 400
