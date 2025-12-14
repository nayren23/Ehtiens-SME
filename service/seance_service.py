"""
Docstring for Ehtiens-SME.ethiens_sme.service.seance_service
"""

from ethiens_sme import connect_mysql
from ethiens_sme.model.seance_model import SeanceModel


def get_seance_info_by_city_name(city_name) -> SeanceModel:
    """Get car information by seance name"""
    query = """
        SELECT
            m.mo_title AS Titre_Film,
            s.se_date_time AS Date_Heure,
            s.se_room AS Salle,
            s.se_language AS Langue,
            c.ci_cinema_name AS Cinema,
            c.ci_city AS Ville
        FROM
            et_seance AS s
        JOIN
            et_cinema AS c ON s.ci_id_cinema = c.ci_id_cinema
        JOIN
            et_movie AS m ON s.mo_id_movie = m.mo_id_movie
        WHERE
            c.ci_city = %s;
    """
    params = (city_name,)
    conn = connect_mysql.connect()
    results = connect_mysql.get_query(conn, query, params, True)
    connect_mysql.disconnect(conn)

    if not results:
        return []

    seances_list = []

    for row in results:
        seance = SeanceModel(
            movie_title=row["Titre_Film"],
            date_time=row["Date_Heure"],
            room=row["Salle"],
            language=row["Langue"],
            cinema_name=row["Cinema"],
            city=row["Ville"],
        )
        seances_list.append(seance)

    return seances_list


def create_seance(data: dict) -> int:
    """Create a new seance"""

    query = """
        INSERT INTO et_seance (
            se_date_time,
            se_room,
            se_language,
            mo_id_movie,
            ci_id_cinema
        ) VALUES (%s, %s, %s, %s, %s);
    """

    params = (
        data.get("date_time"),  # Format 'YYYY-MM-DD HH:MM:SS'
        data.get("room"),
        data.get("language"),  # Ex: 'VOSTFR' ou 'VF'
        data.get("movie_id"),
        data.get("cinema_id"),
    )

    conn = connect_mysql.connect()
    try:
        connect_mysql.execute_command(conn, query, params)

        res_id = connect_mysql.get_query(conn, "SELECT LAST_INSERT_ID() as id;", None, True)
        new_id = res_id[0]["id"]

        return new_id
    finally:
        connect_mysql.disconnect(conn)


def get_upcoming_seances(limit: int = 20, offset: int = 0) -> list:
    """Get all upcoming seances with pagination"""
    query = """
        SELECT
            s.se_id_seance,
            m.mo_id_movie,
            m.mo_title AS Titre_Film,
            m.mo_poster AS Affiche_Film,
            s.se_date_time AS Date_Heure,
            s.se_room AS Salle,
            s.se_language AS Langue,
            c.ci_id_cinema,
            c.ci_cinema_name AS Cinema,
            c.ci_city AS Ville
        FROM
            et_seance AS s
        JOIN
            et_cinema AS c ON s.ci_id_cinema = c.ci_id_cinema
        JOIN
            et_movie AS m ON s.mo_id_movie = m.mo_id_movie
        WHERE
            s.se_date_time >= NOW()
        ORDER BY
            s.se_date_time ASC, s.se_id_seance ASC
        LIMIT %s OFFSET %s;
    """
    conn = connect_mysql.connect()
    results = connect_mysql.get_query(conn, query, (limit, offset), True)
    connect_mysql.disconnect(conn)

    if not results:
        return []

    seances_list = []
    for row in results:
        # Create a dictionary that mimics the structure plus the image
        seance = {
            "seance_id": row["se_id_seance"],
            "movie_id": row["mo_id_movie"],
            "movie_title": row["Titre_Film"],
            "movie_poster": row.get("Affiche_Film"),
            "date_time": row["Date_Heure"],
            "room": row["Salle"],
            "language": row["Langue"],
            "cinema_id": row["ci_id_cinema"],
            "cinema_name": row["Cinema"],
            "city": row["Ville"]
        }
        seances_list.append(seance)
    return seances_list


