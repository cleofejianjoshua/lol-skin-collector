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


def get_champions(version):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion.json"
    return requests.get(url).json()["data"]


def get_champion_data(version, champ_key):
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/champion/{champ_key}.json"
    return requests.get(url).json()["data"][champ_key]


def build_image_url(champion, skin_name):
    clean_champ = champion.replace(" ", "")
    clean_skin = skin_name.replace(" ", "_").replace("'", "").replace(":", "")

    return f"https://ddragon.leagueoflegends.com/cdn/img/champion/loading/{clean_champ}_{clean_skin}.jpg"


def assign_rarity(skin_name):
    name = skin_name.lower()

    if "prestige" in name or "ultimate" in name:
        return "legendary"
    elif "project" in name or "k/da" in name:
        return "epic"
    elif name == "classic":
        return "common"
    else:
        return "rare"


# ----------------------------
# SEED LOGIC
# ----------------------------

def seed_skins():
    version = get_latest_version()
    champions = get_champions(version)

    print(f"Using version: {version}")

    for champ_key, champ_data in champions.items():

        full_data = get_champion_data(version, champ_key)
        skins = full_data["skins"]

        for skin in skins:
            name = skin["name"]

            image_url = build_image_url(full_data["name"], name)
            rarity_name = assign_rarity(name)

            rarity = Rarity.query.filter_by(rarity_name=rarity_name).first()

            if not rarity:
                print(f"Skipping missing rarity: {rarity_name}")
                continue

            exists = Skin.query.filter_by(
                name=name,
                champion=full_data["name"]
            ).first()

            if exists:
                continue

            new_skin = Skin(
                name=name,
                champion=full_data["name"],
                rarity_id=rarity.id,
                image_path=image_url
            )

            db.session.add(new_skin)

        db.session.commit()
        print(f"Seeded {champ_key}")


if __name__ == "__main__":
    seed_skins()