from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect
import os
from dotenv import load_dotenv

load_dotenv()

# Создаем экземпляр БД
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Инициализация БД с приложением
    db.init_app(app)
    migrate.init_app(app, db)  # Инициализируем миграции

    # Импорт моделей после инициализации db
    from app.models import (
        User, Address,
        Product, Category,
        QuestionCategory, Question)

    # Импорт и регистрация blueprint
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    return app
