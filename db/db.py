from typing import Tuple
from random import randint
import sqlite3

#test


class Database:
    def __enter__(self):
        self.__conn = sqlite3.connect("./db/holidays.db")
        self.__cursor = self.__conn.cursor()
        return self
    
    def __exit__(self, *args):
        try:
            self.__conn.close()
        except:
            print("dsadsadsaqwertyuiokjnbvcde45678ikjnbv cxzsdertyuio")


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


