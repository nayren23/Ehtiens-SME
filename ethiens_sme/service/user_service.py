"""
Docstring for Ehtiens-SME.ethiens_sme.service.user_service
"""

import bcrypt
from ethiens_sme import app, connect_mysql
from ethiens_sme.model.user_model import UserModel
from ethiens_sme.utils.exception.exceptions import MissingInputException

from ethiens_sme.utils.exception.user_exceptions import (
    UserNotFoundException,
    PasswordIncorrectException,
)


def authenticate(login, password) -> UserModel:
    """authenticate the user"""
    # check if exist
    if not login:
        raise MissingInputException("LOGIN_MISSING")
    if not password:
        raise MissingInputException("PASSWORD_MISSING")

    user_bo = get_user_by_login(login)
    _verify_password(password, user_bo.password)
    return user_bo


def get_user_by_login(login) -> UserModel:
    """Get user infos from db using the login"""
    return _get_user_by_identifier(login, "u_login")


def _verify_password(password, hashed_password) -> bool:
    """Verify the password is correct"""
    if not bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8")):
        raise PasswordIncorrectException()


def _get_user_by_identifier(identifier, identifier_type) -> UserModel:
    """Get user infos from db"""
    if not identifier and not identifier_type:
        raise MissingInputException("IDENTIFIER_MISSING")

    query = f"select * from uniride.ur_user where {identifier_type} = %s"
    params = (identifier,)

    conn = connect_mysql.connect()
    infos = connect_mysql.get_query(conn, query, params, True)
    connect_mysql.disconnect(conn)

    if not infos:
        raise UserNotFoundException()
    infos = infos[0]

    user_bo = UserModel(
        id=infos["us_id_user "],
        pseudo=infos["us_pseudo "],
        password=infos["us_password "],
    )
    return user_bo


def _verify_password(password, hashed_password) -> bool:
    """Verify the password is correct"""
    if not bcrypt.checkpw(password.encode("utf8"), hashed_password.encode("utf8")):
        raise PasswordIncorrectException()


def _hash_password(password) -> str:
    """Hash the password"""
    salt = app.config["JWT_SALT"]
    password = password.encode("utf8")
    password = bcrypt.hashpw(password, salt)
    # convert back to string
    return str(password, "utf8")
