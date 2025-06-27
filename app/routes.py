from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.services import create_user, update_user, delete_user, get_user_by_id, get_all_users, \
    get_all_users_with_full_address, create_product, update_product, delete_product, get_product_by_id, \
    get_all_products, get_all_categories, get_category_by_id, create_category, update_category, delete_category, \
    delete_question, update_question, create_question, get_all_questions, get_question_by_id, get_questions_by_category, \
    get_all_question_categories, get_question_category_by_id, create_question_category, update_question_category, \
    delete_question_category

api_blueprint = Blueprint("api", __name__, url_prefix="/api")


@api_blueprint.route("/question-categories", methods=["GET"])
def get_question_categories_route():
    try:
        question_categories = get_all_question_categories()
        return jsonify(question_categories), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/question-categories/<int:question_category_id>", methods=["GET"])
def get_question_category_route(question_category_id):
    try:
        question_category = get_question_category_by_id(question_category_id)
        if question_category is None:
            return jsonify({"error": "Question category not found"}), 404
        return jsonify(question_category), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/question-categories", methods=["POST"])
def create_question_category_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        question_category = create_question_category(data)
        return jsonify(question_category), 201
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/question-categories/<int:question_category_id>", methods=["PUT"])
def update_question_category_route(question_category_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        question_category = update_question_category(question_category_id, data)
        return jsonify(question_category), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/question-categories/<int:question_category_id>", methods=["DELETE"])
def delete_question_category_route(question_category_id):
    try:
        delete_question_category(question_category_id)
        return jsonify({"message": "Question category deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# Маршруты для вопросов
@api_blueprint.route("/questions", methods=["GET"])
def get_questions_route():
    try:
        category_id = request.args.get('category_id', type=int)
        if category_id:
            questions = get_questions_by_category(category_id)
        else:
            questions = get_all_questions()
        return jsonify(questions), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/questions/<int:question_id>", methods=["GET"])
def get_question_route(question_id):
    try:
        question = get_question_by_id(question_id)
        if question is None:
            return jsonify({"error": "Question not found"}), 404
        return jsonify(question), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/questions", methods=["POST"])
def create_question_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        question = create_question(data)
        return jsonify(question), 201
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/questions/<int:question_id>", methods=["PUT"])
def update_question_route(question_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        question = update_question(question_id, data)
        return jsonify(question), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/questions/<int:question_id>", methods=["DELETE"])
def delete_question_route(question_id):
    try:
        delete_question(question_id)
        return jsonify({"message": "Question deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/products", methods=["GET"])
def get_products_route():
    try:
        products = get_all_products()
        return jsonify(products), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/products/<int:product_id>", methods=["GET"])
def get_product_route(product_id):
    try:
        product = get_product_by_id(product_id)
        if product is None:
            return jsonify({"error": "Product not found"}), 404
        return jsonify(product), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/products", methods=["POST"])
def create_product_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        product = create_product(data)
        return jsonify(product), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/products/<int:product_id>", methods=["PUT"])
def update_product_route(product_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        product = update_product(product_id, data)
        return jsonify(product), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product_route(product_id):
    try:
        delete_product(product_id)
        return jsonify({"message": "Product deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/categories", methods=["GET"])
def get_categories_route():
    try:
        categories = get_all_categories()
        return jsonify(categories), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/categories/<int:category_id>", methods=["GET"])
def get_category_route(category_id):
    try:
        category = get_category_by_id(category_id)
        if category is None:
            return jsonify({"error": "Category not found"}), 404
        return jsonify(category), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/categories", methods=["POST"])
def create_category_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        category = create_category(data)
        return jsonify(category), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/categories/<int:category_id>", methods=["PUT"])
def update_category_route(category_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        category = update_category(category_id, data)
        return jsonify(category), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/categories/<int:category_id>", methods=["DELETE"])
def delete_category_route(category_id):
    try:
        delete_category(category_id)
        return jsonify({"message": "Category deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/users", methods=["POST"])
def create_user_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user = create_user(data)
        return jsonify(user), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/users/<string:user_uuid>", methods=["GET"])
def get_user_route(user_uuid):
    try:
        user = get_user_by_id(user_uuid)
        if user is None:
            return jsonify({"error": "User not found"}), 404
        return jsonify(user), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/users", methods=["GET"])
def get_all_users_route():
    try:
        users = get_all_users()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/users_wa", methods=["GET"])
def get_all_users_with_full_address_route():
    try:
        users = get_all_users_with_full_address()
        return jsonify(users), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/users/<string:user_uuid>", methods=["PUT"])
def update_user_route(user_uuid):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        user = update_user(user_uuid, data)
        return jsonify(user), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/users/<string:user_uuid>", methods=["DELETE"])
def delete_user_route(user_uuid):
    try:
        delete_user(user_uuid)
        return jsonify({"message": "User deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400
