import datetime
import json
import os
import random
import textwrap
from sys import getsizeof

import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_cors import CORS

import pastebin_wrapper
from db_resources import Record, Session
from sqlalchemy import desc

app = Flask(__name__)

CORS(app, origins=r"*")


@app.errorhandler(404)
def page_not_found(e):

    # note that we set the 404 status explicitly
    return json.dumps({"error": "requested resource does not exist on database server"}), 404


@app.route("/records", methods=["GET"])
def get_records():

    sess = Session()

    results = sess.query(Record.date).order_by(desc(Record.date))

    if "limit" in request.args:
        results = results.limit(int(request.args.get("limit")))

    results = results.all()

    sess.close()

    if len(results) == 0:
        return "[]", 204

    else:
        results = set([str(x[0]) for x in results])
        return json.dumps(list(results)), 200


@app.route("/records/<date>/categories", methods=["GET"])
def get_categories_for_date(date):
    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    session = Session()
    results = session.query(Record.category).filter(Record.date == date).all()
    session.close()

    if len(results) == 0:
        return "[]", 204

    else:
        results = set([str(x[0]) for x in results])
        return json.dumps(list(results)), 200


@app.route("/records/<date>/categories/<category>", methods=["GET"])
def get_information_on_category_for_date(date, category):

    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    session = Session()
    result = session.query(Record.url).filter(
        Record.date == date).filter(Record.category == category).first()
    session.close()

    if not result:
        return json.dumps({"error": "There are no records for the specified combination of category and date."}), 204

    pastebin_url = result[0]

    pastebin_data = pastebin_wrapper.get_paste(pastebin_url)

    return pastebin_data + textwrap.dedent(f"""

    This data can also be found in pastebin, at the following URL: {pastebin_url}
    """), 200


@app.route("/records/<date>/categories", methods=["POST"])
def create_category_entry_on_date(date):

    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    if "category" not in request.form.keys():
        return json.dumps({"error": "No category specified in the request body."}), 422

    elif "content" not in request.form.keys():
        return json.dumps({"error": "No content specified in the request body."}), 422

    else:
        category = request.form.get("category")
        content = request.form.get("content")

        # first, check is paste already exists
        session = Session()
        result = session.query(Record.url).filter(
            Record.date == date).filter(Record.category == category).first()

        if result:
            return json.dumps({"url": result[0]}), 409  # 409 = conflict

        paste_url = pastebin_wrapper.add_paste(content)

        session.add(Record(category=category, date=date, url=paste_url))
        session.commit()
        session.close()

        return json.dumps({"url": paste_url}), 201  # created


if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"

    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(host='0.0.0.0', port=7801, debug=True, use_reloader=True)
