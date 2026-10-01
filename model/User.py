from datetime import datetime
from extensions import db


class User(db.Model):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.Text, nullable=True)
    fullname = db.Column(db.String(128))
    email = db.Column(db.String(128), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(30), nullable=False, default="Customer")
    status = db.Column(db.String(30), nullable=False, default="Active")
    create_at = db.Column(db.DateTime, default=datetime.utcnow)
    update_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.email}>"
