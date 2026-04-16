from pyscript import document, when
from api import get_request_holidays

@when("click", ".search-cta")
def click_go():
    holidays = get_request_holidays()
    print(holidays)


# go_button = document.GetElementsByClassName("search-cta")[0]
