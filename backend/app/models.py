from app import db
from datetime import datetime, timezone


class User(db.Model):
    __tablename__ = "users"
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(20))
    email    = db.Column(db.String(255))
    essence = db.Column(db.Integer,default=0)
    gold     = db.Column(db.Integer,default=0)

    # Relationship to skin collection
    collection = db.relationship(
        "UserCollection",
        back_populates="user",
        lazy=True,
        cascade="all, delete-orphan"
    )

    display_slots = db.relationship(
        "DisplaySlot", 
        back_populates="user", 
        lazy=True, 
        cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.username}>"


class Skin(db.Model):
    __tablename__ = "skins"
    id    = db.Column(db.Integer, primary_key=True)
    skin_name  = db.Column(db.String(120), nullable=False)
    champion   = db.Column(db.String(80), nullable=False)
    # Rarity: common | rare | epic | legendary
    rarity_id  = db.Column(db.Integer, db.ForeignKey("rarities.id"),nullable=False)
    # Path relative to /public, e.g. /images/skins/champions/ahri/spirit_blossom.jpg
    image_path = db.Column(db.String(255), nullable=False, default="")
    

    rarity = db.relationship("Rarity", lazy="joined", back_populates="skins")

    collection = db.relationship(
        "UserCollection",
        back_populates="skin",
        lazy=True,
        cascade="all, delete-orphan"
    )

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.skin_name,
            "champion":   self.champion,
            "rarity":     self.rarity.rarity_name,
            "image_path": self.image_path,
        }

    def __repr__(self):
        return f"<Skin {self.skin_name} ({self.champion})>"
    

class Rarity(db.Model):
    __tablename__ = "rarities"
    id = db.Column(db.Integer, primary_key=True)
    rarity_name = db.Column(db.String(50), unique=True, nullable=False)
    item_cost = db.Column(db.Integer, nullable=False)
    disenchant_value = db.Column(db.Integer, nullable=False)

    skins = db.relationship("Skin", back_populates="rarity", lazy=True)

    def __repr__(self):
        return f"<Rarity {self.rarity_name}>"


class UserCollection(db.Model):
    __tablename__ = "user_collection"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skin_id     = db.Column(db.Integer, db.ForeignKey("skins.id"), nullable=False)
    obtained_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    duplicate_count = db.Column(db.Integer, nullable=False, default=0)
    is_owned    = db.Column(db.Boolean, nullable=False, default=False)
    __table_args__ = (
        db.UniqueConstraint ("user_id", "skin_id", name="uq_user_skin"),
    )

    user = db.relationship("User", back_populates="collection")
    skin = db.relationship("Skin", back_populates="collection")

    def to_dict(self):
        return {
            "id":          self.id,
            "skin":        self.skin.to_dict(),
            "obtained_at": self.obtained_at.isoformat(),
            "duplicate_count": self.duplicate_count,
            "is_owned" :   self.is_owned,
        }

    def __repr__(self):
        return f"<UserCollection user={self.user_id} skin={self.skin_id}>"
    
class DisplaySlot(db.Model):
    __tablename__ = "display_slot"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    slot_index  = db.Column(db.Integer, nullable=False)
    skin_id     = db.Column(db.Integer, db.ForeignKey("skins.id"))

    __table_args__ = (
        db.UniqueConstraint("user_id", "slot_index", name="uq_user_slot"),
        db.CheckConstraint("slot_index BETWEEN 0 AND 3", name="ck_slot_index_range"),
    )

    user = db.relationship("User", back_populates="display_slots")
    skin = db.relationship("Skin", lazy="joined")
    