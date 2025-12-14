"""User seance modele"""

import dataclasses
from datetime import date
from typing import List
from ethiens_sme.model.actor_model import ActorModel


@dataclasses.dataclass
class MovieModel:
    """Movie Model class representation"""

    id: int = None
    date_publication: date = None
    length_minutes: int = None
    minimum_age: str = None
    synopsis: str = None
    title: str = None
    poster: str = None
    country: str = None
    producer: str = None
    being_date: date = None
    end_date: date = None
    actors: List[ActorModel] = dataclasses.field(default_factory=list)
