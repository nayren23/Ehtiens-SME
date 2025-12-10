"""User model module"""

import dataclasses
from datetime import datetime


@dataclasses.dataclass
class UserModel:
    """User business object class"""

    id: int = None
    pseudo: str = None
    password: str = None
