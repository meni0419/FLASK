from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.services import create_user, update_user, delete_user, get_user_by_id, get_all_users, \
    get_all_users_with_full_address

api_blueprint = Blueprint("api", __name__, url_prefix="/api")

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