from typing import Any

def parse_booking(customer_name: str,
                  telephone: str,
                  holiday_id: str,
                  guests: list[dict[str, Any]]) -> dict[str, Any]:
    
    name = customer_name.split(maxsplit = 1)
    if len(name) == 1:
        forename, surname = name[0], name[0]
    else:
        forename, surname = name

    return {"forename": forename, 
            "surname": surname,
            "holiday_id": holiday_id,
            "telephone": telephone,
            "guests": guests  }

def parse_guest(name: str,
                allergens: list[str],
                meal: str
                ) -> dict[str, Any]:
    pass
    return {"name": name, 
            "allergens": allergens, 
            "meal": meal}