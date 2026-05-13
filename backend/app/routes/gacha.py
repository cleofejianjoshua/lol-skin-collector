from flask import Blueprint, jsonify
from app import db
from app.models import Skin, UserCollection
from .api import get_current_user
import random

gacha = Blueprint("gacha", __name__, url_prefix="/api/gacha")

PULL_COST     = 25
PITY_INTERVAL = 10

NORMAL_WEIGHTS = { "common": 40, "rare": 32, "epic": 18, "legendary": 9, "ultimate": 1 }
PITY_WEIGHTS   = { "common": 0, "rare": 15, "epic": 45, "legendary": 36, "ultimate": 4 }

def pick_rarity(is_pity=False):
    weights = PITY_WEIGHTS if is_pity else NORMAL_WEIGHTS
    return random.choices(list(weights.keys()), weights=list(weights.values()), k=1)[0]

@gacha.route("/pull", methods=["POST"])
def gacha_pull():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    if (user.gold or 0) < PULL_COST:
        return jsonify({"error": "Not enough gold"}), 400

    all_skins = Skin.query.all()
    if not all_skins:
        return jsonify({"error": "No skins available"}), 404

    user.pull_count = (user.pull_count or 0) + 1
    is_pity = (user.pull_count % PITY_INTERVAL == 0)

    rarity = pick_rarity(is_pity)
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
        pulls_until_pity = PITY_INTERVAL - (user.pull_count % PITY_INTERVAL)
        return jsonify({
            "skin":             skin.to_dict(),
            "is_duplicate":     is_duplicate,
            "gold":             user.gold,
            "pulls_until_pity": pulls_until_pity,
        })
    except Exception:
        db.session.rollback()
        return jsonify({"error": "Pull failed"}), 500

@gacha.route("/status", methods=["GET"])
def gacha_status():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401
    pull_count      = user.pull_count or 0
    pulls_until_pity = PITY_INTERVAL - (pull_count % PITY_INTERVAL)
    return jsonify({
        "pull_count":       pull_count,
        "pulls_until_pity": pulls_until_pity,
    })

@gacha.route("/pull_total", methods=["GET"])
def pull_total():
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401
    return jsonify({
        "pull_count":       user.pull_count,
    })