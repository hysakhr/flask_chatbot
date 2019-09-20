from datetime import datetime
from chatbot.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), index=True, unique=True)
    password = db.Column(db.String(255), nullable=False)
    create_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    update_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self, username, password, create_at, update_at):
        self.username = username
        self.password = password
        self.create_at = create_at
        self.update_at = update_at
