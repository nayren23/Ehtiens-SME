"""User seance modele"""

import dataclasses
from datetime import datetime


@dataclasses.dataclass
class SeanceModel:
    """Seance Model class"""

    id: int = None
    date_publication: datetime = None
    length_minutes: int = None
    minimum_age: str = None
    synopsis: str = None
    title: str = None
    poster: str = None
    country: str = None
    producer: str = None
    being_date: datetime = None
    end_date: datetime = None
