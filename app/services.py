import uuid
from itertools import product

from passlib.context import CryptContext
from datetime import datetime
from app import db
from app.models import User, Address, Product, Category
from app.schemas import UserCreate, UserUpdate, ProductCreate, ProductUpdate, CategoryCreate, CategoryUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def product_to_dict(product):
    return {
        "product_id": product.product_id,
        "name": product.name,
        "price": product.price,
        "description": product.description,
        "in_stock": product.in_stock,
        "category_id": product.category_id,
        "created_at": product.created_at.isoformat() if product.created_at else None,
        "updated_at": product.updated_at.isoformat() if product.updated_at else None
    }


def category_to_dict(category):
    return {
        "category_id": category.category_id,
        "name": category.name,
        "description": category.description,
        "created_at": category.created_at.isoformat() if category.created_at else None,
        "updated_at": category.updated_at.isoformat() if category.updated_at else None
    }


def get_all_products():
    products = Product.query.all()
    return [product_to_dict(product) for product in products]


def get_all_categories():
    categories = Category.query.all()
    return [category_to_dict(category) for category in categories]


def get_product_by_id(product_id):
    product = Product.query.filter_by(product_id=product_id).first()
    if product:
        return product_to_dict(product)
    return None


def get_category_by_id(category_id):
    category = Category.query.filter_by(category_id=category_id).first()
    if category:
        return category_to_dict(category)
    return None


def create_product(product_data: dict):
    try:
        parsed_data = ProductCreate(**product_data)
        product = Product(
            name=parsed_data.name,
            price=parsed_data.price,
            description=parsed_data.description,
            in_stock=parsed_data.in_stock,
            category_id=parsed_data.category_id
        )

        db.session.add(product)
        db.session.commit()

        return product_to_dict(product)

    except Exception as e:
        raise e


def update_product(product_id: int, product_data: dict):
    try:
        product = Product.query.filter_by(product_id=product_id).first()
        if not product:
            raise ValueError("Product not found")
        parsed_data = ProductUpdate(**product_data)
        product.name = parsed_data.name
        product.price = parsed_data.price
        product.description = parsed_data.description
        product.in_stock = parsed_data.in_stock
        product.category_id = parsed_data.category_id
        product.updated_at = datetime.now()
        db.session.commit()
        return product_to_dict(product)
    except Exception as e:
        db.session.rollback()
        raise e


def delete_product(product_id: int):
    try:
        product = Product.query.filter_by(product_id=product_id).first()
        if not product:
            raise ValueError("Product not found")
        db.session.delete(product)
        db.session.commit()
        return product_to_dict(product)
    except Exception as e:
        db.session.rollback()
        raise e


def create_category(category_data: dict):
    try:
        parsed_data = CategoryCreate(**category_data)
        category = Category(
            name=parsed_data.name,
            description=parsed_data.description
        )
        db.session.add(category)
        db.session.commit()
        return category_to_dict(category)
    except Exception as e:
        db.session.rollback()
        raise e


def update_category(category_id: int, category_data: dict):
    try:
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            raise ValueError("Category not found")
        parsed_data = CategoryUpdate(**category_data)
        category.name = parsed_data.name
        category.description = parsed_data.description
        category.updated_at = datetime.now()
        db.session.commit()
        return category_to_dict(category)
    except Exception as e:
        db.session.rollback()
        raise e


def delete_category(category_id: int):
    try:
        category = Category.query.filter_by(category_id=category_id).first()
        if not category:
            raise ValueError("Category not found")
        db.session.delete(category)
        db.session.commit()
        return category_to_dict(category)
    except Exception as e:
        db.session.rollback()
        raise e


