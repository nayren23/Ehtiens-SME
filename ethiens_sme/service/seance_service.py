# function pour chercer toutes les séances dans une ville

"""
Docstring for Ehtiens-SME.ethiens_sme.service.seance_service
"""

from ethiens_sme import app, connect_mysql
from ethiens_sme.model.seance_model import SeanceModel
from ethiens_sme.utils.exception.exceptions import MissingInputException

from ethiens_sme.utils.exception.user_exceptions import (
    UserNotFoundException,
    PasswordIncorrectException,
)


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
