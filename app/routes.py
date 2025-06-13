from flask import Blueprint, request, jsonify
from pydantic import ValidationError
from app.services import create_user, update_user, delete_user, get_user_by_id, get_all_users, \
    get_all_users_with_full_address, create_address, update_address, delete_address, get_address_by_id, \
    get_all_addresses

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


# Address routes
@api_blueprint.route("/addresses", methods=["POST"])
def create_address_route():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        address = create_address(data)
        return jsonify(address), 201
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/addresses/<int:address_id>", methods=["GET"])
def get_address_route(address_id):
    try:
        address = get_address_by_id(address_id)
        if address is None:
            return jsonify({"error": "Address not found"}), 404
        return jsonify(address), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/addresses", methods=["GET"])
def get_all_addresses_route():
    try:
        addresses = get_all_addresses()
        return jsonify(addresses), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@api_blueprint.route("/addresses/<int:address_id>", methods=["PUT"])
def update_address_route(address_id):
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        address = update_address(address_id, data)
        return jsonify(address), 200
    except ValidationError as ve:
        return jsonify({"error": "Validation error", "details": ve.errors()}), 400
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@api_blueprint.route("/addresses/<int:address_id>", methods=["DELETE"])
def delete_address_route(address_id):
    try:
        delete_address(address_id)
        return jsonify({"message": "Address deleted successfully"}), 200
    except ValueError as ve:
        return jsonify({"error": str(ve)}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 400