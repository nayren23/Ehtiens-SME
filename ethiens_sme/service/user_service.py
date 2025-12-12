"""
Docstring for Ehtiens-SME.ethiens_sme.service.user_service
"""

import bcrypt
from ethiens_sme import connect_mysql
from ethiens_sme.model.user_model import UserModel
from ethiens_sme.utils.exception.exceptions import MissingInputException

from ethiens_sme.utils.exception.user_exceptions import (
    UserNotFoundException,
    PasswordIncorrectException,
)


def authenticate(login, password) -> UserModel:
    """authenticate the user"""
    if not login:
        raise MissingInputException("LOGIN_MISSING")
    if not password:
        raise MissingInputException("PASSWORD_MISSING")

    user_bo = get_user_by_login(login)

    # On vérifie le mot de passe
    if not _verify_password(password, user_bo.password):
        raise PasswordIncorrectException()

    return user_bo


def get_user_by_login(login) -> UserModel:
    """Get user infos from db using the pseudo as login"""
    conn = connect_mysql.connect()
    try:
        query = "SELECT * FROM et_user WHERE us_pseudo = %s"
        params = (login,)

        infos = connect_mysql.get_query(conn, query, params, True)

        if not infos:
            raise UserNotFoundException()

        row = infos[0]

        user_bo = UserModel(
            id=row["us_id_user"],
            pseudo=row["us_pseudo"],
            password=row["us_password"],
        )
        return user_bo
    finally:
        connect_mysql.disconnect(conn)


def _verify_password(password, hashed_password) -> bool:
    """Verify the password is correct"""
    if isinstance(hashed_password, str):
        hashed_password = hashed_password.encode("utf-8")

    return bcrypt.checkpw(password.encode("utf8"), hashed_password)
