import dataclasses


@dataclasses.dataclass
class ActorModel:
    """Actor Model class representation"""

    id: int
    name: str
    picture: str
