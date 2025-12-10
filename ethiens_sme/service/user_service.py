import bcrypt
from ethiens_sme import app, connect_mysql
from ethiens_sme.service import admin_service

# Requetes SQL ici


def get_user_role(user_id):
    """Get user role"""
    with connect_mysql.connect() as conn:
        admin_service.verify_user(user_id)

        query = """
        SELECT r_id, u_id
        FROM uniride.ur_user
        WHERE u_id = %s
        """

        r_id = connect_mysql.get_query(conn, query, (user_id,))

    if not r_id:
        raise UserNotFoundException

    document = r_id[0]

    return {"role": document[0], "id": user_id}
