from typing import Tuple
from random import randint
import sqlite3

#test


class Database:
    def __init__(self):
        self.__conn = sqlite3.connect("./db/holidays.db")
        self.__cursor = self.__conn.cursor()
    
    def close(self):
        self.__conn.close()

    def add_new_customer(self, forename: str, surname: str, telephone: str):
        id_ = forename[0] + surname[:2].upper() + str(randint(111, 999))
        self.__cursor.execute(f"INSERT INTO Customer VALUES ('{id_}', '{forename}', '{surname}', '{telephone}')")
        self.__conn.commit()

    def get_all_customers(self) -> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM Customer").fetchall()
        return records
    
    def get_holidays(self, location: str)-> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM Holiday WHERE Location = ?", (location,))
        return records

    def delete_holidays(self, location:str)-> Tuple[Tuple]:
        records = self.__cursor.execute("DELETE * FROM Holiday WHERE Location = ?", (location,))
        return records
    
    def get_bookings(self, Booking_id:str)-> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM BOOKINGS WHERE BookingID = ?", (Booking_id,))
        return records
    
    def get_all_allergen(self) -> Tuple[Tuple]:
        records = self.__cursor.execute("SELECT * FROM ALLERGEN").fetchall()
        return records





db = Database()


if __name__ == "__main__":
    # tests
    print(db.get_holidays("New York"))

    # should see martin davies

db.close()