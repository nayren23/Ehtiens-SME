from flask import Blueprint, request, jsonify
from ethiens_sme.utils.role_user import RoleUser, role_required
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.service import seance_service

seance = Blueprint("seance", __name__, url_prefix="/seance")


@seance.route("/test", methods=["GET"])
def test():
    """Get information about the seance's car endpoint"""
    return jsonify("message")


@seance.route("/<ville_name>", methods=["GET"])
def get_seances_by_city(ville_name):
    """Get information about the seance's car endpoint"""
    try:
        available_seance = seance_service.get_seance_info_by_city_name(ville_name)
        response = jsonify(available_seance), 200
    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code
    return response


@seance.route("/", methods=["POST"])
def add_seance():
    """
    Add a new seance to a cinema schedule.
    Expected JSON:
    {
        "date_time": "2025-12-25 20:00:00",
        "room": "Salle 1",
        "language": "VOSTFR",
        "movie_id": 12,
        "cinema_id": 3
    }
    """
    try:
        data = request.get_json()

        # Validation des champs obligatoires
        required_fields = ["date_time", "movie_id", "cinema_id"]
        if not all(field in data for field in required_fields):
            return jsonify({"message": "Missing required fields"}), 400

        new_id = seance_service.create_seance(data)

        return jsonify({"message": "Seance added successfully", "id": new_id}), 201

    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code
    except Exception as e:
        return jsonify({"message": str(e)}), 500
