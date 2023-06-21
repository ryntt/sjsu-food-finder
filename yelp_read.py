"""
Implements methods to effectively utilize Yelp's API.

This program contains code necessary to authorize a user on Yelp's API
and allow said user to retrieve information. It also contains several
lines of code to store essential constant variables such as URLs to
use with the API and default arguments to pass through. Some lines of
code also allow the code to read from a protected .env file.

Two of the methods, return_best_results() and return_details(), call
Yelp's API to retrieve specific information and are only accessed when
the bot recognizes specific inputted user arguments. The
eatery_list_string() method is meant to return a string representation
of a list of restaurants, though it can return a string representation
of any list passed to it.
"""

import requests
import json
import os
from dotenv import load_dotenv

# API authorization
load_dotenv()
API_KEY = os.getenv('API_KEY')
HEADERS = {'Authorization': 'Bearer %s' % API_KEY}  # authorization
GENERAL_URL = 'https://api.yelp.com/v3/businesses/search'
DETAILED_URL = 'https://api.yelp.com/v3/businesses/'

# preset query parameters
LOCATION = '1 Washington Sq, San Jose, CA 95192'  # SJSU
TERM = 'food'
RADIUS = 1610  # 1 mile radius
DEFAULT_LIMIT = 5
DEFAULT_RATING = 3.5
DEFAULT_PRICE = 2
DEFAULT_CATEGORY = 'ANY'


def return_best_results(category, limit, rating, price):
    """
    Passes the given arguments and some defaults to Yelp's API, then
    takes the list of returned results and keeps any restaurant within
    a specific rating range.
    :param category: (string) an optional restaurant category
    :param limit: (int) an optional results limit, default is 5
    :param rating: (float) an optional rating minimum, default is 3.5
    :param price: (float) an optional price value, default is 2
    :return: a list of the best matching restaurants
    """
    result_list = []
    params = {'location': LOCATION, 'term': TERM, 'radius': RADIUS,
              'price': price}
    if category != DEFAULT_CATEGORY:
        params['categories'] = category
    req = requests.get(GENERAL_URL, params=params, headers=HEADERS)
    # returns a list of each location
    places = json.loads(req.text)['businesses']
    current_val = 0
    for place in places:
        if place["rating"] >= rating and rating <= 5.0 and current_val < limit:
            result_list.append(place["name"])
            current_val += 1
    return result_list


def eatery_list_string(eatery_list):
    """
    Accepts a given list of restaurants and returns a string
    representation of it.
    :param eatery_list: (list) the list to accept
    :return: a string representation of eatery_list
    """
    result_str = ''
    for eatery in eatery_list:
        result_str = result_str + f'Name: {eatery}\n'
    return result_str


def return_details(eatery_name):
    """
    Accepts the name of a restaurant, retrieves its Yelp business ID
    through a series of API calls, and finds and returns essential
    details of the business by searching for it using its business ID.
    :param eatery_name: (str) the name of the restaurant
    :return: a string representation of essential details
    """
    # retrieves the business id through the restaurant arg and then
    # calls this id in businesses/{id} from Yelp API
    params = {'location': LOCATION, 'term': eatery_name, 'radius': RADIUS,
              'limit': 1}
    req = requests.get(GENERAL_URL, params=params, headers=HEADERS)
    best_match = json.loads(req.text)['businesses'][0]
    best_match_url = f'{DETAILED_URL}{best_match["id"]}'
    best_match_req = requests.get(best_match_url, headers=HEADERS)
    details = json.loads(best_match_req.text)

    # retrieves details of restaurant from both businesses/{id} and
    # businesses/search when needed
    name = details["name"]
    address = details["location"]["address1"]
    city, state, zip_code = details["location"]["city"], details[
        "location"]["state"], details["location"]["zip_code"]
    phone_number = details["display_phone"]
    rating = details["rating"]
    relative_dist = round(best_match["distance"] / RADIUS, 1)
    open_now = "Yes" if details["hours"][0]["is_open_now"] else "No"

    result = f'Name: {name}\n' \
             f'Address: {address}\n' \
             f'              {city}, {state}, {zip_code}\n' \
             f'Phone Number: {phone_number}\n' \
             f'Rating: {rating}/5\n' \
             f'Distance: Around {relative_dist} mi from SJSU\n' \
             f'Open now: {open_now}'
    return result


def main():
    print(return_details("house of bagels"))


if __name__ == "__main__":
    main()
