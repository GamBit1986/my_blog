from .extension import db
from flask_login.mixins import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))

    def __repr__(self):
        return f"<User #{self.id} {self.username!r}>"
