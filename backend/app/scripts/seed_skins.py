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
    """Summary list — used only to get champion keys."""
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    return requests.get(url).json()["data"]


def get_champion_detail(session, version, champ_key):
    """Full champion data including skins list."""
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champ_key}.json"
    data = session.get(url).json()["data"]
    return data[list(data.keys())[0]]  # key name isn't always champ_key (e.g. Wukong = MonkeyKing)


def get_community_dragon_skins(session):
    url = "https://raw.communitydragon.org/latest/plugins/rcp-be-lol-game-data/global/default/v1/skins.json"
    print("Fetching Community Dragon skin data...")
    raw = {int(k): v for k, v in session.get(url).json().items()}

    # Build a set of all chroma IDs from the chromas arrays
    chroma_ids = set()
    for skin_data in raw.values():
        for chroma in skin_data.get("chromas", []):
            chroma_ids.add(chroma["id"])

    return raw, chroma_ids

def build_image_url(champ_key, skin_num):
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
    session.request = lambda method, url, **kwargs: requests.Session.request(session, method, url, timeout=10, **kwargs)

    print("Fetching champion list...")
    champions = get_champion_list(version)
    total_champs = len(champions)

    print("Fetching skin rarities...")
    cd_skins, chroma_ids = get_community_dragon_skins(session)

    rarity_cache = {r.rarity_name: r for r in Rarity.query.all()}

    total_added = 0

    for idx, champ_key in enumerate(champions, start=1):
        print(f"[{idx}/{total_champs}] Processing {champ_key}...")

        full_data = get_champion_detail(session, version, champ_key)
        champ_name = full_data["name"]
        champ_id = int(full_data["key"])

        for skin in full_data["skins"]:
            skin_num = skin["num"]
            skin_id = champ_id * 1000 + skin_num

            # Skip chromas using the definitive chroma ID set from Community Dragon
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

            exists = Skin.query.filter_by(
                skin_name=name,
                champion=champ_name
            ).first()

            if exists:
                continue

            db.session.add(Skin(
                skin_name=name,
                champion=champ_name,
                rarity_id=rarity.id,
                image_path=build_image_url(champ_key, skin_num),
            ))
            total_added += 1

        db.session.commit()

    print(f"Seeding complete. {total_added} skins added.")


if __name__ == "__main__":
    seed_skins()