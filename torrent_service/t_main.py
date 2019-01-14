import datetime
import json
import os
import random
import textwrap
from sys import getsizeof

import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_cors import CORS
import requests

import rarbgapi

app = Flask(__name__)

CORS(app, origins=r"*")

TORRENT_API = rarbgapi.RarbgAPI()

SUPPORTED_CATEGORIES = [
    "software",     # CATEGORY_SOFTWARE,
    "ebooks",       # CATEGORY_EBOOK,
    "movies",       # CATEGORY_MOVIES_ALL,
    "TV-series",    # CATEGORY_TV_ALL,
    "music",        # CATEGORY_MUSIC_ALL,
    "games"         # CATEGORY_GAMES_ALL,
]


@app.errorhandler(404)
def page_not_found(e):

    # note that we set the 404 status explicitly
    return json.dumps({"error": "requested resource does not exist on torrent server"}), 404


@app.route("/categories", methods=["GET"])
def get_categories():
    """
    Returns the categories that we support in general
    """
    return json.dumps(SUPPORTED_CATEGORIES), 200


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




if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"

    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(host='0.0.0.0', port=7802, debug=True, use_reloader=True)
