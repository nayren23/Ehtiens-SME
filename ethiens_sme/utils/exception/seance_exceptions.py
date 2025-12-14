"""Exceptions for Seance Model endpoints"""

from ethiens_sme.utils.exception.exceptions import ApiException


class SeanceAlreadyExist(ApiException):
    """Exception for when an invalid intermediate seance is encountered"""

    def __init__(self):
        super().__init__("SEANCE_ALREADY_EXIST", 422)


class SeanceNotFoundException(ApiException):
    """Exception for when the seance isn't found"""

    def __init__(self, message):
        super().__init__(message, 422)
