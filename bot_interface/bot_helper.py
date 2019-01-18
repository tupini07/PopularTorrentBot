"""
The *bot_helper* module contains "helper" functions for the telegram bot. Basically these are all the functions that 
bot uses, but the main bot file `bot_main <https://github.com/tupini07/PopularTorrentBot/blob/master/bot_interface/bot_main.py>`_ 
only contains the code for setting up the proper callbacks: 
when a user inputs a comment via telegram, *bot_main* will ensure that the proper function from this file
get invoked.
"""

import requests
import sys
import datetime
import functools
import datetime
from typing import List

DATABASE_SERVICE_ADDRESS = "http://127.0.0.1:7801"
TORRENT_SERVICE_ADDRESS = "http://127.0.0.1:7802"
APP_ID = "PopularTorrentsBotAppId"


def _service_call(c_type=""):
    """
    Just a decorator that tells the user an error message in case that
    the services (torrent or database) are not reachable

    :param c_type: if the function that we're decorating is either ``database`` or ``torrent``

    :returns: a wrapped function
    """

    def _dec_scall(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                return (f"There was an error connecting to the {c_type} service. "
                        "It seems that it is currently offline.")

        return wrapper

    return _dec_scall


def join_list_into_message(lst: List[str], joiner="-") -> str:
    """
    Helper function that converts a list into a *bulleted list*

    :param lst: the list of strings that we want to convert into bullets
    :param joiner: the character that will be used to denote a bullet

    :returns: A bulleted list
    """

    return "\n".join(joiner + " " + c for c in lst)


@_service_call("torrent")
def get_supported_categories() -> List:
    """
    We do a request to the torrent service to see which categories are supported

    :returns: the list of supported categories
    """

    return requests.get(TORRENT_SERVICE_ADDRESS + "/categories").json()["categories"]


@_service_call("database")
def get_dates_in_record(limit=15) -> List:
    """
    Here we do a request to the database service and get a list of the dates it has 
    in record.

    :param limit: the maximum amount of records we want to fetch

    :returns: the list of records that the database service has
    """

    res = requests.get(DATABASE_SERVICE_ADDRESS + "/records",
                       params={
                           "limit": limit,
                           "app_id": APP_ID
                       })

    if res.status_code == 206:
        return "There are no records in the database, sorry!"

    else:
        return res.json()["data"]


@_service_call("database")
def get_record_of_categories_on_date(dt: str) -> List:
    """
    Here we do a request to the database service and ask, for a specific date, which 
    categories do we have records on

    :param dt: the date in YYYY-MM-DD format

    :returns: a list of categories for which we have a record for the specified date
    """

    res = requests.get(DATABASE_SERVICE_ADDRESS + f"/records/{dt}/categories",
                       params={
                           "app_id": APP_ID
                       })

    if res.status_code == 422:
        return res.json()["error"]

    elif res.status_code == 206:
        return "There is no data available in the database for the specified date."

    else:
        return res.json()["data"]


@_service_call()
def get_information_for_category_on_date(category: str, date="today") -> str:
    """
    Get the information we have on a specific date for a specific category. This information 
    is asked to the database service, and if the date is today and no information is found
    for the specified category then we ask the torrent service for that category information. 
    Once we get it we then proceed to send it to the database service for storage.

    This method is what the user calls if he/she wants to know the top torrents for a specifc
    category for a specific date.

    Note that if the user asks for a date which we don't have in the database then a message
    saying so is displayed to the user.

    :param category: the category we want to get information about
    :param date: the date we want to get information about

    :returns: the actual string of information to display to the user. This is either an 
        error message or a message with all the top torrents for a specific category for a 
        specific date.
    """

    today = str(datetime.datetime.now().date())
    pastebin_url = None

    if not date or date.lower() == "today":
        date = today

    starting_message = f"Most popular '{category}' torrents for '{date}' \n\n"

    #################################################################
    # Ask database to see if we have record in memory
    res = requests.get(DATABASE_SERVICE_ADDRESS +
                       f"/records/{date}/categories/{category}",
                       params={
                           "app_id": APP_ID
                       })

    # Then result exists and just return that
    if res.status_code == 200:
        return starting_message + res.json()["data"]

    # in case it exists but pastbin is asking for captcha confirmation
    elif res.status_code == 500:
        # if the result exists and the date is today then we just ask for the information to the
        # torrent service once more

        if date == today:
            pastebin_url = res.json()["data"]

        else:
            return (f"We do have data for this category and date, and it can be found here: {res.json()['data']} "
                    "But sadly we can't access it programatically since it's asking for captcha verification "
                    "so you'll need to open the link and fill it up yourself.")

    elif res.status_code == 422 or (res.status_code == 206 and date != today):
        return res.json()["error"]

    #################################################################
    # get torrent information
    res = requests.get(TORRENT_SERVICE_ADDRESS + f"/categories/{category}")

    if res.status_code == 400:
        return res.json()["error"]

    res = res.json()["data"]

    # format result
    output = []
    for it in res:
        output.append("\n".join(f"{k}: {v}" for k, v in it.items()))
    output = "\n\n".join(output)

    # now, if we already have a pastebin url (meaning that the request was for today
    # and that we have the information in the database but pastebin is asking for captcha)
    # then we proceed to just add this to the end of the result and return this
    if pastebin_url:
        return starting_message + output + "\n\nThis data can also be found in Pastebin, at the following URL: " + pastebin_url

    #################################################################
    # add to database

    res = requests.post(DATABASE_SERVICE_ADDRESS +
                        f"/records/{today}/categories",
                        params={"app_id": APP_ID},
                        data={"category": category,
                              "content": output})

    if res.status_code == 422:
        return res.json()["error"]

    elif res.status_code == 500:

        if date == today:
            sorry_message = ("It seems that we've exceeded the pastebin limit for these 24 hours. "
                             "So the entry could not be created in the database (meaning that the data will not be availble "
                             "for future reference), please try later. In the meantime I've gotten the torrent information "
                             "data for today.\n\n")

            return sorry_message + starting_message + output

        else:
            return res.json()["error"]

    else:
        return starting_message + res.json()["data"]
