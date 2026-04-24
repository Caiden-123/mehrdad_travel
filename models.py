from datetime import date, datetime
from dataclasses import dataclass

@dataclass
class Holiday:  # make sure this matches the database
    id: str
    location: str
    departure_date: date
    duration: int
    outbound_plane_id: str
    return_plane_id: str

    def __post_init(self):
        if len(self.id) != 5:
            raise Exception(f"Invalid holiday id {self.id}")


        



    
@dataclass
class Customer:
    id: str
    forename: str
    surname: str
    telephone: str
    

@dataclass
class Booking:
    customer: Customer
    holiday: Holiday
    num_guest: int

@dataclass
class Allergen:
    id: int
    name: str

@dataclass
class Guest:
    id: int
    booking: Booking
    name: str
    allergens: list[Allergen]

@dataclass
class Food:
    id: int
    guest: Guest
    choice: str
    
@dataclass
class PlaneJourney:
    id: str
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    airline: str
    duration: int