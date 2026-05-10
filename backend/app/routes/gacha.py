import random
from flask import Blueprint, jsonify, session
from app import db
from app.models import User, Skin, Rarity, UserCollection

gacha = Blueprint("gacha", __name__)

WEIGHTS = {
    "ultimate":  1,
    "legendary": 9,
    "epic":      18,
    "rare":      32,
    "common":    40,
}

def weighted_rarity_roll():
    pool = list(WEIGHTS.keys())
    weights = list(WEIGHTS.values())
    return random.choices(pool, weights=weights, k=1)[0]

@gacha.route("/api/gacha/pull", methods=["POST"])
def gacha_pull():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    # Roll a rarity
    rarity_name = weighted_rarity_roll()

    # Get rarity from DB
    rarity = Rarity.query.filter_by(rarity_name=rarity_name).first()
    if not rarity:
        return jsonify({"error": f"Rarity '{rarity_name}' not found"}), 500

    # Pick a random skin of that rarity
    skins = Skin.query.filter_by(rarity_id=rarity.id).all()
    if not skins:
        return jsonify({"error": f"No skins found for rarity '{rarity_name}'"}), 500

    skin = random.choice(skins)

    # Check if user already owns this skin
    existing = UserCollection.query.filter_by(user_id=user_id, skin_id=skin.id).first()

    if existing:
        existing.duplicate_count += 1
        is_duplicate = True
    else:
        db.session.add(UserCollection(
            user_id=user_id,
            skin_id=skin.id,
            duplicate_count=0,
        ))
        is_duplicate = False

    db.session.commit()

    return jsonify({
        "skin": {
            "id":           skin.id,
            "name":         skin.skin_name,
            "champion":     skin.champion,
            "rarity":       rarity_name,
            "image_path":   skin.image_path,
        },
        "is_duplicate": is_duplicate,
    })