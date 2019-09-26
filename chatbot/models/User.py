from datetime import datetime
from chatbot.database import db


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(
        db.String(255),
        index=True,
        unique=True,
        nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.now,
        onupdate=datetime.now)

    def __init__(self, username, password, create_at, update_at):
        self.username = username
        self.password = password
        self.created_at = create_at
        self.updated_at = update_at
