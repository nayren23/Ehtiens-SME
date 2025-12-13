"""
Docstring for Ehtiens-SME.ethiens_sme.service.movie_service
"""

from typing import List
from ethiens_sme import connect_mysql
from ethiens_sme.model.movie_model import MovieModel
from ethiens_sme.utils.exception.exceptions import ResourceNotFoundException
from ethiens_sme.model.actor_model import ActorModel
from ethiens_sme.service import actor_service


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
        query_movie = """
            SELECT * FROM et_movie WHERE mo_id_movie = %s;
        """
        movie_results = connect_mysql.get_query(conn, query_movie, (movie_id,), True)

        if not movie_results:
            raise ResourceNotFoundException(f"Movie with id {movie_id} not found")

        row = movie_results[0]

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
            being_date=row["mo_begin_date"],
            end_date=row["mo_end_date"],
            actors=[],
        )
        movie.actors = get_actors_by_movie_id(conn, movie_id)

        return movie

    finally:
        connect_mysql.disconnect(conn)


def create_movie(data: dict) -> int:
    """
    Create a new movie.
    Actors are passed by name. They are created if they don't exist.
    """
    conn = connect_mysql.connect()

    try:
        query_movie = """
            INSERT INTO et_movie (
                mo_title, mo_date_publication, mo_length_minutes,
                mo_minimum_age, mo_synopsis, mo_poster,
                mo_country, mo_producer, mo_begin_date, mo_end_date
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
            data.get("producer"),
            data.get("begin_date"),
            data.get("end_date"),
        )

        # Use execute_command to ensure the INSERT is committed
        connect_mysql.execute_command(conn, query_movie, params_movie)

        query_get_id = "SELECT MAX(mo_id_movie) as id FROM et_movie;"
        # Or SELECT LAST_INSERT_ID() if we are sure it's the same connection/session. 
        # Since we pass 'conn', it is the same session.
        # But let's be safe with LAST_INSERT_ID() in the same session context if possible, 
        # or just MAX(id) if traffic is low (risky). 
        # Actually, execute_command commits, so the ID is safe.
        # But execute_command returns `lastrowid` if configured? 
        # Let's check execute_command implementation in connect_mysql.py... 
        # It returns `cur.lastrowid` if "returning" is in query... wait, that's postgres style logic in a mysql file?
        # The file says: if "returning" in query.lower(): returning_value = cur.lastrowid
        # For MySQL INSERT, lastrowid is available on the cursor.
        
        # Simpler approach: Just get the ID.
        res_id = connect_mysql.get_query(conn, "SELECT LAST_INSERT_ID() as id;", None, True)
        new_movie_id = res_id[0]["id"]
        
        actor_names = data.get("actor_names", [])

        if actor_names:
            query_casting = "INSERT INTO et_casting (mo_id_movie, ac_id_actor) VALUES (%s, %s);"

            for name in actor_names:
                clean_name = name.strip()
                if clean_name:
                    actor_id = actor_service.get_or_create_actor(conn, clean_name)
                    connect_mysql.execute_command(conn, query_casting, (new_movie_id, actor_id))

        return new_movie_id

    except Exception as e:
        raise e
    finally:
        connect_mysql.disconnect(conn)


def delete_movie(movie_id: int):
    """
    Delete a movie by ID.
    First removes casting associations and seances, then the movie.
    """
    conn = connect_mysql.connect()
    try:
        # Delete casting first
        query_delete_casting = "DELETE FROM et_casting WHERE mo_id_movie = %s;"
        connect_mysql.execute_command(conn, query_delete_casting, (movie_id,))
        
        # Delete seances
        query_delete_seance = "DELETE FROM et_seance WHERE mo_id_movie = %s;"
        connect_mysql.execute_command(conn, query_delete_seance, (movie_id,))

        query_delete_movie = "DELETE FROM et_movie WHERE mo_id_movie = %s;"
        connect_mysql.execute_command(conn, query_delete_movie, (movie_id,))
    finally:
        connect_mysql.disconnect(conn)



def get_all_movies_simple() -> list:
    """
    Get a lightweight list of all movies (ID and Title only).
    Useful for dropdown menus.
    """
    query = "SELECT mo_id_movie, mo_title FROM et_movie ORDER BY mo_title ASC;"

    conn = connect_mysql.connect()
    try:
        results = connect_mysql.get_query(conn, query, None, True)

        movies_list = []
        if results:
            for row in results:
                movies_list.append({"id": row["mo_id_movie"], "title": row["mo_title"]})
        return movies_list
    finally:
        connect_mysql.disconnect(conn)
