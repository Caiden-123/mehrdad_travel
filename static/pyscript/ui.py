from pyscript import document, when, display

from api import get_request_holidays, post_request_booking

from dto import parse_booking, parse_guest

holiday = ""



    
@when("change", "#trip")
def select_holiday(e):
    # get the rest of the form elements out of the DOM (getElementById)
    # un-disable all of them

    print("select_holiday")
    form = document.getElementsByClassName("booking")[0]
    inputs = form.querySelectorAll("input, button, select")

    for _input_ in inputs:
         _input_.disabled = False

def create_booking():
    # get the stuff from the fields

    customer_name = document.getElementById("cust-name").value
    customer_telephone = document.getElementById("cust-tel").value

    guest_meal = document.getElementById("meal")
    guest_name = document.getElementById("guest1").value
    allergies = document.getElementsByClassName("checkboxes")
    guest_allergies = []
    for allergy in guest_allergies:
        try:
            if allergy.checked:
                guest_allergies.append(allergy.name)
        except AttributeError:
            pass

    
    holiday_id = document.getElementById("trip").value


    # come back to multiple guests later

    guest = parse_guest(guest_name, allergies, guest_meal)

    guest = [guest]

    booking = parse_booking(customer_name, customer_telephone, holiday_id, guest)

    return booking
    # make dictionary (which contains a Holiday object, and a customer object)



@when("click", "#book_holiday") 
async def click_book_holiday(e):
    '''Triggers a request to add the new booking to the database'''
    booking = create_booking()
    feedback = await post_request_booking(booking)
    display(feedback)

async def click_add_another_guest():
    '''Duplicates the customer form for another guest'''

def save_for_later():
    '''Save the partially completed form using a cookie'''

@when("click", ".search-cta")
async def click_go(e):

    '''Sends a request to the database to find holidays matching the location the user enters'''

    location_input = document.getElementById("dest")
    location = location_input.value

    holidays = await get_request_holidays(location)
    
    load_holidays_to_select_trip_dropdown(holidays)
    print("click_go")

def load_holidays_to_select_trip_dropdown(holidays):

    # get/add something from/to the HTML DOM - syntax guide

    # element = document.getElementById("<id goes here")

    # element = document.createElement("<tag>")
    
    # parent_element.appendChild(child_element)


    # get the select parent element and store in a var

    # set the property disabled TO FALSE

    select_var = document.getElementById("trip")

    select_var.disabled = False

    for holiday in holidays:

        duration = holiday["duration"]
        location = holiday["location"]
        date = holiday["departure_date"]

        # make that look nice for the user

        option_text = (f"Going to {location}, departing on {date} ({duration} days)")

        # make an option

        option = document.createElement("option")

        # set the text of the option to the string you made

        option.innerHTML = option_text

        option.value = holiday["id"]

        # add as a child of the select element

        select_var.appendChild(option)

        
    
