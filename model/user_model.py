"""User model module"""

import dataclasses


@dataclasses.dataclass
class UserModel:
    """User business object class"""

    id: int = None
    pseudo: str = None
    password: str = None
    is_admin: bool = False
