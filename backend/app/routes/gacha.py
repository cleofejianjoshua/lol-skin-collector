from flask import Blueprint, jsonify, request
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


@gacha.route("/history", methods=["GET"])
def gacha_history():
    """Return paginated pull history for the current user.

    Uses UserCollection.obtained_at for ordering (oldest = pull #1).
    Pull numbers are computed as a global rank across all the user's pulls.
    """
    user = get_current_user()
    if not user:
        return jsonify({"error": "Not logged in"}), 401

    try:
        page      = int(request.args.get("page", 1))
        page_size = int(request.args.get("page_size", 5))
    except ValueError:
        return jsonify({"error": "Invalid pagination params"}), 400

    if page < 1:
        page = 1
    if page_size < 1 or page_size > 50:
        page_size = 5

    # Total number of pulls (one row per skin, duplicates have duplicate_count > 0
    # but each row was obtained once — we treat each UserCollection entry as 1 pull).
    total = UserCollection.query.filter_by(user_id=user.id).count()
    total_pages = max(1, -(-total // page_size))  # ceiling division

    # Fetch the page ordered by oldest first so pull #1 = first skin obtained
    offset = (page - 1) * page_size
    rows = (
        UserCollection.query
        .filter_by(user_id=user.id)
        .order_by(UserCollection.obtained_at.asc())
        .offset(offset)
        .limit(page_size)
        .all()
    )

    pulls = []
    for idx, row in enumerate(rows):
        pull_number = offset + idx + 1  # 1-based global pull number
        pulls.append({
            "pull_number": pull_number,
            "skin_name":   row.skin.skin_name,
            "champion":    row.skin.champion,
            "rarity":      row.skin.rarity.rarity_name,
            "image_path":  row.skin.image_path,
            "obtained_at": row.obtained_at.strftime("%Y-%m-%d"),
            "is_duplicate": row.duplicate_count > 0,
        })

    return jsonify({
        "pulls":       pulls,
        "total":       total,
        "page":        page,
        "page_size":   page_size,
        "total_pages": total_pages,
    })