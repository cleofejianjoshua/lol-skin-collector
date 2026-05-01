from app import db

class User(db.Model):
    __tablename__="users"# explicit table name is a good habit for Oracle
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(80),unique=True,nullable=False)
    password=db.Column(db.String(255),nullable=False)
    nickname=db.Column(db.String(20))
    email=db.Column(db.String(255))

    def __repr__(self):
        return f"<User{self.username}>"