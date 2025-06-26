from app import create_app, db
from app.models import Product, Category
from sqlalchemy import func


def init_app():
    """Инициализация приложения Flask для работы с базой данных"""
    app = create_app()
    return app


def count_products_by_category():
    """
    Задача 4: Агрегация и группировка
    Подсчитываем общее количество продуктов в каждой категории
    """
    print("=== Задача 4: Количество продуктов в каждой категории ===")

    # Выполняем запрос с группировкой и агрегацией
    results = db.session.query(
        Category.name.label('category_name'),
        func.count(Product.product_id).label('product_count')
    ).outerjoin(Product, Category.category_id == Product.category_id) \
        .group_by(Category.category_id, Category.name) \
        .all()

    # Выводим результаты
    for result in results:
        print(f"Категория: {result.category_name}, Количество продуктов: {result.product_count}")

    return results


def categories_with_multiple_products():
    """
    Задача 5: Группировка с фильтрацией
    Выводим только те категории, в которых более одного продукта
    """
    print("\n=== Задача 5: Категории с более чем одним продуктом ===")

    # Выполняем запрос с группировкой, агрегацией и фильтрацией
    results = db.session.query(
        Category.name.label('category_name'),
        func.count(Product.product_id).label('product_count')
    ).join(Product, Category.category_id == Product.category_id) \
        .group_by(Category.category_id, Category.name) \
        .having(func.count(Product.product_id) > 1) \
        .all()

    # Выводим результаты
    for result in results:
        print(f"Категория: {result.category_name}, Количество продуктов: {result.product_count}")

    return results


def main():
    """Главная функция для выполнения всех заданий"""
    app = init_app()

    with app.app_context():
        # Выполняем задачи
        count_products_by_category()
        categories_with_multiple_products()


if __name__ == "__main__":
    main()