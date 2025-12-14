"""User seance modele"""

import dataclasses
from datetime import datetime


@dataclasses.dataclass
class SeanceModel:
    """Seance Model class representation"""

    movie_title: str
    date_time: datetime
    room: str
    language: str
    cinema_name: str
    city: str
