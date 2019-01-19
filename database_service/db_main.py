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
    """Returns the records (dates) that we have information of in the database. 

    .. :quickref: Get Records; Returns list of dates in database.

    **Example request:**

    .. code-block:: http

        GET /records HTTP/1.1
        Host: http://tupini07.pythonanywhere.com
        Accept: application/json


    **Example response:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "data":
            [
                "2019-01-14",
                "2019-01-15",
                "2019-01-16",
                "2019-01-17"
            ]
        }

    :query app_id: this is the id of the app
    :status 422: the ``app_id`` parameter was not provided
    :status 206: no records found in database 
    :status 200: records found
    """

    app_id = request.args.get("app_id")
    if not app_id:
        return json.dumps({"error": "No 'app_id' parameter has been provided"}), 422

    sess = Session()

    results = sess.query(Record.date).filter(
        Record.app_id == app_id).order_by(desc(Record.date))

    if "limit" in request.args:
        results = results.limit(int(request.args.get("limit")))

    results = results.all()

    sess.close()

    if len(results) == 0:
        return json.dumps({"data": []}), 206

    else:
        results = set([str(x[0]) for x in results])
        return json.dumps({"data": list(results)}), 200


@app.route("/records/<date>/categories", methods=["GET"])
def get_categories_for_date(date):
    """Returns the list of categories for which we have information in the 
    database for a specific date. 

    .. :quickref: Get Categories for Date; Returns list of categories for which we have information for a date.

    **Example request:**

    .. code-block:: http

        GET /records/2019-01-16/categories HTTP/1.1
        Host: http://tupini07.pythonanywhere.com
        Accept: application/json


    **Example response:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "data":
            [
                "ebooks",
                "movies",
                "TV-series"
            ]
        }

    :query app_id: this is the id of the app
    :query date: the date for which we want to get the list of available categories

    :status 422: the ``app_id`` parameter was not provided
    :status 422: the date parameter is not properly formatted
    :status 206: no records found in database 
    :status 200: records found
    """

    app_id = request.args.get("app_id")
    if not app_id:
        return json.dumps({"error": "No 'app_id' parameter has been provided"}), 422

    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    session = Session()
    results = session.query(Record.category).filter(
        Record.date == date).filter(Record.app_id == app_id).all()
    session.close()

    if len(results) == 0:
        return json.dumps({"data": []}), 206

    else:
        results = set([str(x[0]) for x in results])
        return json.dumps({"data": list(results)}), 200


@app.route("/records/<date>/categories/<category>", methods=["GET"])
def get_information_on_category_for_date(date, category):
    """Get the entry we have saved for a specific category on a specific date. This endpoint will 
    first check if we have a corresponding entry for the combined (date, category) and if yes then
    it will attempt to pull the information from the corresponding pastebin page.

    On some occasions Pastebin will complain saing that a paste is SPAM and a captcha has to 
    be filled to see the paste's content. In this case the endpoing will just return the pastebin 
    URL and it will be up to the user to go to the URL, solve the captcha, and see the paste.

    Note that the content returned for the category is completely arbitrary, and is up to the creator
    of said content to specify it.

    .. :quickref: Get Category Information for Date; Returns information we have saved for a category on a specific date.

    **Example request:**

    .. code-block:: http

        GET /records/2019-01-16/categories/ebooks HTTP/1.1
        Host: http://tupini07.pythonanywhere.com
        Accept: application/json


    **Example response:** *(Note: this result has been shortened to save space. Normally the result will contain 7 entries insted of 2)*

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: text/javascript

        {
            "data": `
            Title: Accidental Texting: Finding Love despite the Spotl .EPUB
            Seeders: 4
            Leechers: 0

            Title: Tear You Apart by Megan Hart .PDF
            Seeders: 3
            Leechers: 0

            This data can also be found in pastebin, at the following URL: https://pastebin.com/9tggfzGT
            `
        }

    :query app_id: this is the id of the app category
    :query date: the date which we're interested in
    :query category: the category we're interested in

    :status 422: the ``app_id`` parameter was not provided
    :status 422: the date parameter is not properly formatted
    :status 500: pastebin is asking for captcha verification (only pastebin URL is returned in this case)
    :status 206: no records found in database 
    :status 200: records found
    """

    app_id = request.args.get("app_id")
    if not app_id:
        return json.dumps({"error": "No 'app_id' parameter has been provided"}), 422

    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    session = Session()
    result = session.query(Record.url).filter(Record.app_id == app_id).filter(
        Record.date == date).filter(Record.category == category).first()
    session.close()

    if not result:
        return json.dumps({"error": "There are no records for the specified combination of category and date."}), 206

    pastebin_url = result[0]

    pastebin_data = pastebin_wrapper.get_paste(pastebin_url)

    if "Your paste has triggered our automatic SPAM" in pastebin_data:
        # pastebin is asking for captcha
        return json.dumps({"data": pastebin_url}), 500
    else:
        return json.dumps({"data": pastebin_data}), 200


