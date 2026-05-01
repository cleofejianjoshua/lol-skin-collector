from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User
from sqlalchemy.exc import IntegrityError


api = Blueprint("api", __name__, url_prefix="/api")

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
    
#dashboard api
@api.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"message": "Welcome to your dashboard"})