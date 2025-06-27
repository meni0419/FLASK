import uuid
from datetime import datetime
from app import db


class QuestionCategory(db.Model):
    __tablename__ = 'question_categories'

    question_category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
    questions = db.relationship('Question', backref='category', lazy=True)

    def __repr__(self):
        return f"<QuestionCategory {self.question_category_id}, {self.name}, {self.description}>"


class Question(db.Model):
    __tablename__ = 'questions'
    question_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_category_id = db.Column(db.Integer, db.ForeignKey('question_categories.question_category_id'),
                                     nullable=False)
    question = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

    def __repr__(self):
        return f"<Question {self.question_id}, {self.question}>"


class Product(db.Model):
    __tablename__ = 'products'

    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=True)
    in_stock = db.Column(db.Boolean, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)

    def __repr__(self):
        return f"<Product {self.product_id}, {self.name}, {self.price}, {self.in_stock}, {self.description}>"

class Category(db.Model):
    __tablename__ = 'categories'

    category_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
    products = db.relationship('Product', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.category_id}, {self.name}, {self.description}>"

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
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=True, onupdate=datetime.now)
    status = db.Column(db.Integer, default=1)
    is_admin = db.Column(db.Boolean, default=False)
    age = db.Column(db.Integer, nullable=True)
    is_employed = db.Column(db.Boolean, default=False)

    # Foreign Key and Relationship with Address
    address_id = db.Column(db.Integer, db.ForeignKey('addresses.address_id'), nullable=True)
    address = db.relationship('Address', back_populates='users')

    def __repr__(self):
        return f"<User {self.username}>"