def user_to_dict(user):
    """Преобразование объекта User в словарь для JSON ответа"""
    user_dict = {
        "user_uuid": user.user_uuid,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "created_at": user.created_at.isoformat() if user.created_at else None,
        "updated_at": user.updated_at.isoformat() if user.updated_at else None,
        "status": user.status,
        "is_admin": user.is_admin,
        "age": user.age,
        "is_employed": user.is_employed,
        "address": None
    }

    if user.address:
        user_dict["address"] = {
            "address_id": user.address.address_id,
            "city": user.address.city,
            "street": user.address.street,
            "house_number": user.address.house_number
        }

    return user_dict


def create_user(user_data: dict):
    try:
        parsed_data = UserCreate(**user_data)

        # Проверка возраста для трудоустроенных пользователей
        if parsed_data.is_employed and parsed_data.age is not None:
            if parsed_data.age < 18 or parsed_data.age > 65:
                raise ValueError('Employed users must be between 18 and 65 years old')

        user_uuid = str(uuid.uuid4())
        hashed_password = pwd_context.hash(parsed_data.password)

        # Обработка адреса
        address = None
        if parsed_data.address:
            address = Address(
                city=parsed_data.address.city,
                street=parsed_data.address.street,
                house_number=parsed_data.address.house_number
            )
            db.session.add(address)
            db.session.flush()

        # Создание пользователя
        user = User(
            user_uuid=user_uuid,
            username=parsed_data.username,
            email=parsed_data.email,
            password_hash=hashed_password,
            full_name=parsed_data.full_name,
            age=parsed_data.age,
            is_employed=parsed_data.is_employed if parsed_data.is_employed is not None else False,
            address_id=address.address_id if address else None
        )

        db.session.add(user)
        db.session.commit()

        return user_to_dict(user)

    except Exception as e:
        db.session.rollback()
        raise e


def get_user_by_id(user_uuid: str):
    user = User.query.filter_by(user_uuid=user_uuid).first()
    if user:
        return user_to_dict(user)
    return None


def get_all_users():
    users = User.query.all()
    return [user_to_dict(user) for user in users]


def get_all_users_with_full_address():
    users = User.query.join(Address, User.address_id == Address.address_id, isouter=True).all()
    return [user_to_dict(user) for user in users]


def update_user(user_uuid: str, user_data: dict):
    try:
        user = User.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            raise ValueError("User not found")

        parsed_data = UserUpdate(**user_data)

        # Получаем текущие значения для валидации
        current_age = user.age if parsed_data.age is None else parsed_data.age
        current_is_employed = user.is_employed if parsed_data.is_employed is None else parsed_data.is_employed

        # Дополнительная проверка для обновления
        if current_is_employed and current_age is not None:
            if current_age < 18 or current_age > 65:
                raise ValueError('Employed users must be between 18 and 65 years old')

        # Обновляем поля пользователя
        if parsed_data.username is not None:
            user.username = parsed_data.username
        if parsed_data.email is not None:
            user.email = parsed_data.email
        if parsed_data.full_name is not None:
            user.full_name = parsed_data.full_name
        if parsed_data.age is not None:
            user.age = parsed_data.age
        if parsed_data.is_employed is not None:
            user.is_employed = parsed_data.is_employed

        user.updated_at = datetime.now()

        # Обработка адреса
        if parsed_data.address:
            if user.address:
                # Обновляем существующий адрес
                user.address.city = parsed_data.address.city
                user.address.street = parsed_data.address.street
                user.address.house_number = parsed_data.address.house_number
            else:
                # Создаем новый адрес
                address = Address(
                    city=parsed_data.address.city,
                    street=parsed_data.address.street,
                    house_number=parsed_data.address.house_number
                )
                db.session.add(address)
                db.session.flush()
                user.address_id = address.address_id

        db.session.commit()
        return user_to_dict(user)

    except Exception as e:
        db.session.rollback()
        raise e


def delete_user(user_uuid: str):
    try:
        user = User.query.filter_by(user_uuid=user_uuid).first()
        if not user:
            raise ValueError("User not found")

        # Удаляем связанный адрес, если он есть
        if user.address:
            db.session.delete(user.address)

        db.session.delete(user)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
