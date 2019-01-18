import datetime
import json
import os
import random
import sys
import textwrap
from sys import getsizeof

import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_cors import CORS

import rarbgapi

sys.path.insert(0, '..')
import keys

app = Flask(__name__)

CORS(app, origins=r"*")

OMBD_URL = "http://www.omdbapi.com/"
TORRENT_API = rarbgapi.RarbgAPI()

SUPPORTED_CATEGORIES = {
    "software":     TORRENT_API.CATEGORY_SOFTWARE,
    "ebooks":       TORRENT_API.CATEGORY_EBOOK,
    "movies":       TORRENT_API.CATEGORY_MOVIES_ALL,
    "TV-series":    TORRENT_API.CATEGORY_TV_ALL,
    "music":        TORRENT_API.CATEGORY_MUSIC_ALL,
    "games":        TORRENT_API.CATEGORY_GAMES_ALL,
    "all":          None
}


@app.errorhandler(404)
def page_not_found(e):

    # note that we set the 404 status explicitly
    return json.dumps({"error": "requested resource does not exist on torrent server"}), 404


@app.route("/categories", methods=["GET"])
def get_categories():
    """Returns the supported categories. This is basically always the same content, and the categories
    are *hardcoded* in the service, so that is why it is not possible for this to fail. 

    .. :quickref: Get Categories; Returns the supported categories.

    **Example request:**

    .. code-block:: http

        GET /categories HTTP/1.1
        Host: http://www.torrent.com
        Accept: application/json


    **Example response:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "categories": [
                "software",
                "ebooks",
                "movies",
                "TV-series",
                "music",
                "games",
                "all"
            ]
        }


    :status 200: able to list categories
    """
    return json.dumps({"categories": list(SUPPORTED_CATEGORIES.keys())}), 200


@app.route("/categories/<category>", methods=["GET"])
def get_information_on_category_for_date(category):
    """Asks the torrent information provider for torrents about the specified category and 
    returns top torrents as dictionaries with the keys already properly formatted. If the 
    specified category is either *movie* or *TV-series* then the service will also include
    IMDB information as part of the return data.

    .. :quickref: Get Category Information; Returns top torrents for the specified category.

    For all categories the service returns: **Title**, **Seeders**, and **Leechers**. When 
    the category is *movie* or *TV-series* then the service also returns the following 
    information for each torrent:

    * **Runtime**
    * **Genre**
    * **Director**
    * **Awards**
    * **Rating**
    * **Plot**

    This service only returns data on the top 7 torrents.

    **Example request:**

    .. code-block:: http

        GET /categories/movies HTTP/1.1
        Host: http://www.torrent.com
        Accept: application/json


    **Example response:** *(note that we're only showing one result in the response, so as to save space, but 
    usually there would be 7)*

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "data": [
                {
                    "Title": "The Girl in the Spider's Web",
                    "Seeders": 5644,
                    "Leechers": 2568,
                    "Runtime": "117 min",
                    "Genre": "Action, Crime, Drama, Thriller",
                    "Director": "Fede Alvarez",
                    "Awards": "N/A",
                    "Rating (IMDB)": "6.1",
                    "Plot": "Young computer hacker Lisbeth Salander and journalist Mikael Blomkvist find themselves caught in a web of spies, cybercriminals and corrupt government officials."
                },

            ]
        }

    :query category: the category we're interested in getting information about
    :status 400: the specified category is not valid
    :status 200: data for category has been successfully found
    """
    if category not in SUPPORTED_CATEGORIES:
        return json.dumps({"error": "Invalid category"}), 400

    torrents = TORRENT_API.list(sort="seeders", format_="json_extended",
                                category=SUPPORTED_CATEGORIES.get(category))

    # only process top 7 torrents
    if len(torrents) > 7:
        torrents = torrents[:7]

    def process_as_movie_tv(tm: rarbgapi.Torrent) -> str:
        params = {
            "apikey": keys.OMBD_KEY,
            "i": tm.imdb_id
        }

        data = requests.get(OMBD_URL, params=params).json()

        return {
            "Title": data.get("Title"),
            "Seeders": tm.seeders,
            "Leechers": tm.leechers,
            "Runtime": data.get("Runtime"),
            "Genre": data.get("Genre"),
            "Director": data.get("Director"),
            "Awards": data.get("Awards"),
            "Rating (IMDB)": data.get("imdbRating"),
            "Plot": data.get("Plot"),
        }

    def process_as_other(tm: rarbgapi.Torrent) -> str:
        return {
            "Title": tm.filename,
            "Seeders": tm.seeders,
            "Leechers": tm.leechers,
        }

    results = []
    # if we're talking about movies or tvseries then we need to get info from IMDB
    for mm in torrents:
        if hasattr(mm, "imdb_id") and mm.imdb_id:
            ir = process_as_movie_tv(mm)

        else:
            ir = process_as_other(mm)

        results.append(ir)

    return json.dumps({"data": results}), 200


if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"

    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(host='0.0.0.0', port=7802, debug=True, use_reloader=True)
