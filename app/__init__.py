from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

load_dotenv()

# Создаем экземпляр БД
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Конфигурация
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{os.getenv('DATABASE_USER')}:{os.getenv('DATABASE_PASSWORD')}@{os.getenv('DATABASE_HOST')}:{os.getenv('DATABASE_PORT')}/{os.getenv('DATABASE_NAME')}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
        'pool_pre_ping': True,
        'pool_recycle': 300,
    }

    # Инициализация БД с приложением
    db.init_app(app)

    # Импорт моделей после инициализации db
    from app.models import User, Address

    # Импорт и регистрация blueprint
    from app.routes import api_blueprint
    app.register_blueprint(api_blueprint)

    # Создание таблиц
    with app.app_context():
        db.create_all()

    return app