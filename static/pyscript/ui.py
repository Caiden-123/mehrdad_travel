from pyscript import document, when

from api import get_request_holidays, post_request_booking


holiday = ""



    
@when("change", "#trip")
def select_holiday(e):
    # get the rest of the form elements out of the DOM (getElementById)
    # un-disable all of them

    print("select_holiday")
    form = document.getElementsByClassName("booking")[0]

    inputs = form.getElementsByTagName("input")
    selects = form.getElementsByTagName("select") 

    for _input_ in inputs:
         _input_.disabled = False
    
    for select in selects:
        select.disabled = False

def create_booking():
    # get the stuff from the fields

    customer_forename, customer_surname = document.getElementById("cust-name").value.split(" ")
    customer_telephone = document.getElementById("cust-tell").value


    guest_name = document.getElementById("guest1".value)
    allergies = document.getElementsByClassName("checkboxes")
    guest_allergies = []

    for allergy in guest_allergies:
        if allergy.checked:
            guest_allergies.append(allergy.name)


    # make dictionary (which contains a Holiday object, and a customer object)
    booking = {"customer_forename" : customer_forename, "customer_surname" : customer_surname, "customer_telephone": customer_telephone, "holiday_id" : None, "guest" : [{"guest_name" : guest_name, "allergies" : guest_allergies, "food" : None}]}

    
@when("click",) 
async def click_book_holiday(e):
    '''Triggers a request to add the new booking to the database'''
    booking = create_booking()
    feedback = await post_request_booking(booking)

@when("click",)
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

        # add as a child of the select element

        select_var.appendChild(option)
    