def get_rooms_by_cinema(cinema_id: int) -> list:
    """
    Get list of rooms used by a cinema. 
    Since there is no room table, we query distinct rooms from existing seances.
    We also add some default rooms if the list is short.
    """
    import re

    def natural_sort_key(s):
        return [int(text) if text.isdigit() else text.lower() for text in re.split('([0-9]+)', s)]

    query = "SELECT DISTINCT se_room FROM et_seance WHERE ci_id_cinema = %s;"
    conn = connect_mysql.connect()
    try:
        results = connect_mysql.get_query(conn, query, (cinema_id,), True)
        rooms = [row['se_room'] for row in results] if results else []
        
        # Merge with default rooms to ensure the dropdown isn't empty for new cinemas
        default_rooms = [f"Salle {i}" for i in range(1, 11)]
        all_rooms = list(set(rooms + default_rooms))
        
        # Sort naturally (Salle 2 before Salle 10)
        all_rooms.sort(key=natural_sort_key)
        
        return all_rooms
    finally:
        connect_mysql.disconnect(conn)


def get_all_cinemas() -> list:
    """Get all cinemas simple list"""
    query = "SELECT ci_id_cinema, ci_cinema_name, ci_city FROM et_cinema ORDER BY ci_cinema_name;"
    conn = connect_mysql.connect()
    try:
        results = connect_mysql.get_query(conn, query, None, True)
        return results if results else []
    finally:
        connect_mysql.disconnect(conn)


def delete_seance(seance_id: int):
    """Delete a seance by ID"""
    query = "DELETE FROM et_seance WHERE se_id_seance = %s;"
    conn = connect_mysql.connect()
    try:
        connect_mysql.execute_command(conn, query, (seance_id,))
    finally:
        connect_mysql.disconnect(conn)


def get_cinema_by_id(cinema_id: int) -> dict:
    """Get cinema details by ID"""
    query = "SELECT * FROM et_cinema WHERE ci_id_cinema = %s;"
    conn = connect_mysql.connect()
    try:
        results = connect_mysql.get_query(conn, query, (cinema_id,), True)
        if results:
            return results[0]
        return None
    finally:
        connect_mysql.disconnect(conn)

def get_dashboard_stats() -> dict:
    """Get statistics for the dashboard"""
    conn = connect_mysql.connect()
    try:
        # Count Movies
        res_mov = connect_mysql.get_query(conn, "SELECT COUNT(*) as c FROM et_movie", None, True)
        count_movies = res_mov[0]['c'] if res_mov else 0
        
        # Count Cinemas
        res_cin = connect_mysql.get_query(conn, "SELECT COUNT(*) as c FROM et_cinema", None, True)
        count_cinemas = res_cin[0]['c'] if res_cin else 0
        
        # Count Seances (This week? Or total upcoming? Dashboard says "Séances cette semaine")
        # Let's do total upcoming for now, or specific range. 
        # "Séances cette semaine" implies range.
        # Let's just do total upcoming to be safe/simple, or range NOW to NOW+7 days.
        query_seance = "SELECT COUNT(*) as c FROM et_seance WHERE se_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 7 DAY)"
        res_sea = connect_mysql.get_query(conn, query_seance, None, True)
        count_seances = res_sea[0]['c'] if res_sea else 0
        
        return {
            "movies": count_movies,
            "cinemas": count_cinemas,
            "seances": count_seances
        }
    finally:
        connect_mysql.disconnect(conn)

def get_seances_by_cinema_id(cinema_id: int) -> list:
    """Get upcoming seances for a specific cinema"""
    query = """
        SELECT
            m.mo_id_movie,
            m.mo_title AS Titre_Film,
            m.mo_poster AS Affiche_Film,
            s.se_date_time AS Date_Heure,
            s.se_room AS Salle,
            s.se_language AS Langue
        FROM
            et_seance AS s
        JOIN
            et_movie AS m ON s.mo_id_movie = m.mo_id_movie
        WHERE
            s.ci_id_cinema = %s
            AND s.se_date_time >= NOW()
        ORDER BY
            s.se_date_time ASC;
    """
    conn = connect_mysql.connect()
    try:
        results = connect_mysql.get_query(conn, query, (cinema_id,), True)
        seances_list = []
        if results:
            for row in results:
                seance = {
                    "movie_id": row["mo_id_movie"],
                    "movie_title": row["Titre_Film"],
                    "movie_poster": row.get("Affiche_Film"),
                    "date_time": row["Date_Heure"],
                    "room": row["Salle"],
                    "language": row["Langue"]
                }
                seances_list.append(seance)
        return seances_list
    finally:
        connect_mysql.disconnect(conn)



