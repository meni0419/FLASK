import uuid
from datetime import datetime
from app import db

class Address(db.Model):
    __tablename__ = 'addresses'

    address_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    city = db.Column(db.String(255), nullable=True)
    street = db.Column(db.String(255), nullable=True)
    house_number = db.Column(db.Integer, nullable=True)

    # Relationship with User
    users = db.relationship('User', back_populates='address')

    def __repr__(self):
        return f"<Address {self.city}, {self.street} {self.house_number}>"

class User(db.Model):
    __tablename__ = 'users'

    user_uuid = db.Column(
        db.String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=True)
    password_hash = db.Column(db.String(255), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.utcnow)
    status = db.Column(db.Integer, default=1)
    is_admin = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer, nullable=True)
    is_employed = db.Column(db.Boolean, default=False)

    # Foreign Key and Relationship with Address
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=True)
    address = db.relationship('Address', back_populates='users')

    def __repr__(self):
        return f"<User {self.username}>"