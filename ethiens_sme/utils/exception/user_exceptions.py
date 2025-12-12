"""Exceptions for UserBO endpoints"""

from ethiens_sme.utils.exception.exceptions import ApiException


class UserNotFoundException(ApiException):
    """Exception for when the user isn't found"""

    def __init__(self):
        super().__init__("USER_NOT_FOUND", 422)


class PasswordIncorrectException(ApiException):
    """Exception for when password is incorrect"""

    def __init__(self):
        super().__init__("PASSWORD_INCORRECT", 422)


class UserNotAUTHORIZED(ApiException):
    """Exception for when the user isn't authorized"""

    def __init__(self):
        super().__init__("USER_NOT_AUTHORIZED", 422)
