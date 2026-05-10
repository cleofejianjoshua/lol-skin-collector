import requests
from app import db, app
from app.models import Skin, Rarity

app.app_context().push()


# ----------------------------
# API HELPERS
# ----------------------------

def get_latest_version():
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    return requests.get(url).json()[0]


def get_champion_list(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    return requests.get(url).json()["data"]


def get_champion_detail(session, version, champ_key):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champ_key}.json"
    data = session.get(url, timeout=10).json()["data"]
    return data[list(data.keys())[0]]


def get_community_dragon_skins(session):
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json"
    print("Fetching Community Dragon skin data...")
    raw = {int(k): v for k, v in session.get(url, timeout=30).json().items()}

    chroma_ids = set()
    for skin_data in raw.values():
        for chroma in skin_data.get("chromas", []):
            chroma_ids.add(chroma["id"])

    return raw, chroma_ids


def build_image_url(skin_id, cd_skins, champ_key, skin_num):
    cd_data = cd_skins.get(skin_id, {})
    path = cd_data.get("loadScreenPath", "")

    if path:
        clean = path.lower().replace("/lol-game-data/assets/", "")
        return f"https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/{clean}"

    # Fallback to DDragon if Community Dragon has no path
    return f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{champ_key}_{skin_num}.jpg"


def map_rarity(community_rarity: str, is_base: bool) -> str:
    if is_base:
        return "common"

    mapping = {
        "kNoRarity":  "rare",
        "kEpic":      "epic",
        "kLegendary": "legendary",
        "kMythic":    "legendary",
        "kUltimate":  "ultimate",
    }
    return mapping.get(community_rarity, "rare")


# ----------------------------
# SEED LOGIC
# ----------------------------

def seed_skins():
    version = get_latest_version()
    print(f"Using version: {version}")

    session = requests.Session()

    print("Fetching champion list...")
    champions = get_champion_list(version)
    total_champs = len(champions)

    print("Fetching skin rarities...")
    cd_skins, chroma_ids = get_community_dragon_skins(session)

    rarity_cache = {r.rarity_name: r for r in Rarity.query.all()}

    added = 0
    updated = 0

    for idx, champ_key in enumerate(champions, start=1):
        print(f"[{idx}/{total_champs}] Processing {champ_key}...")

        full_data = get_champion_detail(session, version, champ_key)
        champ_name = full_data["name"]
        champ_id = int(full_data["key"])

        for skin in full_data["skins"]:
            skin_num = skin["num"]
            skin_id = champ_id * 1000 + skin_num

            if skin_id in chroma_ids:
                continue

            is_base = skin_num == 0
            name = f"Original {champ_name}" if is_base else skin["name"]

            cd_rarity = cd_skins.get(skin_id, {}).get("rarity", "kNoRarity")
            rarity_name = map_rarity(cd_rarity, is_base)

            rarity = rarity_cache.get(rarity_name)
            if not rarity:
                print(f"  Skipping '{name}' — missing rarity in DB: {rarity_name}")
                continue

            image_url = build_image_url(skin_id, cd_skins, champ_key, skin_num)
            if not image_url:
                print(f"  No image found for '{name}', skipping.")
                continue

            existing = Skin.query.filter_by(
                skin_name=name,
                champion=champ_name
            ).first()

            if existing:
                # Update only if something changed
                changed = False
                if existing.rarity_id != rarity.id:
                    existing.rarity_id = rarity.id
                    changed = True
                if existing.image_path != image_url:
                    existing.image_path = image_url
                    changed = True
                if changed:
                    updated += 1
            else:
                db.session.add(Skin(
                    skin_name=name,
                    champion=champ_name,
                    rarity_id=rarity.id,
                    image_path=image_url,
                ))
                added += 1

        db.session.commit()

    print(f"Seeding complete. {added} skins added, {updated} skins updated.")


if __name__ == "__main__":
    seed_skins()