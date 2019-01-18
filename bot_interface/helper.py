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


def join_list_into_message(lst, joiner="-") -> str:
    return "\n".join(joiner + " " + c for c in lst)


@_service_call("torrent")
def get_supported_categories() -> List:
    return requests.get(TORRENT_SERVICE_ADDRESS + "/categories").json()["categories"]


@_service_call("database")
def get_dates_in_record(limit=15) -> List:
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
def get_information_for_category_on_date(category: str, date="today"):
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
