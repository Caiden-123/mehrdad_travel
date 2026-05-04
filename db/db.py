from typing import Tuple
from random import randint
import sqlite3

# test

from models import *

class DatabaseError(Exception):
    pass

class Database:
    def __enter__(self):
        self.__conn = sqlite3.connect("./db/holidays.db")
        self.__cursor = self.__conn.cursor()
        return self

    def __exit__(self, *args):
        
        self.__conn.close()
    
    def add_new_customer(self, forename: str, surname: str, telephone: str):
        id_ = forename[0] + surname[:2].upper() + str(randint(111, 999))
        self.__cursor.execute(f"INSERT INTO Customer VALUES ('{id_}', '{forename}', '{surname}', '{telephone}')")
        self.__conn.commit()

    def get_all_customers(self) -> Tuple[Tuple]:    
        records = self.__cursor.execute("SELECT * FROM Customer").fetchall()
        return records
    
    def get_holidays_by_location(self, location: str) -> Tuple[Holiday]:
        records = self.__cursor.execute("SELECT * FROM Holiday WHERE Location = ?", (location,)).fetchall()

        return [Holiday(*record) for record in records]

        #return records # at the mo this is a tuple of tuples
    
    def get_holiday_by_id(self, holiday_id) -> Holiday | None:
        record = self.__cursor.execute("SELECT * FROM Holiday WHERE HolidayID = ?", (holiday_id,)).fetchone()

        return Holiday(*record)

    def create_new_customer(self, forename : str, surname: str, telephone : str) -> Customer:
        """work out the new customer's ID
        write the new customer to the database
        return the new customer as a Customer object"""
        id = forename[0] + surname[:2] + str(randint(0,999).zfll(3))
        self.__cursor.execute(f"INSERT INTO CUSTOMER VALUES( '{id}', '{forename}', '{surname}', '{telephone}') ")

        return Customer(id, forename, surname, telephone)

    def get_customer_by_names(self, forename : str, surname: str) -> Customer | None:
        """ look in the database to find a customer
        if it exists, return the cusomter as a Customer
        if it doesn't, return None"""
        record = self.__cursor.execute(f"SELECT * FROM CUSTOMER WHERE Forename = '{forename}' and Surname = '{surname}'").fetchone()
        if record:
            return Customer(*record)
        return None

    def get_allergen_by_name(self, allergen_name) -> Allergen | None:
        """ look in the database to find an allergen 
        if it exsists, return the Allergen object
        if it doesn't return the Allergen Object
        if it doesn't return None"""
        record = self.__cursor.execute(f"SELECT * FROM ALLERGEN WHERE AllergenName = '{allergen_name}'").fetchone()
        if record:
            return Allergen(*record)
        return None


    def create_new_guest(self, guest_name: str, booking : Booking, allergies : list[Allergen]) -> Guest:
        """write a new guest to the database (priary key will be made automatically
        associate the new guest with their allergies)
        return the new guest as a Guest"""
        guest_id = self.__cursor.execute("INSERT INTO GUEST VALUES (NULL, ?, ?) RETURNING GUEST.GuestID", (Booking.id, guest_name)).fetchone()

        query = ""
        for allergen in allergies:
            query += f"INSERT INTO GUEST_ALLERGEN VALUES {guest_id} {allergen.id}"
        
        self.__cursor.execute(query)

        return Guest(guest_id, booking, guest_name, allergies)

    def create_new_booking(self, customer : Customer, holiday : Holiday) -> Booking:
        """write a new booking to the database
        return omdels if valid"""
        booking_id = randint(0, 999999)

        self.__cursor.execute(f"INSERT INTO BOOKING VALUES('{booking_id}', '{customer.id}', '{holiday.id}', NULL)")

        return Booking(booking_id, customer, holiday, None)

    def get_food_choice_by_name(self, food_choice : str) -> Food:
        record = self.__cursor.execute(f"SELECT * FROM GUEST_FOOD WHERE FoodChoice = '{food_choice}'").fetchone()
        if record:
            return Food(*record)
        return None

    def create_new_food_choice(self, guest, food_choice : str) -> Food:

        food_id = self.__cursor.execute(f"INSERT INTO GUEST_FOOD VALUES('NULL, '{guest.id}', '{food_choice}') RETURNING FOOD.FoodID")

        return Food(food_id, guest, food_choice)
    
    def process_booking(self, form_data) -> tuple[Customer, Booking, list[Guest]]:
        """Validates that the data received from the front end is axceptable returns models if valid"""

        # extract data from post request body
        
        holiday_id = form_data.get("holiday_id")
        forename = form_data.get("forename")
        surname = form_data.get("surname")
        telephone = form_data.get("telephone")
        guests = form_data.get("guests")

        if holiday_id is None:
            raise AttributeError("holiday_id was not found in post request data")
        
        if not isinstance(holiday_id, str):
            raise TypeError("holiday_id was not a string")
        
        holiday = self.get_holiday_by_id(holiday_id)

        # if it isn't - error

        if not holiday:
            raise DatabaseError(f"Holiday_id {holiday_id} not found in the database")

        # check if the customer's forename/surname exists, and is in the database ?

        if not forename:
            raise AttributeError("forename was not found in post request data")

        if not isinstance(forename, str):
            raise TypeError("forename was not a string")
        
        if not surname:
            raise AttributeError("surname was not found in post request data")
    
        if not isinstance(surname, str):
            raise TypeError("surname was not a string")
        
        customer - self.get_customer_by_names(forename, surname)
        if customer is None:
            customer = self.create_new_customer(forename, surname, telephone)
        

        booking = self.create_new_booking(customer, holiday)

        if not guests:
            raise AttributeError("Guest data missing from post request")
    
        if not isinstance(guests,list):
            raise TypeError("guests was not a list")
        
        for guest in guests:

            # to do - client will deal with missing data 
            # assume everything OK if we got to this point

            meal = guest.get("meal")
            allergens = guest.get("allergens")
            name = guest.get("name")

            if not name:
                raise AttributeError("guest name missing from post request data")

            if not meal:
                raise AttributeError(f"guest {name}'s meal missin from post request data")
            
            meal = self.get_food_choice_by_name(meal)

            if not meal:
                raise DatabaseError (f"meal {meal} does not exist")
        
            if not allergens:
                raise AttributeError(f"guest {name}'s allergies missin from post request data")
            
            valid_allergens : list[Allergen]= []

            for allergen in allergens:
                allergen = self.get_allergen_by_name(allergen)
                if not allergen:
                    raise DatabaseError (f" allergen {allergen} does not exist in database")
                
                valid_allergens.append(allergen)
                
            guest = self.create_new_guest(booking, name, valid_allergens)
            food_choice = self.create_new_food_choice(guest, meal)
            





        return holiday, customer, booking, guests, allergens
        
    

if __name__ == "__main__":
    # tests
    print(db.get_holidays("New York"))
    

    # should see martin davies