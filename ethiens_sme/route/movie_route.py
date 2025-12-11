from flask import Blueprint, request, jsonify
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.service import movie_service

# Définition du Blueprint
movie = Blueprint("movie", __name__, url_prefix="/movie")


@movie.route("/<int:movie_id>", methods=["GET"])
def get_movie_details(movie_id):
    """
    Get detailed information about a specific movie.
    Corresponds to Question 3: displaying details given in Question 1.
    """
    try:
        movie_details = movie_service.get_movie_details_by_id(movie_id)
        response = jsonify(movie_details), 200

    except ApiException as e:
        response = jsonify({"message": e.message}), e.status_code

    return response


@movie.route("/", methods=["POST"])
def create_new_movie():
    """
    Create a new movie with its details and actors.
    Expected JSON:
    {
        "title": "Titanic",
        "length_minutes": 195,
        "minimum_age": "12",
        "synopsis": "Un bateau coule...",
        "producer": "James Cameron",
        "date_publication": "1997-01-01",
        "being_date": "2025-01-01",
        "end_date": "2025-02-01",
        "actor_ids": [1, 2]
    }
    """
    try:
        data = request.get_json()

        # Validation basique
        if not data or not data.get("title"):
            return jsonify({"message": "Title is required"}), 400

        new_id = movie_service.create_movie(data)

        return jsonify({"message": "Movie created successfully", "id": new_id}), 201

    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code
    except Exception as e:
        return jsonify({"message": str(e)}), 500
