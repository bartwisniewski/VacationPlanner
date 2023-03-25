from dataclasses import dataclass
from datetime import datetime

# defaults
@dataclass
class Query:
    region: str
    adults: int
    children: int
    infants: int
    start_date: datetime
    end_date: datetime


@dataclass
class Place:
    name: str = ""
    url: str = ""
    description: str = ""
    address: str = ""
    city: str = ""
    country: str = ""
    region: str = ""
    place_type: str = ""
    owner_name: str = ""
    owner_phone: str = ""
    owner_email: str = ""
    adults: int = 1
    children: int = 0
    infants: int = 0
    bedrooms: int = 1
    bathrooms: int = 1
    living_rooms: int = 0
    kitchens: int = 0
    price: float = 0.0

    def __str__(self):
        return f"""{self.name}
{self.description}
{self.address} {self.city} {self.country}"""
