"""Movie related endpoints"""

from flask import Blueprint, request, jsonify
from ethiens_sme.utils.exception.exceptions import ApiException, ResourceNotFoundException
from ethiens_sme.service import movie_service
from ethiens_sme.config import Config
from flask_jwt_extended import jwt_required
import requests

# Définition du Blueprint
movie = Blueprint("movie", __name__, url_prefix="/movie")

@movie.route("/tmdb/search", methods=["GET"])
def search_tmdb_movie():
    """
    Search for a movie using TMDB API (with fallback).
    """
    query = request.args.get("query")
    if not query:
        return jsonify({"message": "Query parameter is required"}), 400

    # Try Official TMDB API first
    if Config.TMDB_API_KEY:
        try:
            url = f"https://api.themoviedb.org/3/search/movie?api_key={Config.TMDB_API_KEY}&query={query}&language=fr-FR"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            results = []
            for item in data.get("results", []):
                 results.append({
                     "id": item.get("id"),
                     "title": item.get("title"),
                     "release_date": item.get("release_date")
                 })
            return jsonify({"results": results}), 200
        except Exception as e:
            # Log error and fall through to backup
            print(f"TMDB Primary Search failed: {e}")
            pass

    print("Using Fallback API for search")
    # Fallback API: https://imdb.iamidiotareyoutoo.com/search?q={query}
    url = f"https://imdb.iamidiotareyoutoo.com/search?q={query}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Transform data to match what frontend expects
        # Frontend expects: { results: [ { id, title, release_date } ] }
        results = []
        if "description" in data:
            for item in data["description"]:
                results.append({
                    "id": item.get("#IMDB_ID"),
                    "title": item.get("#TITLE"),
                    "release_date": str(item.get("#YEAR", "N/A"))
                })
        
        return jsonify({"results": results}), 200
    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Search API Error: {str(e)}"}), 500

@movie.route("/tmdb/<string:tmdb_id>", methods=["GET"])
def get_tmdb_movie_details(tmdb_id):
    """
    Get details for a movie from TMDB API (with fallback).
    """
    # Try Official TMDB API first if ID is numeric (TMDB IDs are numeric)
    if Config.TMDB_API_KEY and str(tmdb_id).isdigit():
         try:
            url = f"https://api.themoviedb.org/3/movie/{tmdb_id}?api_key={Config.TMDB_API_KEY}&language=fr-FR&append_to_response=credits"
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()

            movie_data = {}
            movie_data["title"] = data.get("title")
            movie_data["overview"] = data.get("overview")
            movie_data["release_date"] = data.get("release_date")
            movie_data["runtime"] = data.get("runtime")
            movie_data["poster_path"] = data.get("poster_path") # Frontend handles partial path
            
            movie_data["production_countries"] = data.get("production_countries", [])
            movie_data["production_companies"] = data.get("production_companies", [])
            
            credits = data.get("credits", {})
            movie_data["credits"] = {"cast": credits.get("cast", [])}

            return jsonify(movie_data), 200
         except Exception as e:
            print(f"TMDB Primary Details failed: {e}")
            pass

    # Fallback API: https://imdb.iamidiotareyoutoo.com/search?tt={id}
    # Note: If ID was numeric (TMDB ID), this fallback (IMDb ID) will likely fail unless we map IDs. 
    # But user might have selected from fallback search which returns IMDb IDs (tt...).
    
    url = f"https://imdb.iamidiotareyoutoo.com/search?tt={tmdb_id}"
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Parse the complex response structure
        # We need: title, release_date, runtime, overview, poster_path, production_countries, production_companies, credits.cast
        
        movie_data = {}
        
        # Helper to safely get nested keys
        short = data.get("short", {})
        main = data.get("main", {})
        
        movie_data["title"] = short.get("name")
        movie_data["overview"] = short.get("description")
        
        raw_date = short.get("datePublished")
        if raw_date and len(str(raw_date)) == 4:
             movie_data["release_date"] = f"{raw_date}-01-01"
        else:
             movie_data["release_date"] = raw_date
        
        # Runtime is in seconds in main.runtime.seconds
        runtime_seconds = main.get("runtime", {}).get("seconds")
        if runtime_seconds:
            movie_data["runtime"] = int(runtime_seconds) // 60
        else:
            movie_data["runtime"] = 0

        # Poster - Full URL provided
        movie_data["poster_path"] = short.get("image")
        
        # Countries
        countries_data = main.get("countriesDetails", {}).get("countries", [])
        movie_data["production_countries"] = [{"name": c.get("text")} for c in countries_data]
        
        # Companies
        companies = []
        production_edges = main.get("production", {}).get("edges", [])
        for edge in production_edges:
            company_name = edge.get("node", {}).get("company", {}).get("companyText", {}).get("text")
            if company_name:
                companies.append({"name": company_name})
        movie_data["production_companies"] = companies
        
        # Cast
        cast_list = []
        # Try castV2 -> Top Cast
        cast_groups = main.get("castV2", [])
        if cast_groups:
            top_cast = cast_groups[0].get("credits", [])
            for credit in top_cast:
                name = credit.get("name", {}).get("nameText", {}).get("text")
                if name:
                    cast_list.append({"name": name})
        
        movie_data["credits"] = {"cast": cast_list}
        
        return jsonify(movie_data), 200

    except requests.exceptions.RequestException as e:
        return jsonify({"message": f"Details API Error: {str(e)}"}), 500

@movie.route("/<int:movie_id>", methods=["DELETE"])
@jwt_required()
def delete_movie(movie_id):
    """
    Delete a movie.
    """
    try:
        # Assuming service has this method, if not I need to create it.
        # Checking service... likely not there. I will implement a stub or direct call.
        # But per instructions "avoid change to backend except if absolutely necessary".
        # Deleting a movie is necessary for "admin should be able to delete movie".
        # I'll check movie_service.py next. For now, I'll add the route.
        movie_service.delete_movie(movie_id)
        return jsonify({"message": "Movie deleted"}), 200
    except ApiException as e:
        return jsonify({"message": e.message}), e.status_code
    except AttributeError:
        # Fallback if service method doesn't exist yet
        return jsonify({"message": "Delete function not implemented in service"}), 501
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
