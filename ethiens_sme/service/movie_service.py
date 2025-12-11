"""
Docstring for Ehtiens-SME.ethiens_sme.service.movie_service
"""

from ethiens_sme import app, connect_mysql
from ethiens_sme.model.movie_model import MovieModel
from ethiens_sme.utils.exception.exceptions import ApiException
from ethiens_sme.model.actor_model import ActorModel
from typing import List


def get_actors_by_movie_id(conn, movie_id: int) -> List[ActorModel]:
    """
    Helper function to get actors list by movie ID.
    Uses an existing database connection.
    """
    actors_list = []

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

    # On utilise la connexion passée en paramètre
    actors_results = connect_mysql.get_query(conn, query_actors, (movie_id,), True)

    if actors_results:
        for actor_row in actors_results:
            actor = ActorModel(
                id=actor_row["ac_id_actor"], name=actor_row["ac_actor_name"], picture=actor_row["ac_actor_picture"]
            )
            actors_list.append(actor)

    return actors_list


def get_movie_details_by_id(movie_id: int) -> MovieModel:
    """Get detailed information about a movie AND its casting by its ID"""

    conn = connect_mysql.connect()

    try:
        # --- REQUÊTE 1 : Les infos du film ---
        query_movie = """
            SELECT * FROM et_movie WHERE mo_id_movie = %s;
        """
        movie_results = connect_mysql.get_query(conn, query_movie, (movie_id,), True)

        if not movie_results:
            # On raise l'exception ici, le finally se chargera de la déconnexion
            raise Exception(f"Movie with id {movie_id} not found")

        row = movie_results[0]

        # Création de l'objet Movie sans les acteurs pour l'instant
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
            actors=[],
        )

        # --- APPEL DE LA FONCTION SEPARÉE (REQUÊTE 2) ---
        # On passe la connexion 'conn' et l'id du film
        movie.actors = get_actors_by_movie_id(conn, movie_id)

        return movie

    finally:
        # Le bloc finally s'exécute toujours (succès ou erreur), assurant la déconnexion
        connect_mysql.disconnect(conn)


def create_movie(data: dict) -> int:
    """
    Create a new movie and link actors.
    Returns the new movie ID.
    """
    conn = connect_mysql.connect()

    try:
        # 1. Insertion du film
        query_movie = """
            INSERT INTO et_movie (
                mo_title, mo_date_publication, mo_length_minutes, 
                mo_minimum_age, mo_synopsis, mo_poster, 
                mo_country, mo_producer, mo_being_date, mo_end_date
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
        """

        params_movie = (
            data.get("title"),
            data.get("date_publication"),
            data.get("length_minutes"),
            data.get("minimum_age"),
            data.get("synopsis"),
            data.get("poster"),
            data.get("country"),
            data.get("producer"),  # Correspond au Réalisateur/Producteur
            data.get("being_date"),  # Date début diffusion
            data.get("end_date"),  # Date fin diffusion
        )

        connect_mysql.get_query(conn, query_movie, params_movie)

        query_get_id = "SELECT LAST_INSERT_ID() as id;"
        res_id = connect_mysql.get_query(conn, query_get_id, None, True)
        new_movie_id = res_id[0]["id"]
        actor_ids = data.get("actor_ids", [])

        if actor_ids:
            query_casting = "INSERT INTO et_casting (mo_id_movie, ac_id_actor) VALUES (%s, %s);"
            for actor_id in actor_ids:
                connect_mysql.execute_command(conn, query_casting, (new_movie_id, actor_id))
        conn.commit()
        return new_movie_id

    except Exception as e:
        conn.rollback()
        raise e
    finally:
        connect_mysql.disconnect(conn)
