"""Movie related endpoints"""

from flask import Blueprint, request, jsonify
from ethiens_sme.utils.exception.exceptions import ApiException, ResourceNotFoundException
from ethiens_sme.service import movie_service
from flask_jwt_extended import jwt_required, get_jwt

# Définition du Blueprint
movie = Blueprint("movie", __name__, url_prefix="/movie")

@movie.route("/tmdb/search", methods=["GET"])
def search_tmdb_movie():
    """
    Search for a movie using TMDB API.
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    results = movie_service.search_tmdb_movie(query)
    return jsonify({"results": results}), 200

@movie.route("/tmdb/<string:tmdb_id>", methods=["GET"])
def get_tmdb_movie_details(tmdb_id):
    """
    Get details for a movie from TMDB API.
    """
    movie_data = movie_service.get_tmdb_movie_details_from_api(tmdb_id)
    if movie_data:
        return jsonify(movie_data), 200
    else:
        return jsonify({"message": "Movie not found or TMDB unavailable"}), 404

@movie.route("/<int:movie_id>", methods=["DELETE"])
@jwt_required()
def delete_movie(movie_id):
    """
    Delete a movie.
    """
    claims = get_jwt()
    if not claims.get("is_admin"):
         return jsonify({"message": "Admin privileges required"}), 403

    try:
        movie_service.delete_movie(movie_id)
        return jsonify({"message": "Movie deleted"}), 200
    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@movie.route("/details/<int:movie_id>", methods=["GET"])
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

        # Sanitize inputs to match DB schema
        if data.get("title") and len(data["title"]) > 150:
            data["title"] = data["title"][:150]
        if data.get("country") and len(data["country"]) > 50:
            data["country"] = data["country"][:50]

        new_id = movie_service.create_movie(data)
        return jsonify({"message": "Movie created", "id": new_id}), 201

    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code
    except Exception as e:
        return jsonify({"message": str(e)}), 500


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

@movie.route("/all", methods=["GET"])
def get_all_movies():
    """
    Get all movies with details (for main page display).
    Supports pagination via limit/offset.
    """
    try:
        limit = request.args.get('limit', 20, type=int)
        offset = request.args.get('offset', 0, type=int)
        movies = movie_service.get_all_movies_paginated(limit, offset)
        return jsonify(movies), 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500