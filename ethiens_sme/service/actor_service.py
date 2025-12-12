"""
Service for Actor related operations
"""

from ethiens_sme import connect_mysql


def get_or_create_actor(conn, actor_name: str) -> int:
    """
    Check if an actor exists by name.
    If yes, return their ID.
    If no, create them and return the new ID.
    """
    query_check = "SELECT ac_id_actor FROM et_actors WHERE ac_actor_name = %s;"
    result = connect_mysql.get_query(conn, query_check, (actor_name,), True)

    if result:
        return result[0]["ac_id_actor"]

    query_insert = "INSERT INTO et_actors (ac_actor_name, ac_actor_picture) VALUES (%s, NULL);"
    connect_mysql.execute_command(conn, query_insert, (actor_name,))

    query_last_id = "SELECT LAST_INSERT_ID() as id;"
    res_id = connect_mysql.get_query(conn, query_last_id, None, True)

    return res_id[0]["id"]
