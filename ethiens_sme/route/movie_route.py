from flask import Blueprint, jsonify
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
