from flask import Blueprint, jsonify, session

main = Blueprint("main", __name__)

@main.route("/")
def home():
    username = session.get("username", "Guest")
    return jsonify({"username": username})