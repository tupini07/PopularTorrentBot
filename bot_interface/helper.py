import requests
import sys
import datetime
import functools
import datetime
from typing import List

DATABASE_SERVICE_ADDRESS = "http://127.0.0.1:7801"
TORRENT_SERVICE_ADDRESS = "http://127.0.0.1:7802"


def _service_call(c_type=""):
    def _dec_scall(f):

        functools.wraps(f)

        def wrapper(*args, **kwargs):
            try:
                return f(*args, **kwargs)
            except requests.exceptions.ConnectionError:
                return (f"There was an error connecting to the {c_type} service. "
                        "It seems that it is currently offline.")

        return wrapper

    return _dec_scall


def join_list_into_message(lst) -> str:
    return "\n".join("- " + c for c in lst)


@_service_call("torrent")
def get_supported_categories() -> List:
    return requests.get(TORRENT_SERVICE_ADDRESS + "/categories").json()["categories"]


@_service_call("database")
def get_dates_in_record(limit=15) -> List:
    res = requests.get(DATABASE_SERVICE_ADDRESS + "/records",
                        params={
                            "limit": limit
                        }).json()["data"]

    if res.status_code == 204:
        return "There are no records in the database, sorry!"

    else:
        return res.json()["data"]



@_service_call("database")
def get_record_of_categories_on_date(dt: str) -> List:
    res = requests.get(DATABASE_SERVICE_ADDRESS + f"/records/{dt}/categories")
    
    if res.status_code == 422:
        return res.json()["error"]

    elif res.status_code == 204:
        return "There is no data available in the database for the specified date."

    else:
        return res.json()["data"]


# TODO: Consider having torrent service returning JSON, also DB service could return JSON so that we comply with service
# specification

# The torrent service shouldn't talk with the database service.
# The bot is the one that consumes both services and is the one that should integrate them

# code extracted from torrent service. Use this to communicate with database and integrate DB + torrent

# today = str(datetime.datetime.now().date())

# try:
#     # Ask database to see if we have record in memory
#     res = requests.get(DATABASE_SERVICE_ADDRESS +
#                     f"/records/{today}/categories/{category}")

#     # Then result exists and just return that
#     if res.status_code == 200:
#         return res.text, 200

# except requests.exceptions.ConnectionError:
#     pass


# try:
#     res = requests.post(DATABASE_SERVICE_ADDRESS +
#                         f"/records/{today}/categories",
#                         data={"category": category,
#                             "content": content})

#     if res.status_code == 500:
#         return res.text + ("\nDatabase service was not able to create entry in database. "
#                             "Possibly because we've exceeded the paste limit in pastebin")

#     else:
#         return res.text, 200 # could create and add content in DB

# except requests.exceptions.ConnectionError:
#     pass
