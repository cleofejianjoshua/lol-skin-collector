from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Skin, UserCollection
import random

api = Blueprint("api", __name__, url_prefix="/api")


# Auth helpers

def get_current_user():
    """Return the logged-in User object or None."""
    if "username" not in session:
        return None
    return User.query.filter_by(username=session["username"]).first()


# User / Profile

@api.route("/user", methods=["GET"])
def get_user():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    return jsonify({
        "username": user.username,
        "nickname": user.nickname,
        "email":    user.email,
    })


@api.route("/update-profile", methods=["POST"])
def update_profile():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    nickname = request.form.get("nickname")
    email    = request.form.get("email")

    if not nickname or not email:
        return jsonify({"error": "All fields are required"}), 400

    try:
        user.nickname = nickname
        user.email    = email
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to update profile"}), 500


@api.route("/dashboard", methods=["GET"])
def dashboard():
    if "username" not in session:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"message": "Welcome to your dashboard"})


# Skins

@api.route("/skins", methods=["GET"])
def get_skins():
    """Return all skins in the pool."""
    skins = Skin.query.all()
    return jsonify([s.to_dict() for s in skins])


# Collection

@api.route("/collection", methods=["GET"])
def get_collection():
    """Return the current user's collected skins."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    entries = UserCollection.query.filter_by(user_id=user.id)\
                .order_by(UserCollection.obtained_at.desc()).all()
    return jsonify([e.to_dict() for e in entries])


# Gacha Pull

# Rarity weights: Ultimate 1%, legendary 9%, epic 18%, rare 32%, common 40%
RARITY_WEIGHTS = {
    "ultimate":  1,
    "legendary": 9,
    "epic":      18,
    "rare":      32,
    "common":    40,
}


def pick_rarity():
    rarities = list(RARITY_WEIGHTS.keys())
    weights  = list(RARITY_WEIGHTS.values())
    return random.choices(rarities, weights=weights, k=1)[0]


@api.route("/gacha/pull", methods=["POST"])
def gacha_pull():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    all_skins = Skin.query.all()
    if not all_skins:
        return jsonify({"error": "No skins available in the pool yet."}), 404

    rarity = pick_rarity()
    pool   = [s for s in all_skins if s.rarity.rarity_name == rarity]
    if not pool:
        pool = all_skins  # fallback

    skin = random.choice(pool)

    existing = UserCollection.query.filter_by(user_id=user.id, skin_id=skin.id).first()

    if existing:
        existing.duplicate_count += 1
        is_duplicate = True
    else:
        db.session.add(UserCollection(user_id=user.id, skin_id=skin.id))
        is_duplicate = False

    db.session.commit()

    return jsonify({
        "skin":         skin.to_dict(),
        "is_duplicate": is_duplicate,
    })


# Seed skins (dev helper)

@api.route("/skins/seed", methods=["POST"])
def seed_skins():
    """
    Dev-only endpoint to seed the skins table with sample data.
    POST /api/skins/seed
    """
    sample_skins = [
        {"name": "Base Ahri",            "champion": "Ahri",    "rarity": "common",    "image_path": "/images/skins/champions/ahri/default.jpg"},
        {"name": "Spirit Blossom Ahri",  "champion": "Ahri",    "rarity": "legendary", "image_path": "/images/skins/champions/ahri/spirit_blossom.jpg"},
        {"name": "Base Jinx",            "champion": "Jinx",    "rarity": "common",    "image_path": "/images/skins/champions/jinx/default.jpg"},
        {"name": "Arcane Jinx",          "champion": "Jinx",    "rarity": "epic",      "image_path": "/images/skins/champions/jinx/arcane.jpg"},
        {"name": "Base Lux",             "champion": "Lux",     "rarity": "common",    "image_path": "/images/skins/champions/lux/default.jpg"},
        {"name": "Elementalist Lux",     "champion": "Lux",     "rarity": "legendary", "image_path": "/images/skins/champions/lux/elementalist.jpg"},
        {"name": "Base Ezreal",          "champion": "Ezreal",  "rarity": "common",    "image_path": "/images/skins/champions/ezreal/default.jpg"},
        {"name": "Pulsefire Ezreal",     "champion": "Ezreal",  "rarity": "epic",      "image_path": "/images/skins/champions/ezreal/pulsefire.jpg"},
        {"name": "Star Guardian Lux",    "champion": "Lux",     "rarity": "rare",      "image_path": "/images/skins/champions/lux/star_guardian.jpg"},
        {"name": "Bewitching Jinx",      "champion": "Jinx",    "rarity": "rare",      "image_path": "/images/skins/champions/jinx/bewitching.jpg"},
    ]

    added = 0
    for s in sample_skins:
        exists = Skin.query.filter_by(name=s["name"]).first()
        if not exists:
            db.session.add(Skin(**s))
            added += 1

    db.session.commit()
    return jsonify({"message": f"Seeded {added} skins."})