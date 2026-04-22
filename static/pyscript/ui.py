from pyscript import document, when

from api import get_request_holidays


@when("select", "#trip")
def select_holiday(e):
    # get the rest of the form elements out of the DOM (getElementById)


    form = document.getElementsByClassName("booking")
    for child in form:
        


    # un-disable all of them

    # store which holiday was clicked
    holiday = e.target.innerHTML



@when("click", ".search-cta")
async def click_go(e):

    location_input = document.getElementById("dest")
    location = location_input.value

    holidays = await get_request_holidays(location)
    
    load_holidays_to_select_trip_dropdown(holidays)



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
        print(holiday)

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