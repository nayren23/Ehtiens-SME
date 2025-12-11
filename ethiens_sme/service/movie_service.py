"""
Docstring for Ehtiens-SME.ethiens_sme.service.movie_service
"""

from ethiens_sme import app, connect_mysql
from ethiens_sme.model.movie_model import MovieModel
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.model.actor_model import ActorModel


def get_movie_details_by_id(movie_id: int) -> MovieModel:
    """Get detailed information about a movie AND its casting by its ID"""

    conn = connect_mysql.connect()

    # --- REQUÊTE 1 : Les infos du film ---
    query_movie = """
        SELECT * FROM et_movie WHERE mo_id_movie = %s;
    """
    movie_results = connect_mysql.get_query(conn, query_movie, (movie_id,), True)

    if not movie_results:
        connect_mysql.disconnect(conn)
        raise Exception(f"Movie with id {movie_id} not found")

    row = movie_results[0]

    # Création de l'objet Movie
    movie = MovieModel(
        id=row["mo_id_movie"],
        date_publication=row["mo_date_publication"],
        length_minutes=row["mo_length_minutes"],
        minimum_age=row["mo_minimum_age"],
        synopsis=row["mo_synopsis"],
        title=row["mo_title"],
        poster=row["mo_poster"],
        country=row["mo_country"],
        producer=row["mo_producer"],
        being_date=row["mo_being_date"],
        end_date=row["mo_end_date"],
        actors=[],  # On initialise la liste vide pour l'instant
    )

    # --- REQUÊTE 2 : Les acteurs du film ---
    # On joint et_actors avec et_casting pour filtrer par l'ID du film
    query_actors = """
        SELECT 
            a.ac_id_actor, 
            a.ac_actor_name, 
            a.ac_actor_picture
        FROM 
            et_actors AS a
        JOIN 
            et_casting AS c ON a.ac_id_actor = c.ac_id_actor
        WHERE 
            c.mo_id_movie = %s;
    """

    actors_results = connect_mysql.get_query(conn, query_actors, (movie_id,), True)
    connect_mysql.disconnect(conn)

    # Remplissage de la liste des acteurs
    if actors_results:
        for actor_row in actors_results:
            actor = ActorModel(
                id=actor_row["ac_id_actor"], name=actor_row["ac_actor_name"], picture=actor_row["ac_actor_picture"]
            )
            movie.actors.append(actor)

    return movie
