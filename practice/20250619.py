from typing import List

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from pydantic import model_validator, ValidationError
from sqlalchemy import create_engine, Integer, String, ForeignKeyConstraint, Index, TIMESTAMP, text, Float
from sqlalchemy.dialects.mssql import TINYINT
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, relationship
from datetime import datetime
import os

app = Flask(__name__)

# Configure database
app.config[
    'SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://ich1:ich1_password_ilovedbs@ich-edit.edu.itcareerhub.de:3306/social_blogs"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Инициализация БД с приложением
db.init_app(app)

# Импорт моделей после инициализации db
from app.models import User, Address, Product, Category

# Импорт и регистрация blueprint
from app.routes import api_blueprint
app.register_blueprint(api_blueprint)

# Создание таблиц
with app.app_context():
    db.create_all()

return app

# Create database engine
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
Session = sessionmaker(bind=engine)

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'

    id = mapped_column(Integer, primary_key=True)
    name = mapped_column(String(20), nullable=False)

    users: Mapped[List['User']] = relationship('User', uselist=True, back_populates='role')


class User(Base):
    __tablename__ = 'user'
    __table_args__ = (
        ForeignKeyConstraint(['role_id'], ['role.id'], name='user_ibfk_1'),
        Index('email', 'email', unique=True),
        Index('role_id', 'role_id')
    )

    id = mapped_column(Integer, primary_key=True)
    first_name = mapped_column(String(25), nullable=False)
    last_name = mapped_column(String(30))
    email = mapped_column(String(255), nullable=False, unique=True)
    password = mapped_column(String(255), nullable=False)
    phone = mapped_column(String(45))
    role_id = mapped_column(Integer, nullable=False)
    created_at = mapped_column(TIMESTAMP, nullable=False, server_default=text('CURRENT_TIMESTAMP'))
    updated_at = mapped_column(TIMESTAMP)
    deleted_at = mapped_column(TIMESTAMP)
    deleted = mapped_column(TINYINT(1), server_default=text('0'))
    rating = mapped_column(Float, server_default=text('0'))

    role: Mapped['Role'] = relationship('Role', back_populates='users')


class UserCreateSchema:
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    role_id: int




class UserResponseSchema:
    id: int
    first_name: str
    last_name: str
    email: str
    password: str
    phone: str
    role_id: int
    created_at: datetime
    updated_at: datetime


@app.route('/api/users', methods=['POST'])
def create_user():
    try:
        data = request.get_json()

        validated_data = UserCreateSchema.model_validate(data)
        user = User(**validated_data.model_dump())

        db.session.add(user)
        db.session.commit()

        return jsonify(UserResponseSchema.model_validate(user).model_dump()), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
