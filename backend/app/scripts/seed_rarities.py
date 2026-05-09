from app import app, db
from app.models import Rarity

RARITIES = [
    {
        "rarity_name": "common",
        "item_cost": 520,
        "disenchant_value": 90
    },
    {
        "rarity_name": "rare",
        "item_cost": 750,
        "disenchant_value": 150
    },
    {
        "rarity_name": "epic",
        "item_cost": 1350,
        "disenchant_value": 350
    },
    {
        "rarity_name": "legendary",
        "item_cost": 1820,
        "disenchant_value": 600
    },
    {
        "rarity_name": "ultimate",
        "item_cost": 3250,
        "disenchant_value": 1200
    }
]

with app.app_context():

    for rarity_data in RARITIES:

        existing = Rarity.query.filter_by(
            rarity_name=rarity_data["rarity_name"]
        ).first()

        if existing:
            print(f"{rarity_data['rarity_name']} already exists")
            continue

        rarity = Rarity(
            rarity_name=rarity_data["rarity_name"],
            item_cost=rarity_data["item_cost"],
            disenchant_value=rarity_data["disenchant_value"]
        )

        db.session.add(rarity)

    db.session.commit()

    print("Rarities seeded successfully.")