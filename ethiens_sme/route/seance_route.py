"""Seance related endpoints"""

from flask import Blueprint, request, jsonify
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.service import seance_service
from flask_jwt_extended import jwt_required, get_jwt

seance = Blueprint("seance", __name__, url_prefix="/seance")


@seance.route("/cinemas", methods=["GET"])
def get_cinemas():
    """Get list of all cinemas"""
    try:
        cinemas = seance_service.get_all_cinemas()
        return jsonify(cinemas), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@seance.route("/stats", methods=["GET"])
def get_stats():
    """Get dashboard stats"""
    try:
        stats = seance_service.get_dashboard_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@seance.route("/cinema/<int:cinema_id>/rooms", methods=["GET"])
def get_cinema_rooms(cinema_id):
    """Get rooms for a specific cinema"""
    try:
        rooms = seance_service.get_rooms_by_cinema(cinema_id)
        return jsonify(rooms), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@seance.route("/cinema/<int:cinema_id>", methods=["GET"])
def get_cinema_details(cinema_id):
    """Get details for a specific cinema"""
    try:
        cinema = seance_service.get_cinema_by_id(cinema_id)
        if cinema:
            return jsonify(cinema), 200
        return jsonify({"message": "Cinema not found"}), 404
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@seance.route("/cinema/<int:cinema_id>/seances", methods=["GET"])
def get_cinema_seances(cinema_id):
    """Get upcoming seances for a specific cinema"""
    try:
        seances = seance_service.get_seances_by_cinema_id(cinema_id)
        return jsonify(seances), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@seance.route("/upcoming", methods=["GET"])
def get_upcoming():
    """Get upcoming seances with pagination"""
    try:
        limit = int(request.args.get("limit", 20))
        offset = int(request.args.get("offset", 0))
        seances = seance_service.get_upcoming_seances(limit, offset)
        return jsonify(seances), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@seance.route("/<ville_name>", methods=["GET"])
def get_seances_by_city(ville_name):
    """Get seances for a specific city"""
    try:
        available_seance = seance_service.get_seance_info_by_city_name(ville_name)
        response = jsonify(available_seance), 200
    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code
    return response


@seance.route("/", methods=["POST"])
@jwt_required()
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


@seance.route("/<int:seance_id>", methods=["DELETE"])
@jwt_required()
def delete_seance(seance_id):
    """
    Delete a seance.
    """
    claims = get_jwt()
    if not claims.get("is_admin"):
         return jsonify({"message": "Admin privileges required"}), 403

    try:
        seance_service.delete_seance(seance_id)
        return jsonify({"message": "Seance deleted successfully"}), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500

