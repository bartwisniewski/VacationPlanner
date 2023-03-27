from dataclasses import dataclass
from datetime import datetime, timedelta, date
from places.forms import PlaceScrapForm
from places.helpers import date_2_datetime


@dataclass
class Query:
    region: str = "Poland"
    adults: int = 2
    children: int = 0
    infants: int = 0
    start_date: datetime = datetime.now()
    end_date: datetime = datetime.now() + timedelta(days=7)

    @staticmethod
    def from_form(form: PlaceScrapForm):
        data = form.cleaned_data
        start_datetime = date_2_datetime(data["start"])
        end_datetime = date_2_datetime(data["end"])
        return Query(
            region=data["region"],
            adults=data["adults"],
            children=data["children"],
            infants=data["infants"],
            start_date=start_datetime,
            end_date=end_datetime,
        )


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
