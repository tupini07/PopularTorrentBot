Database Service Documentation
==============================

The database service is composed of two main parts. A local database (using SQLite) and 
an external repository of data (Pastebin). The local database is very simple, it only saves 
entries of the shape ``(app_id, date, category, URL)``, where ``app_id`` tells the database
who is accessing it, the ``date`` is the date for which we want to get/create a category, and
``category`` is the *key* we're interested in.

All requests to databse must be authenticated with an ``app_id`` parameter.
This allows the database to return the values for said application. Basically, 
the database service keeps a `(key : value)` collection for a specific application. 

When a request is made to the database, for a specifc combination of ``[app_id, date, category]``
the service will obtain the pastebin URL (if any) and it will make a request to this URL and obtain
the actual data the user is interested in. We can think that pastebin is our actual data repository
and the local database is only an index.

Required Authentication
***********************

The authentication steps in the database service are two, one made by the user (when specifying the
``app_id`` parameter), and the other is made by the service when it authenticates with pastebin so
that it can create pastes.



Endpoint Reference Table
************************

.. qrefflask:: db_main:app
   :undoc-static:

Endpoint Documentation
**********************

.. autoflask:: db_main:app
   :undoc-static: