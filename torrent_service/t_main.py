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
    """
    Returns the categories that we support in general
    """
    return json.dumps({"categories": list(SUPPORTED_CATEGORIES.keys())}), 200


@app.route("/categories/<category>", methods=["GET"])
def get_information_on_category_for_date(category):
    """
    Gets the information for category for today. It does this by first checking
    if there is an entry in the database for today with said category. If there is then
    it just returns that. If on the other hand there isn't then it will get information from 
    torrent API and create an entry in the database. Then returns. 
    """

    if category not in SUPPORTED_CATEGORIES:
        return json.dumps({"error": "Invalid category"}), 404

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
