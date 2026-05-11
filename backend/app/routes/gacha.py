from flask import Blueprint, jsonify
from app import db
from app.models import Skin, UserCollection
from .api import get_current_user
import random

gacha = Blueprint("gacha", __name__, url_prefix="/api/gacha")

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


PULL_COST = 25

@gacha.route("/pull", methods=["POST"])
def gacha_pull():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    if (user.gold or 0) < PULL_COST:
        return jsonify({"error": "Not enough gold"}), 400

    all_skins = Skin.query.all()
    if not all_skins:
        return jsonify({"error": "No skins available in the pool yet."}), 404

    rarity = pick_rarity()
    pool   = [s for s in all_skins if s.rarity.rarity_name == rarity]
    if not pool:
        pool = all_skins

    skin = random.choice(pool)

    existing = UserCollection.query.filter_by(user_id=user.id, skin_id=skin.id).first()

    if existing:
        existing.duplicate_count += 1
        is_duplicate = True
    else:
        db.session.add(UserCollection(user_id=user.id, skin_id=skin.id))
        is_duplicate = False

    user.gold -= PULL_COST

    try:
        db.session.commit()
        return jsonify({
            "skin":         skin.to_dict(),
            "is_duplicate": is_duplicate,
            "gold":         user.gold,
        })
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Pull failed"}), 500