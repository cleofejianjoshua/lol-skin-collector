from app import db
from datetime import datetime


class User(db.Model):
    __tablename__ = "users"
    id       = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(20))
    email    = db.Column(db.String(255))

    # Relationship to skin collection
    collection = db.relationship("UserCollection", back_populates="user", lazy=True)

    def __repr__(self):
        return f"<User {self.username}>"


class Skin(db.Model):
    __tablename__ = "skins"
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(120), nullable=False)
    champion   = db.Column(db.String(80), nullable=False)
    # Rarity: common | rare | epic | legendary
    rarity     = db.Column(db.String(20), nullable=False, default="common")
    # Path relative to /public, e.g. /images/skins/champions/ahri/spirit_blossom.jpg
    image_path = db.Column(db.String(255), nullable=False, default="")

    collection = db.relationship("UserCollection", back_populates="skin", lazy=True)

    def to_dict(self):
        return {
            "id":         self.id,
            "name":       self.name,
            "champion":   self.champion,
            "rarity":     self.rarity,
            "image_path": self.image_path,
        }

    def __repr__(self):
        return f"<Skin {self.name} ({self.champion})>"


class UserCollection(db.Model):
    __tablename__ = "user_collection"
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    skin_id     = db.Column(db.Integer, db.ForeignKey("skins.id"), nullable=False)
    obtained_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship("User", back_populates="collection")
    skin = db.relationship("Skin", back_populates="collection")

    def to_dict(self):
        return {
            "id":          self.id,
            "skin":        self.skin.to_dict(),
            "obtained_at": self.obtained_at.isoformat(),
        }

    def __repr__(self):
        return f"<UserCollection user={self.user_id} skin={self.skin_id}>"