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

# login api
@api.route("/login", methods=["POST"])
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
@api.route("/logout", methods=["POST"])
def api_logout():
    session.pop("username", None)
    return jsonify({"message": "Logged out"})

# Profile page api
@api.route("/user", methods=["GET"])
def get_user():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.filter_by(username=session["username"]).first()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "username": user.username,
        "nickname": user.nickname,
        "email": user.email,
        "favorite_skin": user.favorite_skin,
        "skin_image": user.skin_image
    })

# update profile api
@api.route("/update-profile", methods=["POST"])
def update_profile():
    from flask import session, request

    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401

    user = User.query.filter_by(username=session["username"]).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    nickname = request.form.get("nickname")
    email = request.form.get("email")

    if not nickname or not email:
        return jsonify({"error": "All fields are required"}), 400

    try:
        user.nickname = nickname
        user.email = email
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile"}), 500

