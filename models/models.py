# models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    profile_image = db.Column(db.String(100), nullable=True, default='default.jpg')  # Added profile_image attribute with default value 'default.jpg'
    role = db.Column(db.String(50), default='user')  # Added role attribute with default value 'user'
    status = db.Column(db.String(50), default='active')  # Added role attribute with default value 'user'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)  # Added created_at attribute with default timestamp

    def __init__(self, username, email, password, role='user', status='active', profile_image='default.jpg'):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.status = status
        self.profile_image = profile_image


class admins(db.Model):
    _id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

