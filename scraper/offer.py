from dataclasses import dataclass
from typing import Optional


@dataclass
class Offer:
    id: int
    title: str
    description: Optional[str]
    url: str
    map_url: Optional[str]
    district: Optional[str]
    price: Optional[str]
    rent: Optional[str]
    pets: Optional[str]
    furnished: Optional[bool]
    rooms: Optional[str]
    floor: Optional[str]
    area: Optional[str]
    elevator: Optional[bool]
    buildtype: Optional[str]
    created_at: Optional[str]
    rented_at: Optional[str]
    status: Optional[str]
