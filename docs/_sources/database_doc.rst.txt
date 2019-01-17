Database Service Documentation
==============================

All requests to databse must be authenticated with an `app_id` parameter.
This allows the database to return the values for said application. Basically, 
the database service keeps a `(key : value)` collection for a specific application. 

requires api key for pastebin


Endpoint Reference Table
************************

.. qrefflask:: db_main:app
   :undoc-static:

Endpoint Documentation
**********************

.. autoflask:: db_main:app
   :undoc-static: