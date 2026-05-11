from flask import Blueprint, request, jsonify, session
from app import db
from app.models import User, Skin, UserCollection, DisplaySlot
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
        "essence":  user.essence,
        "gold":     user.gold,
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

# Collection Disenchant

@api.route("/collection/disenchant/<int:collection_id>", methods=["DELETE"])
def disenchant_skin(collection_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    entry = UserCollection.query.filter_by(id=collection_id, user_id=user.id).first()
    if not entry:
        return jsonify({"error": "Skin not found in collection"}), 404

    disenchant_value = entry.skin.rarity.disenchant_value

    if entry.duplicate_count > 0:
        entry.duplicate_count -= 1
    else:
        db.session.delete(entry)

    user.essence = (user.essence or 0) + disenchant_value

    try:
        db.session.commit()
        return jsonify({
            "message": "Skin disenchanted",
            "essence": user.essence
        })
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to disenchant skin"}), 500


# Gold

@api.route("/gold", methods=["GET"])
def get_gold():
    """Return the current user's gold balance."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({"gold": user.gold or 0})


@api.route("/gold/add", methods=["POST"])
def add_gold():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    data   = request.get_json(silent=True) or {}
    amount = int(data.get("amount", 1))
    if amount < 1:
        return jsonify({"error": "Amount must be at least 1"}), 400

    user.gold = (user.gold or 0) + amount

    try:
        db.session.commit()
        return jsonify({"gold": user.gold})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to add gold"}), 500


@api.route("/gold/spend", methods=["POST"])
def spend_gold():
    """Spend gold from the current user's balance."""
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    data   = request.get_json(silent=True) or {}
    amount = int(data.get("amount", 0))
    if amount < 1:
        return jsonify({"error": "Amount must be at least 1"}), 400

    current = user.gold or 0
    if current < amount:
        return jsonify({"error": "Not enough gold"}), 400

    user.gold = current - amount
    try:
        db.session.commit()
        return jsonify({"gold": user.gold})
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to spend gold"}), 500


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

@api.route("/display-slots", methods=["GET"])
def get_display_slots():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    slots = DisplaySlot.query.filter_by(user_id=user.id).order_by(DisplaySlot.slot_index).all()

    # Return all 4 slots, empty ones included
    result = []
    slot_map = {s.slot_index: s for s in slots}
    for i in range(4):
        slot = slot_map.get(i)
        result.append({
            "slot_index": i,
            "skin": slot.skin.to_dict() if slot and slot.skin else None,
        })

    return jsonify(result)


@api.route("/display-slots/<int:slot_index>", methods=["PUT"])
def update_display_slot(slot_index):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    if slot_index < 0 or slot_index > 3:
        return jsonify({"error": "Invalid slot index (0-3 only)"}), 400

    data    = request.get_json()
    skin_id = data.get("skin_id")
    if not skin_id:
        return jsonify({"error": "skin_id is required"}), 400

    # Make sure user owns this skin
    owned = UserCollection.query.filter_by(user_id=user.id, skin_id=skin_id).first()
    if not owned:
        return jsonify({"error": "You don't own this skin"}), 403

    slot = DisplaySlot.query.filter_by(user_id=user.id, slot_index=slot_index).first()
    if slot:
        slot.skin_id = skin_id
    else:
        db.session.add(DisplaySlot(user_id=user.id, slot_index=slot_index, skin_id=skin_id))

    db.session.commit()
    return jsonify({"message": "Slot updated", "slot_index": slot_index, "skin_id": skin_id})


@api.route("/display-slots/<int:slot_index>", methods=["DELETE"])
def clear_display_slot(slot_index):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    slot = DisplaySlot.query.filter_by(user_id=user.id, slot_index=slot_index).first()
    if not slot:
        return jsonify({"error": "Slot is already empty"}), 404

    slot.skin_id = None
    db.session.commit()
    return jsonify({"message": "Slot cleared", "slot_index": slot_index})

@api.route("/collection/unlock/<int:collection_id>", methods=["POST"])
def unlock_skin(collection_id):
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    entry = UserCollection.query.filter_by(id=collection_id, user_id=user.id).first()
    if not entry:
        return jsonify({"error": "Skin not found in collection"}), 404

    if entry.is_owned:
        return jsonify({"error": "Skin is already unlocked"}), 400

    unlock_cost = entry.skin.rarity.item_cost
    if (user.essence or 0) < unlock_cost:
        return jsonify({"error": "Not enough essence"}), 400

    user.essence -= unlock_cost
    entry.is_owned = True

    try:
        db.session.commit()
        return jsonify({
            "message":     "Skin unlocked",
            "essence":     user.essence,
            "is_owned":    True,
        })
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Failed to unlock skin"}), 500