@app.route("/records/<date>/categories", methods=["POST"])
def create_category_entry_on_date(date):
    """Allow us to create a new entry for the specified ``date`` and ``category``, which will
    have the specified ``content`` (both content and category are passed as parameters
    in the request body). 

    .. :quickref: Create Entry; Creates entry for date+category combination.

    **Example request:**

    .. code-block:: http

        POST /records/2019-01-17/categories HTTP/1.1
        Host: http://tupini07.pythonanywhere.com
        Accept: application/json

        {
            "content": "some test content",
            "category": "test-category"
        }

    **Example response:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "data": "some test content\\n\\nThis data can also be found in pastebin, at the following URL: https://pastebin.com/raw/2VTRywd3"
        }

    :query app_id: this is the id of the app
    :query date: the date for which we want to create a new category entry

    :json category: this is the name of the category which we want to create
    :json content: this is the content that we want to associate with the category

    :status 422: the ``app_id`` parameter was not provided
    :status 422: the date parameter is not properly formatted
    :status 422: no ``category`` parameter is present in the request body
    :status 422: no ``content`` parameter is present in the request body

    :status 409: records already exists for combination date+category

    :status 500: cannot create entry in pastebin. This happens when the service exceeds the 24h paste limit

    :status 201: new record created successfully 
    """

    app_id = request.args.get("app_id")
    if not app_id:
        return json.dumps({"error": "No 'app_id' parameter has been provided"}), 422

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
        exists = session.query(Record.url).filter(Record.app_id == app_id).filter(
            Record.date == date).filter(Record.category == category).first()

        ret_code = 201
        if exists:
            ret_code = 409  # 409 = conflict
            paste_url = exists[0]

            pastebin_data = pastebin_wrapper.get_paste(paste_url, wrap=False)

            if not "Your paste has triggered our automatic SPAM" in pastebin_data:
                content = pastebin_data

        else:
            try:
                paste_url = pastebin_wrapper.add_paste(content)

                session.add(Record(category=category,
                                   date=date, url=paste_url, app_id=app_id))
                session.commit()
                session.close()

            except RuntimeError:
                return json.dumps({"error": ("Database service was not able to create entry in database. "
                                             "Possibly because we've exceeded the daily paste limit in pastebin.")}), 500  # this happens when we exceed paste limit in pastebin

        return json.dumps({"data": pastebin_wrapper._wrap_data_with_information(content, paste_url)}), ret_code


@app.route("/records/<date>/categories/<category>", methods=["PUT"])
def update_record(date, category):
    """Allow us to update an entry for the specified ``date`` and ``category``, with 
    the specified  ``content`` (which is passed as parameter
    in the request body). 

    Basically what is done is that a new paste in pastebin is created and the URL
    associated with the record gets updated to the URL of the new paste.

    .. :quickref: Update Entry; Updates an entry of date+category combination.

    **Example request:**

    .. code-block:: http

        PUT /records/2019-01-17/categories/movies HTTP/1.1
        Host: http://tupini07.pythonanywhere.com
        Accept: application/json

        {
            "content": "some new content to replace the old content",
        }

    **Example response:**

    .. code-block:: http

        HTTP/1.1 200 OK
        Vary: Accept
        Content-Type: application/json

        {
            "data": "https://pastebin.com/raw/sXCVakjQ"
        }

    :query app_id: this is the id of the app
    :query date: the date for which we want to update the entry
    :query category: the category for which we want to update the entry

    :json content: this is the new content that we want to associate with the category

    :status 422: the ``app_id`` parameter was not provided
    :status 422: the date parameter is not properly formatted
    :status 422: no ``content`` parameter is present in the request body

    :status 206: there is no record with the combination date+category so no update is possible

    :status 500: cannot create entry in pastebin. This happens when the service exceeds the 24h paste limit

    :status 200: record updated successfully
    """

    app_id = request.args.get("app_id")
    if not app_id:
        return json.dumps({"error": "No 'app_id' parameter has been provided"}), 422

    if "content" not in request.form.keys():
        return json.dumps({"error": "No content specified in the request body."}), 422

    try:
        date = [int(x) for x in date.split("-")]
        date = datetime.date(*date)

    except Exception:
        return json.dumps({"error": "Date is not properly formated, it should have the following format: YYYY-MM-DD"}), 422

    content = request.form.get("content")

    session = Session()
    result = session.query(Record).filter_by(
        app_id=app_id, date=date, category=category).first()

    if not result:
        session.close()
        return json.dumps({"error": "There is no record for the specified date and category so no update can be made."}), 206

    try:
        paste_url = pastebin_wrapper.add_paste(content)
        result.url = paste_url
        session.commit()

    except RuntimeError:
        return json.dumps({"error": ("Database service was not able to create entry in database. "
                                     "Possibly because we've exceeded the daily paste limit in pastebin.")}), 500  # this happens when we exceed paste limit in pastebin
    finally:
        session.close()

    return json.dumps({"data": result.url}), 200


if __name__ == "__main__":

    os.environ["FLASK_ENV"] = "development"

    app.secret_key = os.urandom(12)  # Generic key for dev purposes only
    app.run(host='0.0.0.0', port=7801, debug=True, use_reloader=True)
