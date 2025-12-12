"""Movie related endpoints"""

from flask import Blueprint, request, jsonify
from ethiens_sme.utils.exception.exceptions import ApiException, ResourceNotFoundException
from ethiens_sme.service import movie_service
from flask_jwt_extended import jwt_required

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
@jwt_required()
def create_new_movie():
    """
    Create a new movie with its details and actors.
    """
    try:
        data = request.get_json()
        if not data or not data.get("title"):
            return jsonify({"message": "Title is required"}), 400

        new_id = movie_service.create_movie(data)
        return jsonify({"message": "Movie created", "id": new_id}), 201

    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code


@movie.route("/list", methods=["GET"])
def get_movies_list():
    """
    Get a simple list of movies (id, title).
    Used to populate select inputs in the frontend.
    """
    try:
        movies = movie_service.get_all_movies_simple()
        return jsonify(movies), 200
    except ResourceNotFoundException as e:
        return jsonify({"message": str(e)}), 500
