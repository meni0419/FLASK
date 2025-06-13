import uuid
from passlib.context import CryptContext
from datetime import datetime
from app import db
from app.models import User, Address
from app.schemas import UserCreate, UserUpdate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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

        user.updated_at = datetime.utcnow()

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


def address_to_dict(address):
    """Преобразование объекта Address в словарь для JSON ответа"""
    return {
        "address_id": address.address_id,
        "city": address.city,
        "street": address.street,
        "house_number": address.house_number
    }


def create_address(address_data: dict):
    try:
        from app.schemas import AddressCreate
        parsed_data = AddressCreate(**address_data)

        address = Address(
            city=parsed_data.city,
            street=parsed_data.street,
            house_number=parsed_data.house_number
        )

        db.session.add(address)
        db.session.commit()

        return address_to_dict(address)

    except Exception as e:
        db.session.rollback()
        raise e


def get_address_by_id(address_id: int):
    address = Address.query.filter_by(address_id=address_id).first()
    if address:
        return address_to_dict(address)
    return None


def get_all_addresses():
    addresses = Address.query.all()
    return [address_to_dict(address) for address in addresses]


def update_address(address_id: int, address_data: dict):
    try:
        from app.schemas import AddressCreate
        address = Address.query.filter_by(address_id=address_id).first()
        if not address:
            raise ValueError("Address not found")

        parsed_data = AddressCreate(**address_data)

        address.city = parsed_data.city
        address.street = parsed_data.street
        address.house_number = parsed_data.house_number

        db.session.commit()
        return address_to_dict(address)

    except Exception as e:
        db.session.rollback()
        raise e


def delete_address(address_id: int):
    try:
        address = Address.query.filter_by(address_id=address_id).first()
        if not address:
            raise ValueError("Address not found")

        # Check if address is being used by any user
        if address.users:
            raise ValueError("Cannot delete address that is assigned to users")

        db.session.delete(address)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        raise e
